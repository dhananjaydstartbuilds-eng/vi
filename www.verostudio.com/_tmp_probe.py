import re, urllib.request

html_path = r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com\index.html"
html = open(html_path, encoding="utf-8").read()

print("unblock-slides:", "unblock-slides" in html)
print("6lubt4tb count:", html.count("6lubt4tb"))
print("FullSizeScroller count:", html.count("FullSizeScroller"))

# Extract RSC payload chunks that mention FullSizeScroller or mask
for pat in ["FullSizeScroller", "6lubt4tb", "mask-progress", "parallax-width"]:
    idxs = [m.start() for m in re.finditer(re.escape(pat), html)]
    print(pat, "hits", len(idxs))
    for i in idxs[:5]:
        print(" ", html[max(0, i - 80) : i + 120].replace("\n", " ")[:200])
        print("  ---")

# Served CSS check
url = "http://127.0.0.1:8080/_next/static/chunks/0b.y.basln~dj.css?dpl=dpl_5DJLEfML6Tahb8bYNMHiKG68mpNy&v=unblock-slides"
try:
    css = urllib.request.urlopen(url, timeout=5).read().decode("utf-8", "replace")
    print("SERVED override:", "#_R_6lubt4tb_-1,#_R_6lubt4tb_-2{--mask-progress:1!important}" in css)
    print("SERVED len", len(css), "tail:", css[-120:])
except Exception as e:
    print("SERVE ERR", e)
