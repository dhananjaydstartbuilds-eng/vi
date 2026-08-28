import os, re

chunks = r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks"
needles = [
    "mask-progress",
    "maskProgress",
    "--mask-progress",
    "parallax-width",
    "parallaxWidth",
    "FullSizeScrollerStepper",
    "setProperty",
]
# Search js files for mask-progress context
for fn in os.listdir(chunks):
    if not fn.endswith(".js"):
        continue
    path = os.path.join(chunks, fn)
    try:
        data = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    if "mask-progress" in data or "FullSizeScrollerStepper" in data:
        print("FILE", fn, "size", len(data))
        for n in ["mask-progress", "FullSizeScroller", "parallax-width", "Mask"]:
            if n in data:
                print("  has", n, "count", data.count(n))
        # show contexts around mask-progress
        for m in re.finditer(r".{0,60}mask-progress.{0,80}", data):
            print("  CTX:", m.group().replace("\n", " ")[:200])
        for m in re.finditer(r".{0,40}FullSizeScrollerStepper.{0,60}", data):
            print("  FS:", m.group().replace("\n", " ")[:160])
            break
