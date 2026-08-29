import re
from pathlib import Path

p = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html")
html = p.read_text(encoding="utf-8", errors="ignore")

# slide2 mobile hash
idx = html.find('alt="From data"', html.find('alt="From data"') + 1)
print("=== From data mobile ===")
print(html[idx:idx+500])

# slide1 mobile
idx = html.find('alt="Your dress"', html.find('alt="Your dress"') + 1)
print("\n=== Your dress mobile ===")
print(html[idx:idx+400])

# slide3 mobile
idx = html.find('alt="To sculpture"', html.find('alt="To sculpture"') + 1)
print("\n=== To sculpture mobile ===")
print(html[idx:idx+400])

# RSC blocks - find scroller items array
for pat in [
    r'"alt":"Your dress"[^}]{0,800}',
    r'"alt":"From data"[^}]{0,800}',
    r'"alt":"To sculpture"[^}]{0,800}',
]:
    for m in re.finditer(pat, html):
        print(f"\n=== RSC match @ {m.start()} ===")
        print(m.group(0)[:800])

# MainHero video RSC pattern
idx = html.find('"type":"video"')
print(f"\n=== First video type @ {idx} ===")
print(html[idx:idx+600])

# Count slide2 hash
print("\n457833e548c061d08e21f99cae765b488c1489b1:", html.count("457833e548c061d08e21f99cae765b488c1489b1"))
# find mobile for slide2
m = re.search(r'457833e548c061d08e21f99cae765b488c1489b1[^"]*".*?"From data".*?86f18c27', html)
# search for second From data hash in RSC
parts = html.split('"alt":"From data"')
print("From data occurrences:", len(parts)-1)
for i, part in enumerate(parts[1:3]):
    print(f"\n--- RSC From data chunk {i+1} ---")
    print(part[:500])
