"""Inject slide-media-fix.js into vero/index.html if missing."""
from pathlib import Path

HTML = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
TAG = '<script src="/vero/slide-media-fix.js"></script>'

text = HTML.read_text(encoding="utf-8", errors="ignore")
if TAG in text:
    print("already present")
else:
    if "</body>" in text:
        text = text.replace("</body>", TAG + "</body>", 1)
    else:
        text += TAG
    HTML.write_text(text, encoding="utf-8")
    print("injected")
