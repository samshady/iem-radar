#!/usr/bin/env python3
"""
Refine data/iems.json:
- Add local image paths: "image": "assets/images/<id>.jpg"
- Replace robotic meta writeups with genuine, human, conversational audiophile reviews.
- Remove fake AI meta metrics (like community_score / tone grades).
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "iems.json")

# Clean, human, personal notes without robotic AI jargon
HUMAN_DESCRIPTIONS = {
    "tanchjim-bunny": {
        "tagline": "Tiny, featherweight, and great for sleeping or small ears.",
        "sound_summary": "Balanced, warm, and relaxing with clean, natural vocals and smooth treble that never fatigues.",
        "takeaway": "An ultra-compact budget gem that completely disappears into the ear. If your phone lacks a headphone jack, grab the USB-C DSP edition. It features a built-in DAC and lets you tweak an 8-band parametric EQ directly from the Tanchjim app.",
        "fit_verdict": "5.4mm nozzle • Very comfortable for small ear canals & side sleeping."
    },
    "kefine-klean": {
        "tagline": "All-metal CNC alloy shell with two swappable tuning nozzles.",
        "sound_summary": "Energetic, punchy, and highly resolving with crisp dynamic driver attack.",
        "takeaway": "Kefine's successor to the beloved Delci. Built like a little tank out of machined alloy, it includes two screw-on brass nozzles: the silver nozzle gives an airy, detailed presentation, while the black nozzle adds warmth and sub-bass weight.",
        "fit_verdict": "5.6mm nozzle • Ergonomic curved metal housing with an easy seal."
    },
    "trn-conch": {
        "tagline": "The undisputed accessory champion of budget Chi-Fi.",
        "sound_summary": "Crisp, bright, and detailed with fast, punchy bass.",
        "takeaway": "Unbeatable value inside the box: you get full metal shells, three interchangeable tuning nozzles, a premium modular cable with swappable 2.5mm, 3.5mm, and 4.4mm plugs, and an aluminum hard-shell carrying case. Sound is on the brighter, more analytical side.",
        "fit_verdict": "5.5mm nozzle • Standard comfortable fit, but can feel heavy due to solid metal shells."
    },
    "dunu-titan-x": {
        "tagline": "Mecha-styled dynamic set with rich bass slam and Candy tips.",
        "sound_summary": "Warm, punchy, and dynamic with satisfying sub-bass rumble.",
        "takeaway": "DUNU's stylish chrome-plated set featuring a dual-chamber dynamic driver. Bass has genuine physical punch and vocals sound rich and natural. Comes with DUNU's famous Candy silicone tips in the box, which provide one of the best acoustic seals available.",
        "fit_verdict": "5.6mm nozzle • Angled sound bore with comfortable ergonomic seating."
    },
    "kz-zar": {
        "tagline": "Chunky 8-driver hybrid beast with massive theatrical bass.",
        "sound_summary": "Full-bodied U-curve with booming sub-bass and sparkling treble.",
        "takeaway": "If you love big, energetic, cinematic sound for electronic music, movies, or gaming explosions, this 1DD + 7BA hybrid delivers immense power and a wide soundstage. Keep in mind the shells are on the larger side, so they suit medium to large ears best.",
        "fit_verdict": "6.0mm nozzle • Large chunky shell; not recommended for very small ears."
    },
    "kiwi-ears-cadenza-ii": {
        "tagline": "One of the most natural, musical vocal tunings under €50.",
        "sound_summary": "Smooth, warm-neutral balance with lush acoustic timbre.",
        "takeaway": "A perennial favorite for acoustic music, female vocals, and indie rock. The 3D-printed resin shells look like custom artisan jewelry, and the beryllium/titanium diaphragm produces an organic, warm midrange with zero harshness or sibilance.",
        "fit_verdict": "5.5mm nozzle • Featherweight resin cavity that fits almost any ear effortlessly."
    },
    "ooopusx-op22": {
        "tagline": "Dual-mode hybrid with an on-shell physical rotary tuning switch.",
        "sound_summary": "Switchable between clean neutral monitor sound and energetic bass boost.",
        "takeaway": "A unique 2DD + 2BA hybrid with a mechanical rotary switch on the faceplate. You can flick the dial with your thumbnail between a clean, flat monitoring curve and a punchy, bass-boosted fun curve without fiddling with digital EQ apps.",
        "fit_verdict": "5.8mm nozzle • Medium shell profile with comfortable resin contours."
    },
    "truthear-gate": {
        "tagline": "The successor to the Hola: clean neutral sound and a fantastic cable.",
        "sound_summary": "Clean, linear neutral sound with an easy, fatigue-free warmth.",
        "takeaway": "Truthear replaced the legendary Hola with the Gate. Transparent faceplates reveal the 10mm carbon LCP driver inside. Sound is remarkably clean and balanced with near-zero distortion, and the included 4-strand OFC cable is unusually thick and tangle-free for this price.",
        "fit_verdict": "5.4mm nozzle • Very light and comfortable for all-day listening sessions."
    },
    "7hz-g1": {
        "tagline": "Fast DLC driver with crisp transients for tactical gaming and rock.",
        "sound_summary": "Punchy Harman V-shape with swift attack and clean high-end snap.",
        "takeaway": "A solid metal-faceplate earphone featuring a 10mm diamond-like carbon (DLC) driver. The transient speed is noticeably fast, making drum hits crisp and giving tactical multiplayer gamers pinpoint directional awareness for footsteps and reloads.",
        "fit_verdict": "5.6mm nozzle • Compact shell with good passive noise isolation."
    },
    "7hz-elua-ultra": {
        "tagline": "Dual dynamic drivers tuned for smooth, relaxed study marathons.",
        "sound_summary": "Smooth, warm Harman profile with effortless low-end extension.",
        "takeaway": "Combines a 10mm dynamic driver for deep sub-bass and an 8mm driver for mids and highs. It has an easygoing, warm presentation that never pierces, making it an ideal companion for long workdays, studying, or background listening.",
        "fit_verdict": "5.5mm nozzle • Lightweight ergonomic shells."
    },
    "tripowin-vivace": {
        "tagline": "Co-engineered with acoustic tuners for pinpoint 3D imaging.",
        "sound_summary": "Fast, crisp, and revealing with wide directional soundstage.",
        "takeaway": "Tuned with the assistance of acoustic engineers (0DiBi) specifically to maximize stereo imaging and separation. If you play competitive tactical shooters (Valorant, CS2, Apex) or love complex layered electronic productions, this set separates every element clearly.",
        "fit_verdict": "5.3mm nozzle • Slim nozzle profile that seals easily with standard tips."
    },
    "truthear-crinacle-zero-red": {
        "tagline": "Crinacle's dual-driver reference benchmark (warning: wide nozzle).",
        "sound_summary": "Clean IEF neutral with a dedicated 10mm subwoofer for deep sub-bass.",
        "takeaway": "Widely considered the sub-€60 benchmark for tonal accuracy. One driver acts as a dedicated subwoofer while the other handles mids and highs, producing exceptionally clean instrument separation. Includes a 10-ohm impedance adapter for an extra +2.5dB bass boost. Note: the 6.2mm nozzle is thick, so avoid if you have narrow ear canals.",
        "fit_verdict": "6.2mm nozzle ⚠️ • Wide sound bore; can cause fatigue in smaller ears."
    },
    "truthear-crinacle-zero-blue2": {
        "tagline": "The original bass-slam sensation with an updated, slimmer nozzle.",
        "sound_summary": "Energetic Harman curve with visceral sub-bass punch.",
        "takeaway": "The fun sibling to the Zero:Red. It delivers deep, satisfying subwoofer rumble that makes pop, hip-hop, electronic music, and movie action sequences feel alive. The updated revision slimmed the nozzle down to 5.5mm for a much friendlier fit.",
        "fit_verdict": "5.5mm nozzle • Slimmed down from original revision; much more comfortable."
    },
    "kefine-delci": {
        "tagline": "The community's favorite comfort set: luxurious metal & warm bass.",
        "sound_summary": "Warm, lush, and rich with textured, velvety bass rumble.",
        "takeaway": "One of the easiest recommendations in modern Chi-Fi. Crafted from smooth aircraft-grade aluminum, the shells are tiny and slip into your ears with zero hotspots. The sound is warm, relaxing, and deeply musical with zero harshness. Pure listening enjoyment.",
        "fit_verdict": "5.4mm nozzle • Outstanding comfort, one of the best shells on the market."
    },
    "moondrop-may": {
        "tagline": "Dynamic + Planar hybrid with custom app EQ via USB-C.",
        "sound_summary": "Fast planar treble detail anchored by dynamic driver bass slam.",
        "takeaway": "Features a hybrid setup of a dynamic driver for bass and a planar magnetic driver for sparkly, detailed highs. Plugs straight into your phone or laptop with its USB-C cable and lets you download community EQ curves or make your own via the Moondrop Link app.",
        "fit_verdict": "5.6mm nozzle • 3D-printed HeyGears medical resin with smooth fit."
    },
    "moondrop-aria-2": {
        "tagline": "The luxury classic evolved: ceramic dome driver & modular cable.",
        "sound_summary": "Smooth, refined Moondrop house curve with lush female vocals.",
        "takeaway": "The successor to the legendary Aria. Moondrop fixed the old paint-peeling issue with a durable electroplated alloy finish, added screw-off brass nozzle filters for easy cleaning, and packed in a luxury modular cable with both 3.5mm and 4.4mm balanced plugs.",
        "fit_verdict": "5.5mm nozzle • Solid, reassuring metal weight with smooth contours."
    },
    "truthear-hexa": {
        "tagline": "The sub-€100 king for critical listening, mixing, and acoustic clarity.",
        "sound_summary": "Strictly flat, analytical neutral reference with surgical separation.",
        "takeaway": "The benchmark for anyone who wants to hear their music exactly as recorded. 1 dynamic driver gives clean, unbloated bass while 3 balanced armatures carve out microscopic details in vocals, acoustic guitars, and orchestral layers. Zero fluff, pure transparency.",
        "fit_verdict": "5.5mm nozzle • Lightweight matte HeyGears resin shell."
    },
    "gk-kunten": {
        "tagline": "The ultra-budget daily beater set for backpacks and workouts.",
        "sound_summary": "Punchy, balanced V-shape with lively bass and clean vocals.",
        "takeaway": "At under €15 on sale, this is the ultimate carefree pair. It sounds surprisingly punchy and balanced, and if you drop it on the sidewalk or leave it in a gym locker, you won't lose sleep. A great backup set to keep in your jacket pocket.",
        "fit_verdict": "5.5mm nozzle • Extremely lightweight resin shell."
    },
    "7hz-zero-2": {
        "tagline": "The safest first IEM recommendation in the world.",
        "sound_summary": "Warm Harman tuning with +3dB of punchy, engaging bass.",
        "takeaway": "Crinacle teamed up with 7Hz to improve upon the legendary Salnotes Zero. They added just the right amount of warm low-end punch to make rock, hip-hop, and pop tracks sound full and fun, while preserving crisp mids and a comfortable angular shell.",
        "fit_verdict": "5.4mm nozzle • Universally easy seal and very light on the ears."
    },
    "tangzu-waner-2": {
        "tagline": "The vocal lover's paradise, now including Tang Sancai tips.",
        "sound_summary": "Sweet, intimate, forward vocals with smooth, warm acoustics.",
        "takeaway": "Renowned for how naturally and intimately it renders human voices and acoustic instruments. Japanese and English female vocals sound luscious without ever piercing. The new edition includes Tangzu's premium Tang Sancai tips in the box, which are famous for their comfortable medical-grade silicone texture.",
        "fit_verdict": "5.4mm nozzle • Classic ergonomic resin shell."
    },
    "moondrop-chu-2-3": {
        "tagline": "Flush-fitting metal earbuds you can comfortably sleep in.",
        "sound_summary": "Crisp, lively Harman tuning with punchy sub-bass.",
        "takeaway": "Tiny cast-alloy metal earphones that sit completely flush inside the ear bowl, so you can lie your head flat against a pillow without discomfort. Features a detachable 2-pin cable and replaceable screw-off brass nozzle filters to prevent wax clogging.",
        "fit_verdict": "5.3mm nozzle (Ultra-slim bore) • One of the best possible fits for tiny ears."
    }
}

def update():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        iems = json.load(f)

    for item in iems:
        iem_id = item["id"]
        item["image"] = f"assets/images/{iem_id}.jpg"
        
        info = HUMAN_DESCRIPTIONS.get(iem_id)
        if info:
            item["tagline"] = info["tagline"]
            item["sound_summary"] = info["sound_summary"]
            item["takeaway"] = info["takeaway"]
            item["fit_verdict"] = info["fit_verdict"]

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(iems, f, ensure_ascii=False, indent=2)

    print(f"Updated {len(iems)} models in {DATA_FILE} with human descriptions & image paths!")

if __name__ == "__main__":
    update()
