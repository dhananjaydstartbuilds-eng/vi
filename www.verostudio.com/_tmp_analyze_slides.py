import re
from pathlib import Path

p = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html")
html = p.read_text(encoding="utf-8", errors="ignore")

for alt in ["Your dress", "From data", "To sculpture"]:
    idx = html.find(f'alt="{alt}"')
    print(f"=== {alt} @ {idx} ===")
    if idx >= 0:
        print(html[idx : idx + 900])
        print()

hashes = [
    "cfe716ebeb9d1a0676a59f41aa92b2e678dce13c",
    "86f18c27c5853ee326c8418f1e8e97911092056d",
    "62dddffa9563718a6437deb91cb2a91ceb0e01f2",
    "396f260c54896295fa31fe6985dd256a8da113e5",
]
for h in hashes:
    print(f"{h}: {html.count(h)}")

# find slide2 alt From data context
idx = html.find("From data")
if idx >= 0:
    print("\n=== From data context ===")
    print(html[max(0, idx - 200) : idx + 600])

# RSC media blocks for scroller
for m in re.finditer(r'"alt":"(Your dress|From data|To sculpture)"', html):
    start = max(0, m.start() - 300)
    end = min(len(html), m.end() + 400)
    print(f"\n=== RSC {m.group(1)} @ {m.start()} ===")
    print(html[start:end])
