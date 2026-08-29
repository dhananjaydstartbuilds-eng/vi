from pathlib import Path

js = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/_next/static/chunks/052uyh96p_mzs.js"
).read_text(encoding="utf-8", errors="ignore")

idx = js.find('e.s(["FullSizeScrollerStepper"')
print(f"FullSizeScrollerStepper component @ {idx}")
print(js[idx : idx + 3500])
