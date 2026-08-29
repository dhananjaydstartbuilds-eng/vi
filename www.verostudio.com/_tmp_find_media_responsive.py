from pathlib import Path

# Find MediaResponsive in chunks
base = Path(r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks")
for p in base.glob("*.js"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "MediaResponsive" in text and "function" in text:
        idx = text.find('e.s(["MediaResponsive"')
        if idx < 0:
            idx = text.find("MediaResponsive", 0)
            # find export
            idx2 = text.find('e.s(["MediaResponsive"', idx)
            if idx2 >= 0:
                idx = idx2
        if idx >= 0:
            print(f"\n=== {p.name} @ {idx} ===")
            print(text[idx : idx + 2000])
            break
