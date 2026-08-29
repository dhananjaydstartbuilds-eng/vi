from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/07v-6l5j-yxf_.js"
).read_text(encoding="utf-8", errors="ignore")

idx = js.find('e.s(["Media"')
print(f"Media @ {idx}")
if idx >= 0:
    print(js[idx : idx + 3000])
