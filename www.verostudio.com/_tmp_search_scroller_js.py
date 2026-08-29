from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/052uyh96p_mzs.js"
).read_text(encoding="utf-8", errors="ignore")

# Find scroller component render function
for term in ["K-7siW__media", "FullSizeScrollerStepperItem", ".desktop", ".mobile", "fallback"]:
    idx = 0
    hits = 0
    while hits < 3:
        i = js.find(term, idx)
        if i < 0:
            break
        hits += 1
        print(f"\n=== {term} @ {i} ===")
        print(js[max(0, i - 150) : i + 400])
        idx = i + 1

# search media type switch
for pat in ["video", "Image", "Media"]:
    count = js.count(pat)
    print(f"{pat}: {count}")
