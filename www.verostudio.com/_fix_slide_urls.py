"""Fix slide 1/2 to use Sanity URLs (server-aliased) and keep slide 3 video."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "www.verostudio.com" / "vero" / "index.html"
SLIDE3 = "/videos/slide-3.mp4"
SLIDE3_POSTER = "/videos/hero-bg-poster.jpg"

RSC_SLIDE3_OLD = (
    '{\\"media\\":{\\"type\\":\\"image\\",\\"desktop\\":{\\"src\\":\\"/sanity-cdn/images/xei5vqg0/production/'
    '62dddffa9563718a6437deb91cb2a91ceb0e01f2-2975x1800.jpg\\",\\"alt\\":\\"To sculpture\\",\\"width\\":2975,\\"height\\":1800},'
    '\\"mobile\\":{\\"src\\":\\"/sanity-cdn/images/xei5vqg0/production/396f260c54896295fa31fe6985dd256a8da113e5-1521x2000.jpg\\",'
    '\\"alt\\":\\"To sculpture\\",\\"width\\":1521,\\"height\\":2000}}'
)

RSC_SLIDE3_NEW = (
    f'{{\\"media\\":{{\\"type\\":\\"video\\",\\"fallback\\":{{\\"src\\":\\"{SLIDE3_POSTER}\\",'
    f'\\"alt\\":\\"To sculpture\\",\\"width\\":2975,\\"height\\":1800}},'
    f'\\"desktop\\":{{\\"src\\":\\"{SLIDE3}\\",\\"aria-label\\":\\"Retrowave background\\"}},'
    f'\\"mobile\\":{{\\"src\\":\\"{SLIDE3}\\",\\"aria-label\\":\\"Retrowave background\\"}}}}'
)

IMG_TO_SCULPTURE = re.compile(
    r'<img alt="To sculpture" loading="lazy" width="\d+" height="\d+" decoding="async" data-nimg="1" '
    r'class="Media-module-scss-module__lFYlva__(desktop|mobile) FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
    r'style="color:transparent" sizes="100.00vw" srcSet="[^"]*" src="[^"]*"/>'
)

VIDEO_DESKTOP = (
    '<video playsInline="" autoPlay="" muted="" loop="" '
    'class="Media-module-scss-module__lFYlva__desktop FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
    f'preload="metadata" src="{SLIDE3}" aria-label="Retrowave background"></video>'
)
VIDEO_MOBILE = (
    '<video playsInline="" autoPlay="" muted="" loop="" '
    'class="Media-module-scss-module__lFYlva__mobile FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
    f'preload="metadata" src="{SLIDE3}" aria-label="Retrowave background"></video>'
)


def replace_slide3_imgs(text: str) -> str:
    seen = {"desktop": False, "mobile": False}

    def repl(match: re.Match[str]) -> str:
        variant = match.group(1)
        if variant == "desktop" and not seen["desktop"]:
            seen["desktop"] = True
            return VIDEO_DESKTOP
        if variant == "mobile" and not seen["mobile"]:
            seen["mobile"] = True
            return VIDEO_MOBILE
        return match.group(0)

    return IMG_TO_SCULPTURE.sub(repl, text)


def main() -> None:
    original = subprocess.check_output(
        ["git", "show", "HEAD:www.verostudio.com/www.verostudio.com/vero/index.html"],
        cwd=ROOT.parent,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    text = original

    if RSC_SLIDE3_OLD not in text:
        raise RuntimeError("Slide 3 RSC block not found in HEAD version")
    text = text.replace(RSC_SLIDE3_OLD, RSC_SLIDE3_NEW, 1)
    text = replace_slide3_imgs(text)

    HTML.write_text(text, encoding="utf-8")
    print(
        {
            "slide1_local_paths": text.count("/images/slide-1.avif"),
            "slide2_local_paths": text.count("/images/slide-2.jpg"),
            "slide3_video": text.count(SLIDE3),
            "slide1_sanity": text.count("cfe716ebeb9d1a0676a59f41aa92b2e678dce13c"),
            "slide2_sanity": text.count("457833e548c061d08e21f99cae765b488c1489b1"),
            "rsc_video": RSC_SLIDE3_NEW in text,
        }
    )


if __name__ == "__main__":
    main()
