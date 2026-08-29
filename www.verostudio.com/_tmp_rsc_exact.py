from pathlib import Path

html = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html"
).read_text(encoding="utf-8", errors="ignore")

needle = '{\\"media\\":{\\"type\\":\\"image\\"'
idx = html.find(needle)
while idx >= 0:
    chunk = html[idx : idx + 450]
    if "To sculpture" in chunk:
        print("FOUND:")
        print(repr(chunk))
        break
    idx = html.find(needle, idx + 1)
