---
name: local-music-generation
description: Generate cheap/local procedural background music as WAV/MP3 with genre presets, humanization, anti-loop rules, and public listen links. Use this for lo-fi, cozy background music, ambient beds, simple game/menu music, and rough punk/pop-punk demos without Suno.
tags: [music, procedural-audio, lofi, background-music, local-generation, mp3, python, creative]
triggers:
  - generate background music
  - make lofi
  - local music generation
  - procedural music
  - cheap alternative to Suno
  - make a music link
  - render mp3
  - youtube background music
related_skills: [strudel-music, songwriting-and-ai-music]
---

# Local Music Generation

Use this skill when the user wants **cheap/local generated music** rendered to audio files, especially background music, lo-fi, ambient, cozy loops, game/menu music, or rough punk/pop-punk demos.

This is not a replacement for Suno/Udio-quality full songs with vocals. It is useful for:
- background beds
- lo-fi/study music
- cozy app/site/video music
- ambient loops
- simple game/menu tracks
- educational demos
- cheap iterative sketches

## Core principle

Do not generate “one random loop repeated for 2 minutes.” Generate a **small arrangement**:

```text
Intro → A → A' → B → A'' → breakdown/bridge → final A/B → ending/fade
```

Even background music needs subtle movement.

---

## Rendering backends

### Backend A — Pure Python synth

Use when speed/reliability matters. No extra dependencies beyond Python + ffmpeg.

Good for:
- lo-fi beds
- ambient pads
- cozy/simple game music
- drones
- procedural texture

Weak for:
- realistic rock guitar
- vocals
- acoustic realism

### Backend B — SoundFont/MIDI

Use when a more instrument-like sound is needed. Local system may have:

```text
/usr/share/sounds/sf2/default-GM.sf2
/usr/share/sounds/sf2/TimGM6mb.sf2
/usr/share/sounds/sf3/default-GM.sf3
```

Good for:
- piano/electric piano
- bass
- strings/pads
- GM drums
- simple pop/rock demos

Weak for:
- convincing distorted guitars
- modern production polish

### Backend C — Sample-pack hybrid

Best long-term option if free/licensed samples are available.

Good for:
- real drum one-shots
- vinyl noise
- texture loops
- lo-fi percussion
- guitar/piano phrases

Rule: never use samples unless licensing is clear.

---

## Genre presets

### lofi-study

Target:
- soft, non-distracting, warm
- 70–88 BPM
- 60–180 seconds
- can loop, but with subtle variation

Use:
- dusty electric piano / soft piano approximation
- warm sine/triangle bass
- soft kick/snare/rim/hat
- vinyl noise / tape hiss
- subtle wow/flutter pitch drift
- simple 7th/9th chords if possible

Avoid:
- bright square leads
- aggressive saws
- hard distortion
- busy melodies
- big cymbal crashes

Arrangement:
```text
0–8 bars: intro, filtered/chords only
8–24 bars: drums + bass enter
24–40 bars: melody fragments
40–56 bars: B section / chord variation
56–72 bars: return A with small fills
last bars: strip drums or fade
```

### cozy-background

Use:
- marimba/pluck/bell/soft pad
- simple bass
- tiny percussion
- warm room/reverb

Avoid:
- harsh transients
- strong hooks
- dense drums

### ambient-soft

Use:
- slow pads
- low drone
- sparse bell tones
- long fades

Avoid:
- obvious beat
- repetitive melody
- too much high-frequency hiss

### simple-corporate

Use:
- muted pluck
- soft piano
- simple four-chord progression
- light kick/clap

Avoid:
- cheese if possible
- over-bright synth brass
- aggressive drums

### 2000s-pop-punk-demo

Use:
- acoustic-ish drums
- picked bass
- muted verse guitar
- open chorus power chords
- octave lead only in phrases

Avoid:
- game-like square leads
- excessive distortion
- same 4 bars repeated constantly

---

## Humanization rules

Always apply some of these unless the user explicitly wants robotic/electronic:

- timing offset: ±5–20 ms depending genre
- velocity/gain variation: ±5–20%
- drum fills every 8 or 16 bars, not every bar
- chord voicing changes every section
- melody appears in phrases, not constantly
- vary hats/percussion subtly
- final section should differ from first section
- fade or deliberate ending, not abrupt stop

For lo-fi specifically:
- add vinyl/tape hiss quietly
- use wow/flutter: slow pitch/amplitude modulation
- slightly low-pass bright elements
- leave space

---

## Anti-loop checklist

Before sending a generated track, ask:

- Does the same 4-bar idea repeat for the whole track?
- Is there an intro?
- Is there a B section or breakdown?
- Does something change every 8 bars?
- Does the lead shut up sometimes?
- Does the final section feel slightly fuller or different?
- Does the fade/end feel intentional?

For background music, repetition is allowed, but exact repetition is not.

---

## Quality checklist

Listen mentally / inspect generation choices before publishing:

- No clipping; normalize below ~0.92 peak.
- Bass is not too loud.
- Hiss/noise is quiet, not masking music.
- Lead is not game-like unless requested.
- Distortion is minimal except punk/grunge.
- Drum transients are not painfully sharp.
- Track has a public MP3 link and a simple listen page.

---

## Recommended workflow

1. Pick preset: `lofi-study`, `cozy-background`, `ambient-soft`, `simple-corporate`, `2000s-pop-punk-demo`.
2. Pick duration and seed.
3. Render WAV locally.
4. Encode MP3 with ffmpeg.
5. Publish to `/home/hermes/apps/container-host/music/<slug>/`.
6. Create a simple listen/download `index.html`.
7. Verify local and public URLs return `200 OK`.

Public host workflow:

```bash
mkdir -p /home/hermes/apps/container-host/music/<slug>
cp track.mp3 track.wav /home/hermes/apps/container-host/music/<slug>/
curl -I http://localhost:5090/music/<slug>/
curl -I https://container.omarbenaidy.com/music/<slug>/
```

---

## Script usage

This skill includes a reusable starter renderer:

```bash
python ~/.hermes/skills/creative/local-music-generation/scripts/render_music.py \
  --style lofi-study \
  --duration 120 \
  --seed 42 \
  --slug rainy-desk \
  --outdir /home/hermes/generated-music
```

Expected outputs:

```text
<outdir>/<slug>.wav
<outdir>/<slug>.mp3
```

If the script is not enough for a request, modify or fork it, but keep the preset concepts and quality checklist above.

---

## When to push back

Be honest if the user asks for:
- realistic vocals
- radio-ready pop/rock
- Suno-quality guitars
- exact artist imitation

Say: local procedural generation can sketch the vibe cheaply, but realism needs samples, SoundFonts, or a dedicated music model.
