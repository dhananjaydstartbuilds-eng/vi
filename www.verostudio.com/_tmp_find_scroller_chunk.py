import re
from pathlib import Path

html = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html"
).read_text(encoding="utf-8", errors="ignore")
chunks = re.findall(r"/_next/static/chunks/([^\"?]+\.js)", html)
print("Referenced chunks:", sorted(set(chunks)))

base = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks")
for name in sorted(set(chunks)):
    p = base / name
    if not p.exists():
        print(f"MISSING {name}")
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "FullSizeScroller" in text or "K-7siW" in text:
        idx = text.find("FullSizeScroller")
        print(f"\n=== {name} has FullSizeScroller @ {idx} ===")
        print(text[max(0, idx - 50) : idx + 800])
