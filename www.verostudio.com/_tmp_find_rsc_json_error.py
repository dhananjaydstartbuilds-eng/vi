"""Find malformed JSON in vero RSC payload."""
from pathlib import Path
import re
import json

html = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
text = html.read_text(encoding="utf-8", errors="ignore")

for i, m in enumerate(re.finditer(r'self\.__next_f\.push\(\[1,"(.+?)"\]\)', text, re.DOTALL)):
    payload = m.group(1)
    decoded = payload.encode("utf-8").decode("unicode_escape")

    for alt in ("Your dress", "From data", "To sculpture"):
        idx = decoded.find(alt)
        if idx >= 0:
            snippet = decoded[max(0, idx - 250) : idx + 450]
            print(f"\n=== chunk {i} alt={alt} ===")
            print(snippet)

    # slide 3 reference block
    if "To sculpture" in decoded and "type" in decoded:
        for match in re.finditer(r'\{"media":\{[^\}]+type[^\}]+\}[^\}]*\}[^\}]*\}', decoded):
            if "To sculpture" in match.group(0) or "Your dress" in match.group(0):
                block = match.group(0)
                print(f"\nmedia block chunk {i}:")
                print(block[:500])
