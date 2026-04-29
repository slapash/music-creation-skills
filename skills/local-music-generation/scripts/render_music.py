#!/usr/bin/env python3
"""Tiny local procedural music renderer.

Currently implements: lofi-study.
No external Python deps. Requires ffmpeg for MP3 encoding.
"""
import argparse, math, random, struct, subprocess, wave
from array import array
from pathlib import Path

NOTE={'c':0,'c#':1,'db':1,'d':2,'d#':3,'eb':3,'e':4,'f':5,'f#':6,'gb':6,'g':7,'g#':8,'ab':8,'a':9,'a#':10,'bb':10,'b':11}
CHORDS={
    'Cmaj7':['c3','e3','g3','b3'], 'Am7':['a2','c3','e3','g3'], 'Dm7':['d3','f3','a3','c4'], 'G7':['g2','b2','d3','f3'],
    'Fmaj7':['f2','a2','c3','e3'], 'Em7':['e2','g2','b2','d3'], 'Bbmaj7':['bb2','d3','f3','a3'], 'Ebmaj7':['eb3','g3','bb3','d4'],
}

def midi_freq(name):
    name=name.lower(); key=name[:2] if len(name)>2 and name[1] in '#b' else name[0]; octv=int(name[len(key):])
    midi=12*(octv+1)+NOTE[key]
    return 440*2**((midi-69)/12)
def clamp(x): return max(-1.0,min(1.0,x))
def soft(x,d=1.15): return math.tanh(x*d)/math.tanh(d)
def tri(p): return 4*abs((p+.25)%1-.5)-1

