import re
from pathlib import Path

p = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html")
html = p.read_text(encoding="utf-8", errors="ignore")

# Full RSC scroller item blocks
for term in ["Your dress", "From data", "To sculpture"]:
    pat = f'{{\\"type\\":\\"image\\",\\"desktop\\":{{\\"src\\":\\"/sanity-cdn/images/xei5vqg0/production/'
    # find the block containing this alt
    idx = html.find(f'\\"alt\\":\\"{term}\\"')
    # walk back to find media block start
    start = html.rfind('{"media":', 0, idx)
    if start < 0:
        start = html.rfind('{\\"media\\":', 0, idx)
    # simpler: find type image near alt
    chunk_start = max(0, idx - 250)
    print(f"\n=== RSC block for {term} ===")
    print(html[chunk_start:idx+350])
