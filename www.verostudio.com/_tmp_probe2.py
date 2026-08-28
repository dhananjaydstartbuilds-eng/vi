import re

html = open(r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\index.html", encoding="utf-8").read()

# Extract the FullSizeScrollerStepper section
m = re.search(
    r'<div data-type="full-size-scroller-stepper">.*?</div></div></section></div>',
    html,
    re.DOTALL,
)
if not m:
    # try broader
    start = html.find('data-type="full-size-scroller-stepper"')
    print("start", start)
    chunk = html[start : start + 12000]
else:
    chunk = m.group(0)
    print("matched len", len(chunk))

# Pretty-ish: insert newlines before tags for readability of structure
pretty = re.sub(r"><", ">\n<", chunk)
# Keep only structural lines + style attrs of interest
for line in pretty.split("\n"):
    if any(
        k in line
        for k in [
            "FullSizeScroller",
            "Parallax",
            "mask-progress",
            "parallax-",
            "Beacon",
            "img ",
            "masks",
            "sticky",
            "Bullet",
            "is-active",
            "overflow",
            "--active",
            "id=",
        ]
    ):
        # truncate long lines
        s = line if len(line) < 350 else line[:330] + "..."
        print(s)

print("\n\n=== PARALLAX CSS ===")
css = open(
    r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks\0b.y.basln~dj.css",
    encoding="utf-8",
).read()
parts = re.findall(r"[^}]*Parallax-module[^}]*\}", css)
for p in parts:
    print(p.strip() + "}")
    print("---")
