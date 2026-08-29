import re
from pathlib import Path

p = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html")
html = p.read_text(encoding="utf-8", errors="ignore")

# Extract full img tags for To sculpture
for m in re.finditer(r'<img alt="To sculpture"[^>]*>', html):
    print("=== IMG TAG ===")
    print(m.group(0)[:1200])
    print("len:", len(m.group(0)))

# RSC - search escaped alt
for term in ["Your dress", "From data", "To sculpture"]:
    esc = term.replace('"', '\\"')
    for pat in [f'\\"alt\\":\\"{term}\\"', f'"alt":"{term}"']:
        idx = html.find(pat)
        print(f"\n{term} RSC pattern {pat[:30]} @ {idx}")
        if idx >= 0:
            print(html[idx:idx+500])

# video in RSC
for pat in ['\\"type\\":\\"video\\"', '"type":"video"']:
    idx = 0
    count = 0
    while True:
        i = html.find(pat, idx)
        if i < 0:
            break
        count += 1
        if count <= 2:
            print(f"\n=== video RSC @ {i} ===")
            print(html[i:i+700])
        idx = i + 1
    print(f"Total {pat}: {count}")

# scroller items in RSC - find 62dddffa block
idx = html.find("62dddffa9563718a6437deb91cb2a91ceb0e01f2")
print(f"\n=== slide3 hash context ===")
print(html[max(0,idx-200):idx+400])
