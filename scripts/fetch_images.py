#!/usr/bin/env python3
"""
Fetch official/clean product photos for all 21 IEM models using Brave Images API
Saves them locally to assets/images/<id>.jpg
"""
import os
import sys
import json
import time
import requests
from PIL import Image
import io

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "iems.json")
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
os.makedirs(IMG_DIR, exist_ok=True)

API_KEY = os.environ.get("BRAVE_SEARCH_API_KEY")
if not API_KEY:
    print("Error: BRAVE_SEARCH_API_KEY not found in environment.")
    sys.exit(1)

SEARCH_QUERIES = {
    "tanchjim-bunny": "Tanchjim Bunny earphone IEM product",
    "kefine-klean": "Kefine Klean IEM earphone",
    "trn-conch": "TRN Conch DLC in ear monitor",
    "dunu-titan-x": "DUNU Titan S2 in ear monitor",
    "kz-zar": "KZ ZAR 1DD 7BA IEM earphones",
    "kiwi-ears-cadenza": "Kiwi Ears Cadenza IEM earphones",
    "ooopusx-op22": "ooopusX Op.22 IEM earphone",
    "truthear-gate": "Truthear Gate IEM earphones",
    "7hz-g1": "7Hz G1 IEM Salnotes earphone",
    "7hz-elua-ultra": "7Hz Elua Ultra dual dynamic IEM",
    "tripowin-vivace": "Tripowin Vivace titanium diaphragm IEM",
    "truthear-zero-red": "Truthear Zero Red Crinacle IEM earphones",
    "truthear-zero-blue": "Truthear Zero Blue dual dynamic IEM earphones",
    "kefine-delci-ae": "Kefine Delci AE in-ear monitor",
    "moondrop-may": "Moondrop May dynamic planar DSP IEM",
    "moondrop-aria-2": "Moondrop Aria 2 IEM earphones",
    "truthear-hexa": "Truthear Hexa 1DD 3BA hybrid IEM",
    "gk-kunten": "GK Kunten IEM dynamic earphone",
    "7hz-zero-2": "7Hz Zero 2 Crinacle IEM earphones",
    "tangzu-waner-2": "Tangzu Waner SG earphone IEM",
    "moondrop-chu-2": "Moondrop Chu II Chu 2 IEM earphones"
}

headers = {
    "Accept": "application/json",
    "X-Subscription-Token": API_KEY
}

download_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_and_save(iem_id, query):
    out_path = os.path.join(IMG_DIR, f"{iem_id}.jpg")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"[{iem_id}] Already exists ({os.path.getsize(out_path)} bytes), skipping.")
        return True

    print(f"[{iem_id}] Searching images for: '{query}'...")
    try:
        resp = requests.get(
            "https://api.search.brave.com/res/v1/images/search",
            headers=headers,
            params={"q": query, "count": 10},
            timeout=10
        )
        if resp.status_code != 200:
            print(f"[{iem_id}] Search failed HTTP {resp.status_code}")
            return False

        data = resp.json()
        results = data.get("results", [])
        if not results:
            print(f"[{iem_id}] No image results found.")
            return False

        for r in results:
            img_url = r.get("properties", {}).get("url")
            if not img_url:
                continue
            
            # Skip unpromising links
            if any(bad in img_url.lower() for bad in ["ytimg.com", "avatar", "logo", "icon"]):
                continue

            try:
                img_resp = requests.get(img_url, headers=download_headers, timeout=12)
                if img_resp.status_code == 200 and len(img_resp.content) > 8000:
                    img = Image.open(io.BytesIO(img_resp.content))
                    # Convert to RGB and resize nicely if too large
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                    img.save(out_path, "JPEG", quality=88, optimize=True)
                    print(f"[{iem_id}] Successfully saved: {out_path} ({os.path.getsize(out_path):,} bytes, {img.size}) from {img_url[:60]}...")
                    return True
            except Exception as e:
                # try next image
                continue

        # If full res failed, try thumbnail
        for r in results:
            thumb_url = r.get("thumbnail", {}).get("src")
            if thumb_url:
                try:
                    img_resp = requests.get(thumb_url, headers=download_headers, timeout=10)
                    if img_resp.status_code == 200 and len(img_resp.content) > 3000:
                        img = Image.open(io.BytesIO(img_resp.content))
                        img = img.convert("RGB")
                        img.save(out_path, "JPEG", quality=90)
                        print(f"[{iem_id}] Saved thumbnail fallback: {out_path} ({os.path.getsize(out_path):,} bytes)")
                        return True
                except Exception:
                    pass

        print(f"[{iem_id}] Could not download valid image.")
        return False
    except Exception as e:
        print(f"[{iem_id}] Exception: {e}")
        return False

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        iems = json.load(f)

    success_count = 0
    for item in iems:
        iem_id = item["id"]
        q = SEARCH_QUERIES.get(iem_id, f"{item['brand']} {item['name']} IEM earphone")
        if fetch_and_save(iem_id, q):
            success_count += 1
        time.sleep(1.0) # Respect API rate limits

    print(f"\nFinished: {success_count}/{len(iems)} images downloaded.")

if __name__ == "__main__":
    main()
