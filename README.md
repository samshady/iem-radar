# IEM Radar & Buyer's Guide (2026)

A structured database and interactive web dashboard evaluating budget and benchmark In-Ear Monitors (IEMs), specifically tailored for European/German buyers with live pricing comparisons, reviewer consensus scores, and ergonomic sizing metrics.

## Workspace Structure

```
iem-radar/
├── data/
│   └── iems.json          # Master database of 21+ IEMs (specs, pricing, scores, fit notes)
├── scripts/
│   └── build.py           # Python script that compiles iems.json into dist/index.html
├── dist/
│   └── index.html         # Standalone, interactive single-page application
└── README.md
```

## How to Update the Database

Whenever new IEMs are released or prices change:
1. Open `data/iems.json`.
2. Add a new entry or update existing prices/scores.
3. Re-build the dashboard:
   ```bash
   python3 scripts/build.py
   ```
4. Open `dist/index.html` in your browser.

## Features of the Dashboard
- **Persona Matcher**: Filter instantly for Tactical Gaming, Vocal & Acoustic, Studio Reference, Warm Daily Listening, Bassheads, USB-C DSP, or Small Ears & Bedtime.
- **German / EU Pricing**: Compares Amazon.de Prime, AliExpress Choice Day, and 11.11 Mega Sale pricing.
- **Anatomy & Fit Warning**: Highlights nozzle diameters (warning for >6.0mm nozzles like Truthear Zero:RED).
- **Reviewer Consensus**: Synthesizes grades from Crinacle, Super* Review (Mark Ryan), Jay's Audio, and Timmy (Gizaudio).
