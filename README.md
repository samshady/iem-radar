# IEM Radar, Audio Bench & Hardware Toolkit (2026)

A structured database and interactive web dashboard evaluating budget and benchmark In-Ear Monitors (IEMs), budget headphones (< €100), and bone conduction transducers, specifically tailored for European/German buyers with live pricing comparisons, acoustic sound profiles, reviewer consensus scores, and ergonomic sizing metrics.

The live interactive application is deployed at: [https://samshady.github.io/iem-radar/](https://samshady.github.io/iem-radar/)

---

## Workspace Structure

```
iem-radar/
├── data/
│   └── iems.json               # Master database of 30 IEMs & TWS sets (specs, pricing, scores, fit notes)
├── scripts/
│   ├── build.py                # Python script that compiles iems.json into dist/index.html & index.html
│   ├── template_body.html      # Modular HTML layout (sound bench, toolkit tabs, headphone & bone benches)
│   └── test_e2e.py             # Playwright E2E test suite (62 test assertions across desktop/mobile)
├── tests/
│   └── screenshots/            # Automated visual verification captures (desktop 1440, mobile 390 & 360)
├── assets/
│   └── images/                 # Local verified product photography
├── dist/
│   └── index.html              # Standalone production distribution file
├── index.html                  # Root entrypoint for GitHub Pages hosting
└── README.md
```

---

## What's in the Guide

### 1. Curated IEM & TWS Catalog (30 Benchmark Sets)
- **Ultra-Budget Champions (< €25)**: GK Kunten, Tangzu Wan'er 2, Truthear Gate, Tanchjim Bunny, Moondrop Chu II, 7Hz Zero:2, TinHiFi C0 Clean.
- **Mid-Tier Value (€25 to €50)**: TRN Conch, Tripowin Vivace (tactical FPS), TinHiFi C2 Mech Warrior (all-metal CNC), Moondrop LAN (stainless steel VDSF), Kiwi Ears Belle, 7Hz G1, DUNU Titan X, 7Hz Elua Ultra, ooopusX Op.22.
- **Reference & Hybrid Tier (€50 to €85)**: Truthear Hexa (1DD + 3BA clinical benchmark), Kefine Delci (CNC metal warm bass), Kefine Klean, Kiwi Ears Cadenza II, Truthear Zero:BLUE 2, Truthear Zero:RED, Moondrop May (Planar + DD with USB-C DSP), Moondrop Aria 2.
- **Audiophile Chi-Fi TWS**: Moondrop Space Travel 1, Moondrop Space Travel 2, QCY MeloBuds Pro (HT08 / LDAC), QCY MeloBuds N70, EarFun Air Pro 4 (Snapdragon Sound / aptX Lossless / 50dB ANC).

### 2. Dedicated Budget Headphone Bench (< €100)
- 10 curated over-ear and on-ear benchmarks: FiiO JT1 (JadeAudio 50mm dynamic), FiiO EH11 (retro wireless on-ear with wood cups), FiiO EH13 (wireless ANC over-ear), Moondrop Old Fashioned (retro 80s open-back on-ear), Moondrop Joker (50mm closed-back monitoring), Philips SHP9500 (50mm open-back soundstage champion), Koss KSC75 (titanium clip-on legend), Koss Porta Pro, Creative Aurvana Live! SE (Foster bio-cellulose driver), Superlux HD681.

### 3. Dedicated Bone Conduction Bench & Transducer Guide
- **Curated Benchmarks**: Shokz OpenRun (8th gen bone conduction benchmark), Shokz OpenRun Pro 2 (DualPitch hybrid bone + air conduction), Haylou PurFree BC01 (Qualcomm QCC3044, cVc dual-mic, titanium frame, IP67).
- **Buyer Diagnostic Checks**: Earplug Occlusion Test, 2mm Hover Test, Table Resonance Test to expose fake directional micro-speakers masquerading as bone conduction.

### 4. Audiophile Gear Toolkit (10 Deep Technical Tabs)
1. **Ear Tips & Wave Guide**: Divinus Velvet, Softears UC, FiiO HS18, DUNU S&S, SpinFit W1, Tangzu Tang Sancai. Includes direct Wave Guide Figma chart and video fitting guides.
2. **Dongle DACs & Silicon Architecture**: Apple USB-C Dongle (US 1.0Vrms vs EU 0.5Vrms), FiiO JA11, JCALLY JM12, JCALLY JM6 Pro, FiiO KA11, Moondrop Dawn Pro. Chipset matrix (KT02H20, CX31993, CS43131, ES9318C) and the sub-€10 firmware cross-flashing PEQ guide (flashing FiiO JA11 firmware onto JCALLY JM12).
3. **Audio Formats & Codecs**: Lossless vs lossy (FLAC vs MP3), Redbook CD (16-bit/44.1kHz) vs 24-bit Hi-Res, blind ABX testing reality, Bluetooth codecs (SBC, AAC, aptX Lossless, LDAC, LC3).
4. **Driver Tech & Diaphragm Materials**: PET, LCP, DLC, Beryllium, Bio-cellulose, Balanced Armatures, Planar Magnetic, and Silicon MEMS micro-speakers.
5. **Tuning Curves & Frequency Anatomy**: Harman Target, Diffuse Field, IEF Neutral, Moondrop VDSF, and 6 acoustic frequency zones (Sub-bass, Mid-bass, Lower midrange, Pinna gain, Treble presence, Upper treble air).
6. **Cables & Connector Standards**: 0.78mm 2-Pin, QDC, MMCX, modular plugs, Tripowin Zonie, NiceHCK BlackCat, and cable snake-oil reality check.
7. **Wireless & ANC Mechanics**: Latency, hybrid ANC mechanics, modular Bluetooth earhooks (TRN BT20XS), TWS microphone beamforming and Qualcomm cVc 8.0.
8. **Bone Conduction Physics**: Cranial acoustic impedance, anti-phase acoustic venting (LeakSlayer), and true transducers vs air micro-speakers.
9. **Microphone Lab**: In-line mic limitations, Kinera Celest Ruyi, TRN RedChain Plus, Tripowin Grace, Moondrop FreeDSP, V-MODA BoomPro, and 4-tier vocal hierarchy.
10. **Care & Maintenance**: Super* Review Forever IEMs masterclass, over-under roadie wrap tutorial, silica gel packets, and earwax mesh maintenance.

### 5. Audiophile Sound Bench Player
- Sticky zero-login cyberdeck audio player streaming licensed test tracks via verified YouTube API endpoints.
- Curated test playlists:
  - **Kessoku Band (Bocchi the Rock!)**: Tests guitar transients, rhythm separation, and treble harshness.
  - **YOASOBI**: Tests female vocal sibilance, piano timbre, and choir dynamic range.
  - **Eurobeat (Initial D Classics)**: Tests bass speed, synthesizer attack, and diaphragm damping.

---

## How to Build and Test

1. Update `data/iems.json` or `scripts/template_body.html`.
2. Compile the static application:
   ```bash
   python3 scripts/build.py
   ```
3. Run the automated Playwright test suite:
   ```bash
   python3 scripts/test_e2e.py
   ```
4. Check for zero em-dashes across all files:
   ```bash
   grep -n -E "—|–" scripts/template_body.html dist/index.html README.md
   ```
