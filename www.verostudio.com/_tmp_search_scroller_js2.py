from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/052uyh96p_mzs.js"
).read_text(encoding="utf-8", errors="ignore")

# Find FullSizeScroller component body - search for masks or items
for term in ["masks", "items.map", "MediaResponsive", "e.media", "media.type"]:
    idx = js.find(term)
    while idx >= 0:
        ctx = js[max(0, idx - 80) : idx + 500]
        if "Scroller" in ctx or "K-7siW" in ctx or "Stepper" in ctx:
            print(f"\n=== {term} @ {idx} ===")
            print(ctx)
            break
        idx = js.find(term, idx + 1)

# broader search - find where Image is used with K-7siW media class
idx = 0
while True:
    i = js.find("K-7siW", idx)
    if i < 0:
        break
    ctx = js[max(0, i - 200) : i + 600]
    if "Image" in ctx or "video" in ctx or "Media" in ctx:
        print(f"\n=== K-7siW context @ {i} ===")
        print(ctx)
    idx = i + 1
