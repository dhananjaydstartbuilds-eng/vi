from pathlib import Path

p = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
t = p.read_text(encoding="utf-8")
for idx in (110266, 110874, 111570):
    print(repr(t[idx : idx + 90]))
