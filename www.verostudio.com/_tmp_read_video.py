from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/07v-6l5j-yxf_.js"
).read_text(encoding="utf-8", errors="ignore")

idx = js.find('e.s(["Video"')
print(f"Video @ {idx}")
if idx >= 0:
    print(js[idx : idx + 1200])

# find Video in other chunks
for name in ["0h~h~4-em9w7g.js", "456208"]:
    pass
