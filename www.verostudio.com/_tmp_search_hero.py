import os, re, json
from pathlib import Path

base = Path(r"d:\Node\personal\3d\www.verostudio.com\www.verostudio.com")

def search_file(path, patterns, regex_patterns=None, ctx=250):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"ERR read {path}: {e}")
        return
    for p in patterns:
        idx = 0
        while True:
            i = text.lower().find(p.lower(), idx)
            if i < 0:
                break
            start = max(0, i - ctx)
            end = min(len(text), i + len(p) + ctx)
            print(f"\n=== {path} | {p} @ {i} ===")
            print(text[start:end])
            idx = i + 1
    if regex_patterns:
        for rp in regex_patterns:
            for m in re.finditer(rp, text, re.DOTALL):
                start = max(0, m.start() - ctx)
                end = min(len(text), m.end() + ctx)
                print(f"\n=== {path} | REGEX {rp[:40]} @ {m.start()} ===")
                print(text[start:end])

patterns = [
    "Custom SCULPTURE", "SCULPTURE", "WEDDING DRESS", "wedding dress",
    "Custom", "graphic designer",
    "11sswtocfulc", "052uyh96p", "0~yq2b2d3iy8i",
    'char:"V"', 'char:"E"', 'char:"R"', 'char:"O"',
    'char:"C"', 'char:"K"', 'char:"I"', 'char:"Y"',
    "MSDF", "font.json", "webgl/logo", "LouizeDisplay",
]
regex_patterns = [
    r'id:\s*0,\s*char:\s*"V"',
    r'\[\{id:\d+,char:"[A-Z]"',
    r'char:"V".*char:"E".*char:"R".*char:"O"',
    r'char:"V".*char:"I".*char:"C".*char:"K".*char:"Y"',
]

print("=== index.html ===")
search_file(base / "index.html", patterns, regex_patterns)

print("\n=== hero/index.html ===")
search_file(base / "hero/index.html", patterns, regex_patterns)

chunks = base / "_next/static/chunks"
if chunks.exists():
    for js in sorted(chunks.glob("*.js")):
        text = js.read_text(encoding="utf-8", errors="ignore")
        hits = []
        for p in ['char:"V"', 'char:"E"', 'SCULPTURE', 'WEDDING', '11sswtocfulc', '052uyh96p', '0~yq2b2d3iy8i', 'LouizeDisplay', 'font.json', 'webgl/logo']:
            if p.lower() in text.lower():
                hits.append(p)
        if hits:
            print(f"\n=== CHUNK {js.name} hits: {hits} ===")
            search_file(js, hits, regex_patterns)

html = (base / "index.html").read_text(encoding="utf-8", errors="ignore")
scripts = re.findall(r'src="(/_next/static/chunks/[^"]+)"', html)
print("\n=== script chunks referenced in index.html ===")
for s in scripts:
    name = s.split("/")[-1].split("?")[0]
    local = chunks / name
    print(f"  {name} local={'YES' if local.exists() else 'NO'}")
