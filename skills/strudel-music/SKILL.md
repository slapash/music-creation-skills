---
name: strudel-music
description: Create Strudel live-coding music sketches and workflows, especially pop punk, grunge, and punk-inspired browser music patterns.
tags: [strudel, music, live-coding, algorave, pop-punk, grunge, punk, creative]
triggers:
  - strudel
  - live coding music
  - make music with code
  - browser music pattern
  - algorave
  - pop punk beat
  - grunge riff
  - punk song sketch
  - code music
related_skills: [songwriting-and-ai-music]
---

# Strudel Music

Use this skill when the user wants music made with **Strudel**: browser-based live coding using the TidalCycles-style pattern language in JavaScript.

User taste note: lean toward **pop punk, grunge, punk** unless they ask otherwise. Prefer raw, hooky, energetic sketches over overly polished EDM. Think: fast drums, distorted power-chord energy, driving eighth-note bass, noisy leads, simple memorable hooks.

Main references:
- Strudel docs: https://strudel.cc/learn/getting-started/
- Mini notation: https://strudel.cc/learn/mini-notation/
- Samples: https://strudel.cc/learn/samples/
- Audio effects: https://strudel.cc/learn/effects/
- Time modifiers: https://strudel.cc/learn/time-modifiers/
- Tonal functions / voicings: https://strudel.cc/learn/tonal/
- Recipes: https://strudel.cc/recipes/recipes/

---

## Core mental model

Strudel patterns are short loops. Build from **one good cycle**, then layer and mutate.

Common primitives:

```js
s("bd sd bd sd")              // sample playback: bass drum, snare
note("c3 eb3 g3").s("sawtooth")
stack(patternA, patternB)      // play patterns together
setcpm(160/4)                  // tempo: cycles per minute; often BPM / 4 for 4/4 bars
```

Mini-notation essentials:

```js
s("bd sd hh")                 // sequence events over a cycle
s("bd ~ sd ~")                // ~ or - = rest
s("hh*8")                     // repeat 8 times per cycle
s("[bd hh] sd")               // bracket = subdivision inside one event
s("<bd sd cp>")               // alternate one item per cycle
s("bd(3,8)")                  // Euclidean rhythm: 3 hits across 8 slots
note("g3,b3,d4")              // comma = polyphony / chord
note("[g3,b3,d4] [a3,c4,e4]") // sequence of chords needs brackets
```

Useful modifiers:

```js
.fast(2)      // speed up
.slow(2)      // slow down over 2 cycles
.early(.02)   // nudge earlier
.late(.02)    // nudge later
.clip(.5)     // shorten notes/samples
.gain(.7)     // volume
.pan(.3)      // stereo position
.room(.2)     // reverb send
.delay(.125)  // delay send
.lpf(1200)    // low-pass filter
.hpf(200)     // high-pass filter
.shape(.4)    // waveshaping distortion
.distort(.5)  // distortion
.crush(6)     // bitcrush
.bank("RolandTR909") // choose drum-machine sample bank
.n("0 1 2")   // sample index / scale degree depending context
```

Important effects pitfall: many Strudel effects are effectively **single-use in the signal chain**. Repeating the same effect later can override the earlier value. Do not write `.lpf(200).distort(.4).lpf(1200)` expecting two filters. Use one deliberate value/pattern.

---

## Default workflow

1. **Set tempo and key/energy**
   - Pop punk: 150–190 BPM, major/minor power-chord movement, bright but rough.
   - Punk: 170–220 BPM, simpler, faster, fewer fills.
   - Grunge: 90–145 BPM, heavier, sludgier, minor/modal, more space.

2. **Start with drums**
   - Kick/snare shape is the song’s spine.
   - Add hats/ride only after the core beat hits.

3. **Add bass**
   - Root notes, repeated eighths, octave jumps.
   - Slight distortion, low-pass, short release.

4. **Add guitar surrogate**
   - Use `sawtooth`, `square`, or built-in GM electric guitar samples if available.
   - Fake power chords with root + fifth + octave.
   - Use `.shape()`, `.distort()`, `.crush()`, `.room()` sparingly.

5. **Add hook/lead**
   - 3–6 note motif. Repeat it. Vary it every 4th cycle.

6. **Add arrangement changes**
   - Use `<...>` to alternate sections.
   - Use `.mask()`, `.sometimes()`, `.degradeBy()`, `.fast()`, `.slow()` for fills and breakdowns.

