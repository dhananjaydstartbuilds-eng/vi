"""Inject /vero boot script and ensure RSC brace fix for Vercel."""
from pathlib import Path

HTML = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
BOOT = (
    '<script>(function(){var p=location.pathname;if(p==="/vero"||p==="/vero/"){'
    'history.replaceState(null,"","/"+location.search+location.hash);}})();</script>'
)

text = HTML.read_text(encoding="utf-8-sig")

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
    if old in text:
        text = text.replace(old, new)
        print(f"fixed RSC braces: {old[:40]}...")

if BOOT not in text:
    if text.startswith("<!DOCTYPE html>"):
        text = text.replace("<!DOCTYPE html>", "<!DOCTYPE html>" + BOOT, 1)
        print("injected boot script after DOCTYPE")
    else:
        text = BOOT + text
        print("injected boot script at file start")
else:
    print("boot script already present")

HTML.write_text(text, encoding="utf-8")
print("done")
