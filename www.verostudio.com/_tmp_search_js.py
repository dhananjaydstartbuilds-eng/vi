from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/052uyh96p_mzs.js"
).read_text(encoding="utf-8", errors="ignore")

terms = [
    "FullSizeScrollerStepper",
    'type:"video"',
    "type===\\",
    "VideoPlayer",
    "K-7siW",
]
for t in terms:
    idx = js.find(t)
    print(f"{t}: {idx}")
    if idx >= 0 and t == "FullSizeScrollerStepper":
        print(js[idx : idx + 500])

# find video type check near Media
for m in ["video", "image"]:
    pat = f'"{m}"==='
    idx = js.find(pat)
    print(f'"{m}"=== @ {idx}')
    if idx >= 0:
        print(js[max(0, idx - 100) : idx + 300])