7. **Keep output runnable**
   - Give one complete Strudel block.
   - Avoid imaginary APIs.
   - Include comments, but not so many that they obscure the pattern.

---

## Genre recipes

### Pop punk sketch

Characteristics:
- 150–190 BPM
- kick/snare backbeat
- constant hats or ride
- root-fifth-octave power chords
- bass follows guitar roots
- bright hook, minimal jazz harmony

Chord moves that work:
- I–V–vi–IV: C G Am F
- vi–IV–I–V: Am F C G
- I–IV–V: C F G
- i–VI–III–VII for darker pop-punk: Em C G D

Starter:

```js
setcpm(44) // ~176 BPM if one cycle = one 4/4 bar

stack(
  // Drums: driving backbeat
  s("bd [~ bd] sd [bd ~] bd [~ bd] sd [~ bd], hh*8")
    .bank("RolandTR909")
    .gain(.85),

  // Bass: eighth-note roots
  note("<c2 g1 a1 f1>*8")
    .s("sawtooth")
    .clip(.35)
    .lpf(900)
    .shape(.25)
    .gain(.55),

  // Power-chord guitar surrogate: root + fifth + octave
  note("<[c3,g3,c4] [g2,d3,g3] [a2,e3,a3] [f2,c3,f3]>")
    .s("sawtooth, square:0:.35")
    .clip(.85)
    .distort(.45)
    .hpf(120)
    .room(.18)
    .gain(.45),

  // Hooky lead, enters with simple repetition
  note("<e4 g4 a4 g4 [e4 d4] c4 d4 ~>")
    .s("square")
    .clip(.25)
    .delay(.125)
    .room(.25)
    .gain(.28)
)
```

### Punk sketch

Characteristics:
- 180–220 BPM
- simple three-chord riff
- fewer effects, more velocity/urgency
- drums should feel relentless

```js
setcpm(50) // ~200 BPM

stack(
  s("bd sd bd sd, hh*8")
    .bank("RolandTR909")
    .gain(.9),

  note("<e2 e2 g2 a2>*8")
    .s("sawtooth")
    .clip(.25)
    .shape(.35)
    .lpf(1000)
    .gain(.55),

  note("<[e3,b3,e4] [e3,b3,e4] [g3,d4,g4] [a3,e4,a4]>")
    .s("sawtooth")
    .clip(.45)
    .distort(.65)
    .hpf(140)
    .gain(.5),

  // Noisy shouty motif
  note("<e4 ~ g4 a4>*2")
    .s("square")
    .clip(.18)
    .crush(7)
    .gain(.25)
)
```

### Grunge sketch

Characteristics:
- 90–145 BPM
- half-time or heavy backbeat
- minor key / modal riffs
- fuzz, low-pass, noisy space
- verse can be sparse, chorus can explode

```js
setcpm(30) // ~120 BPM

stack(
  // Heavy half-time feel
  s("bd ~ ~ ~ sd ~ bd ~, hh*8")
    .bank("RolandTR909")
    .gain(.85),

  // Sludgy bass riff
  note("<e2 e2 g2 e2 [d2 e2] ~ g1 ~>*2")
    .s("sawtooth")
    .clip(.5)
    .lpf(650)
    .shape(.5)
    .gain(.6),

  // Dirty power chords
  note("<[e3,b3,e4]@2 [g3,d4,g4] [d3,a3,d4] [c3,g3,c4]>")
    .s("sawtooth, square:0:.4")
    .clip(1)
    .distort(.7)
    .lpf(1800)
    .room(.3)
    .gain(.48),

  // Uneasy lead fragment
  note("<g4 ~ e4 [d4 e4] ~ b3>*2")
    .s("triangle")
    .clip(.4)
    .delay(.25)
    .room(.45)
    .gain(.25)
)
```

---

## Arrangement patterns

Use angle brackets to alternate sections across cycles:

```js
s("<bd sd bd sd, bd ~ sd ~>")
```

Use section comments and masks:

```js
stack(
  s("bd [~ bd] sd [bd ~], hh*8"),
  note("<c2 g1 a1 f1>*8").s("sawtooth"),
  note("e4 g4 a4 g4").s("square").mask("<0 1 1 1>") // silent first cycle
)
```

Useful rock arrangement template:

```js
// 4-cycle loop: intro / verse / chorus / fill
// cycle 1: fewer drums, no lead
// cycle 2: verse groove
// cycle 3: chorus opens up
// cycle 4: fill or turnaround
```

