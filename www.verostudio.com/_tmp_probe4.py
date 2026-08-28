import re
path = r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\_next\static\chunks\07v-6l5j-yxf_.js"
data = open(path, encoding="utf-8").read()

# Extract Mask-related module with context
for m in re.finditer(r"mask-progress", data):
    start = max(0, m.start() - 1500)
    end = min(len(data), m.end() + 800)
    chunk = data[start:end]
    print("=" * 80)
    print(chunk)
    print()

# Also parallax-width setting
for m in re.finditer(r"parallax-width", data):
    start = max(0, m.start() - 800)
    end = min(len(data), m.end() + 400)
    print("PW" + "=" * 78)
    print(data[start:end])
