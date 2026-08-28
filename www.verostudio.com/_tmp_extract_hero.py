import re, urllib.request
from pathlib import Path

html = Path(r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\index.html").read_text(encoding="utf-8")

print("=== 1. SSR CAPTION HTML ===")
m = re.search(
    r'<div class="MainHero-module-scss-module__yRwbjq__title"><h1>.*?</h1></div>',
    html,
)
print(m.group(0) if m else "NOT FOUND")

print("\n=== 2. RSC CAPTION (Sanity portable text spans) ===")
idx = html.find('"text":"Custom"')
print(html[idx : idx + 420] if idx >= 0 else "NOT FOUND")

print("\n=== FULL RSC title block ===")
start = html.find('"title":[{"_key":"d457c8aace50"')
if start < 0:
    start = html.find('\\"title\\":[{\\"_key\\":\\"d457c8aace50\\"')
print("start", start)
if start >= 0:
    snippet = html[start : start + 650]
    print(snippet)

print("\n=== 4. LIVE vs LOCAL letter layout ===")
local = Path(
    r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks\0~yq2b2d3iy8i.js"
).read_text(encoding="utf-8", errors="ignore")
li = local.find("let o=[")
print("LOCAL:", local[li : li + 280])

try:
    live = urllib.request.urlopen(
        "https://www.verostudio.com/_next/static/chunks/0~yq2b2d3iy8i.js?dpl=dpl_5DJLEfML6Tahb8bYNMHiKG68mpNy",
        timeout=20,
    ).read().decode("utf-8", "replace")
    lj = live.find("let o=[")
    print("LIVE:", live[lj : lj + 280] if lj >= 0 else "NO let o= in live chunk")
except Exception as e:
    print("LIVE fetch error:", e)

js = Path(
    r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks\052uyh96p_mzs.js"
).read_text(encoding="utf-8", errors="ignore")
mi = js.find('name:"LogoScene"')
print("\n=== 5. MainHero WebGLView in 052uyh96p_mzs.js ===")
print(js[mi - 200 : mi + 350] if mi >= 0 else "NOT FOUND")