def render_lofi(duration, seed, slug, outdir, bpm=78, sr=44100):
    random.seed(seed)
    beat=60/bpm
    bars=max(16, int(duration/(4*beat)))
    dur=bars*4*beat
    n=int(dur*sr)
    L=array('f',[0.0])*n; R=array('f',[0.0])*n

    def add(t, d, fn, amp=1, pan=.5, human=0.0):
        t += random.uniform(-human,human)
        s=max(0,int(t*sr)); e=min(n,int((t+d)*sr))
        gl=math.cos(pan*math.pi/2); gr=math.sin(pan*math.pi/2)
        for i in range(s,e):
            x=(i-s)/sr; v=fn(x,d)*amp
            L[i]+=v*gl; R[i]+=v*gr

    def ep_chord(t, notes, length, amp=.20, pan=.48):
        freqs=[midi_freq(x) for x in notes]
        def fn(x,d):
            env=min(1,x/.035)*math.exp(-x*.75)*min(1,max(0,d-x)/.2)
            # dusty electric piano: sine-ish fundamental + triangle harmonic + tiny bell transient
            sig=0
            for j,f in enumerate(freqs):
                wow=1+0.0018*math.sin(2*math.pi*(0.18+j*.03)*x + j)
                sig += math.sin(2*math.pi*f*wow*x)*.62 + tri(f*2.01*x+j*.1)*.16 + math.sin(2*math.pi*f*3*x)*.04
            bell=math.sin(2*math.pi*2100*x)*math.exp(-x*16)*.035
            return soft(sig/len(freqs)+bell,1.05)*env
        add(t,length,fn,amp,pan,human=.012)

    def bass(t, note, length, amp=.20):
        f=midi_freq(note)
        def fn(x,d):
            env=min(1,x/.025)*min(1,max(0,d-x)/.15)
            return soft((math.sin(2*math.pi*f*x)*.82+tri(f*x)*.14),1.05)*env
        add(t,length,fn,amp,.45,human=.01)

    def kick(t, amp=.30):
        def fn(x,d):
            return math.sin(2*math.pi*(50+38*math.exp(-x*20))*x)*math.exp(-x*13)
        add(t,.26,fn,amp,.5,human=.008)
    def snare(t, amp=.18):
        def fn(x,d):
            return random.uniform(-1,1)*math.exp(-x*16)*.55 + math.sin(2*math.pi*185*x)*math.exp(-x*9)*.20
        add(t,.20,fn,amp,.54,human=.012)
    def hat(t, amp=.045):
        def fn(x,d):
            return (random.uniform(-1,1)*.75+math.sin(2*math.pi*7600*x)*.25)*math.exp(-x*44)
        add(t,.045,fn,amp,random.uniform(.62,.76),human=.015)
    def rim(t, amp=.09):
        def fn(x,d): return (random.uniform(-1,1)*.35+math.sin(2*math.pi*1250*x)*.65)*math.exp(-x*28)
        add(t,.10,fn,amp,.56,human=.012)
    def lead(t, note, length, amp=.065):
        f=midi_freq(note)
        def fn(x,d):
            env=min(1,x/.04)*min(1,max(0,d-x)/.2)
            vibr=1+0.002*math.sin(2*math.pi*4.2*x)
            return soft(math.sin(2*math.pi*f*vibr*x)*.75+tri(f*x)*.18,1.0)*env
        add(t,length,fn,amp,random.uniform(.55,.68),human=.018)

    # progression: A/A'/B/A'' selected from mellow common lofi moves
    progression=[('Cmaj7','c2'),('Am7','a1'),('Dm7','d2'),('G7','g1')]
    progression_b=[('Fmaj7','f1'),('Em7','e1'),('Dm7','d2'),('G7','g1')]
    melody_pool=['e4','g4','a4','b3','d4','c4','e4','g3']

    for bar in range(bars):
        t=bar*4*beat
        section='intro' if bar<4 else 'a' if bar<20 else 'b' if bar<36 else 'a2' if bar<bars-8 else 'outro'
        prog=progression_b if section=='b' else progression
        cname, root=prog[bar%4]
        notes=CHORDS[cname]
        # chord voicing changes: skip/reorder occasionally
        if bar%8 in (4,5): notes=notes[1:]+notes[:1]
        chord_amp=.13 if section=='intro' else .18 if section=='outro' else .21
        ep_chord(t,notes,beat*3.7,chord_amp)
        if bar%2==1 and section not in ('intro',):
            ep_chord(t+beat*2,notes[1:]+notes[:1],beat*1.6,.08,.42)
        if section!='intro':
            bass(t,root,beat*1.4,.17); bass(t+beat*2,root,beat*1.2,.15)
        # drums enter after intro, thin out near end
        if section not in ('intro','outro') or (section=='outro' and bar<bars-3):
            kick(t,.24); kick(t+beat*2,.18)
            snare(t+beat*1,.15); rim(t+beat*3,.075)
            for h in range(8):
                if random.random()>.18: hat(t+h*beat/2,.035*random.uniform(.75,1.2))
            if bar%8==7:
                snare(t+beat*3.5,.09); hat(t+beat*3.75,.05)
        # sparse melody phrases only in middle sections
        if section in ('a','b','a2') and bar%4 in (2,3) and random.random()>.20:
            phrase=random.sample(melody_pool,4)
            for i,note in enumerate(phrase):
                if random.random()>.28: lead(t+(i+.5)*beat, note, beat*.75, .055 if section!='b' else .065)

    # vinyl/tape hiss and wow-ish amplitude drift
    for i in range(n):
        tt=i/sr
        hiss=random.uniform(-1,1)*0.008
        hum=math.sin(2*math.pi*60*tt)*0.0015
        drift=0.985+0.015*math.sin(2*math.pi*0.08*tt+0.4)
        L[i]=L[i]*drift+hiss+hum
        R[i]=R[i]*(0.99+0.01*math.sin(2*math.pi*0.07*tt))+hiss*.92+hum
    # small cross delay
    for delay,gain in [(int(beat*.75*sr),.035),(int(beat*1.5*sr),.018)]:
        for i in range(delay,n):
            L[i]+=R[i-delay]*gain; R[i]+=L[i-delay]*gain
    # fade in/out
    fade=int(3*sr)
    for i in range(min(fade,n)):
        g=i/fade; L[i]*=g; R[i]*=g
        k=n-1-i; L[k]*=g; R[k]*=g
    peak=max(max(abs(x) for x in L),max(abs(x) for x in R),1e-9)
    scale=.90/peak
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    wav=outdir/f'{slug}.wav'; mp3=outdir/f'{slug}.mp3'
    with wave.open(str(wav),'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        buf=bytearray(); chunk=8192
        for start in range(0,n,chunk):
            buf.clear()
            for a,b in zip(L[start:start+chunk],R[start:start+chunk]):
                buf += struct.pack('<hh',int(clamp(a*scale)*32767),int(clamp(b*scale)*32767))
            w.writeframes(buf)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(wav),'-codec:a','libmp3lame','-b:a','192k',str(mp3)],check=True)
    return wav, mp3, dur

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--style',default='lofi-study')
    ap.add_argument('--duration',type=float,default=90)
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--slug',default='lofi-study-demo')
    ap.add_argument('--outdir',default='/home/hermes/generated-music')
    ap.add_argument('--bpm',type=float,default=78)
    args=ap.parse_args()
    if args.style!='lofi-study':
        raise SystemExit(f'Only lofi-study implemented currently, got {args.style}')
    wav, mp3, dur=render_lofi(args.duration,args.seed,args.slug,args.outdir,args.bpm)
    print(wav); print(mp3); print(f'duration={dur:.1f}s')
if __name__=='__main__': main()
