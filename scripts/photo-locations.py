# Read the GPS position and date from the EXIF data of the fieldwork photos
# in public/photos/ and write src/data/photos.json, which puts them on the
# map's "My route, 2026" layer.
#
#   pip install Pillow
#   python scripts/photo-locations.py
#
# Each photo is matched to the nearest visited site in sites.json (within
# 5 km) so it can be listed with that site. Captions already written in
# photos.json are kept when the script is run again. Photos without GPS data
# (iPhone .heic files must be exported as JPEG first, which keeps the
# location) are listed and skipped: place them by hand in photos.json if needed, and
# mark them "placed": "by hand".
import json, math, pathlib, sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "public" / "photos"
OUT = ROOT / "src" / "data" / "photos.json"
SITES = json.loads((ROOT / "src" / "data" / "sites.json").read_text(encoding="utf-8"))

def exif(path):
    img = Image.open(path)
    raw = img.getexif()
    tags = {TAGS.get(k, k): v for k, v in raw.items()}
    gps = {GPSTAGS.get(k, k): v for k, v in raw.get_ifd(0x8825).items()}
    taken = raw.get_ifd(0x8769).get(36867) or tags.get("DateTime")  # DateTimeOriginal
    return gps, taken

def degrees(dms, ref):
    d, m, s = (float(x) for x in dms)
    value = d + m / 60 + s / 3600
    return -value if ref in ("S", "W") else value

def km(a, b):
    lat1, lng1, lat2, lng2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lng2 - lng1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))

old = {p["src"]: p for p in json.loads(OUT.read_text(encoding="utf-8"))} if OUT.exists() else {}
visited = [s for s in SITES if s.get("visited") and s.get("lat") is not None]
photos, skipped = [], []
for path in sorted(PHOTOS.glob("*")):
    if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        continue
    src = f"/photos/{path.name}"
    try:
        gps, taken = exif(path)
        lat = degrees(gps["GPSLatitude"], gps["GPSLatitudeRef"])
        lng = degrees(gps["GPSLongitude"], gps["GPSLongitudeRef"])
    except (KeyError, OSError, ValueError, TypeError):
        if src in old:
            photos.append(old[src])  # placed by hand earlier
        else:
            skipped.append(path.name)
        continue
    near = min(visited, key=lambda s: km((lat, lng), (s["lat"], s["lng"])))
    photos.append({
        "src": src,
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "taken": str(taken).replace(":", "-", 2) if taken else None,
        "site": near["id"] if km((lat, lng), (near["lat"], near["lng"])) <= 5 else None,
        "caption": old.get(src, {}).get("caption"),
    })

OUT.write_text(json.dumps(photos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(photos)} photos written to {OUT.relative_to(ROOT)}")
if skipped:
    print("No GPS data (skipped):", ", ".join(skipped))
