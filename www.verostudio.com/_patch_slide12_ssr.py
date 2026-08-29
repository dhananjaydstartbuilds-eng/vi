"""Patch SSR scroller imgs for slides 1 and 2 to use local paths."""
from __future__ import annotations

import re
from pathlib import Path

HTML = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"

SLIDE1 = "/images/slide-1.jpg"
SLIDE2 = "/images/slide-2.jpg"

IMG_PATTERN = re.compile(
    r'<img alt="(?P<alt>Your dress|From data)" loading="lazy" width="\d+" height="\d+" '
    r'decoding="async" data-nimg="1" '
    r'class="Media-module-scss-module__lFYlva__(?P<variant>desktop|mobile) '
    r'FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
    r'style="color:transparent" sizes="100.00vw" srcSet="[^"]*" src="[^"]*"/>'
)

ALT_TO_SRC = {
    "Your dress": SLIDE1,
    "From data": SLIDE2,
}


def replacement(match: re.Match[str]) -> str:
    alt = match.group("alt")
    variant = match.group("variant")
    src = ALT_TO_SRC[alt]
    return (
        f'<img alt="{alt}" loading="lazy" decoding="async" data-nimg="1" '
        f'class="Media-module-scss-module__lFYlva__{variant} '
        f'FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
        f'style="color:transparent" sizes="100.00vw" src="{src}"/>'
    )


def main() -> None:
    text = HTML.read_text(encoding="utf-8", errors="ignore")
    updated, count = IMG_PATTERN.subn(replacement, text)
    if count != 4:
        raise RuntimeError(f"Expected 4 img replacements, got {count}")
    HTML.write_text(updated, encoding="utf-8")
    print({"replaced": count, "slide1": updated.count(SLIDE1), "slide2": updated.count(SLIDE2)})


if __name__ == "__main__":
    main()
