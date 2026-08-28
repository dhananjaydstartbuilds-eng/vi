import json
import pathlib
import re
import shutil

WORK = pathlib.Path(r"d:\Node\personal\3d\_msdf_work")
LOGO_DIR = pathlib.Path(
    r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\webgl\logo"
)
CHUNKS = pathlib.Path(
    r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks"
)

src = json.loads((WORK / "LouizeDisplay.json").read_text(encoding="utf-8"))
src["pages"] = ["font.png"]
font_json = json.dumps(src, indent=4) + "\n"
(LOGO_DIR / "font.json").write_text(font_json, encoding="utf-8")
shutil.copy2(WORK / "LouizeDisplay.png", LOGO_DIR / "font.png")

by_char = {c["char"]: c for c in src["chars"]}
order = ["V", "I", "C", "K", "Y"]
pad = src["info"]["padding"][0]

v_inner_h = by_char["V"]["height"] - 2 * pad
scale = 87.23 / v_inner_h
min_yoffset = min(by_char[ch]["yoffset"] for ch in order)

cursor = 0.0
layout = []
for i, ch in enumerate(order):
    c = by_char[ch]
    inner_w = c["width"] - 2 * pad
    inner_h = c["height"] - 2 * pad
    width = inner_w * scale
    height = inner_h * scale
    y = (c["yoffset"] - min_yoffset) * scale
    layout.append(
        {
            "id": i,
            "char": ch,
            "x": round(cursor, 2),
            "y": round(y, 2),
            "width": round(width, 2),
            "height": round(height, 2),
        }
    )
    cursor += c["xadvance"] * scale

layout_js = "let o=[" + ",".join(
    '{id:%d,char:"%s",x:%s,y:%s,width:%s,height:%s}' % (
        item["id"],
        item["char"],
        f'{item["x"]:.2f}'.rstrip("0").rstrip("."),
        f'{item["y"]:.2f}'.rstrip("0").rstrip("."),
        f'{item["width"]:.2f}'.rstrip("0").rstrip("."),
        f'{item["height"]:.2f}'.rstrip("0").rstrip("."),
    )
    for item in layout
) + "];"

print("layout:", layout_js)

chunk_names = [
    "11sswtocfulc~.js",
    "11sswtocfulc.js",
    "0~yq2b2d3iy8i.js",
]
patched = 0
for name in chunk_names:
    path = CHUNKS / name
    if not path.exists():
        print("missing", name)
        continue
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(r"let o=\[[^\]]+\];", layout_js, text, count=1)
    if count:
        path.write_text(new_text, encoding="utf-8")
        patched += 1
        print("patched", name)

alias_src = CHUNKS / "0ejpr-b5t07-.js"
alias_dst = CHUNKS / "0ejpr-~b5t07-.js"
if alias_src.exists():
    shutil.copy2(alias_src, alias_dst)
    print("alias chunk ok")

print("done", patched, "chunks")
