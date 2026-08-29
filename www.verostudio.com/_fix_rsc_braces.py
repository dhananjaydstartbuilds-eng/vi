from pathlib import Path

p = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
t = p.read_text(encoding="utf-8")

fixes = [
    (
        'Abstract motion background\\"}}},\\"text\\"',
        'Abstract motion background\\"}},\\"text\\"',
    ),
    (
        'Blue glass background\\"}}},\\"text\\"',
        'Blue glass background\\"}},\\"text\\"',
    ),
]

for old, new in fixes:
    count = t.count(old)
    print(f"count={count} for {old[:50]}")
    if count != 1:
        raise SystemExit(f"expected 1 occurrence, got {count}")
    t = t.replace(old, new)

p.write_text(t, encoding="utf-8")
print("fixed RSC braces for slides 1 and 2")
