"""Swap SSR slide 1/2 img src paths in vero/index.html."""
import re
from pathlib import Path

HTML = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"

text = HTML.read_text(encoding="utf-8", errors="ignore")

text = re.sub(
    r'(<img alt="Your dress"[^>]*src=")/images/slide-1\.jpg(")',
    r"\1/images/slide-2.jpg\2",
    text,
)
text = re.sub(
    r'(<img alt="From data"[^>]*src=")/images/slide-2\.jpg(")',
    r"\1/images/slide-1.jpg\2",
    text,
)

HTML.write_text(text, encoding="utf-8")

dress = re.findall(r'alt="Your dress"[^>]*src="([^"]+)"', text)
data = re.findall(r'alt="From data"[^>]*src="([^"]+)"', text)
print({"dress": dress, "data": data})