Practical methods:
- `.mask("<0 1 1 1>")` to introduce a layer after the first cycle.
- `.sometimesBy(.25, x => x.fast(2))` for occasional fills.
- `.degradeBy(.2)` for missing notes / human looseness.
- `.early(.01)` or `.late(.01)` for feel, especially hats/snares.
- `.gain("<.4 .5 .7 .6>")` to create section dynamics.

---

## AI-assisted Strudel workflow

When asked to use AI to help write Strudel:

1. Ask or infer:
   - genre/subgenre
   - BPM
   - mood
   - key/chord progression
   - number of sections
   - whether the output should be beginner-friendly or performance-ready

2. Generate a **minimal runnable seed** first:
   - one `setcpm`
   - one `stack(...)`
   - drums + bass + chord/riff + optional lead

3. Then produce **3 variation prompts** for iteration:
   - “make drums more frantic”
   - “make chorus brighter”
   - “make verse grungier and sparse”

4. If using an LLM to create code, constrain it:

```text
Write runnable Strudel code only. Use core functions: setcpm, stack, s, note, n, scale, chord, voicing, fast, slow, clip, gain, bank, room, delay, lpf, hpf, shape, distort, crush, mask, sometimesBy. Avoid undocumented APIs. Keep it under 80 lines. Genre: pop punk / grunge / punk.
```

---

## Debugging and cleanup

If the pattern is broken:
- Check quotes and parentheses first.
- Make sure `stack(...)` items are comma-separated.
- If a melody is too busy, reduce notes before adding effects.
- If it clips/distorts badly, lower `.gain()` on every layer before changing effects.
- If drums are missing, try removing `.bank(...)` because some banks lack some samples.
- Strudel’s GM soundfont samples include realistic instrument names such as `gm_electric_guitar_muted`, `gm_overdriven_guitar`, `gm_distortion_guitar`, and `gm_electric_bass_pick`. These are registered by `@strudel/soundfonts`; use them with `note(...).s("gm_distortion_guitar")` / `note(...).s("gm_electric_bass_pick")`. They load WebAudioFont data from `https://felixroos.github.io/webaudiofontdata/sound/*.js`; default usable files include `0300_FluidR3_GM_sf2_file` for distortion guitar, `0290_FluidR3_GM_sf2_file` for overdriven guitar, `0280/0281_*` for muted guitar, and `0340_FluidR3_GM_sf2_file` for picked bass. If rendering outside Strudel, these JS files contain base64 MP3 zones that can be extracted and sequenced directly.
- If guitar sample names fail, use synths (`sawtooth`, `square`, `triangle`) instead of relying on sample availability.
- If modulation sounds static, add `.seg(16)` before parameter modulation where appropriate, because some params are sampled only on events.

Good gain starting points:
- drums `.gain(.75-.9)`
- bass `.gain(.45-.65)`
- chords `.gain(.35-.55)`
- lead `.gain(.2-.35)`

Avoid:
- 10 layers in the first draft.
- Jazz chords unless requested.
- Too much reverb for punk.
- Over-randomizing: punk needs commitment, not generative mush.
- Fake artist-name imitation. Describe genre and production traits instead.

---

## Response format when generating Strudel

Use this structure:

1. One-sentence concept.
2. Complete Strudel code block.
3. “Tweak knobs” list with 3–5 obvious edits.
4. Optional next variation.

Example:

```markdown
Here’s a fast pop-punk Strudel sketch: backbeat drums, eighth-note bass, power-chord synth guitar, and a simple square-wave hook.

```js
...
```

Tweak knobs:
- Faster: raise `setcpm(44)` to `setcpm(48)`.
- Dirtier: raise `.distort(.45)` on the chord layer.
- More grunge: lower tempo and change progression to `Em C G D`.
```

---

## Educational use

For kids/teens or beginner workshops:
- Start with `s("bd sd")`.
- Add `hh*8`.
- Change one thing at a time.
- Treat code as a sequencer, not programming theory.
- Have learners remix genre knobs: tempo, drums, bass root, instrument sound.

Beginner ladder:

```js
s("bd sd")
s("bd sd, hh*8")
stack(s("bd sd, hh*8"), note("c2 g1 a1 f1").s("sawtooth"))
```

Then explain:
- spaces = sequence
- comma = together
- `*8` = repeat
- `~` = silence
- `<>` = alternate
