"""Replace FullSizeScrollerStepper slides 1-3 media in vero/index.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"

SLIDE1 = "/images/slide-1.avif"
SLIDE2 = "/images/slide-2.jpg"
SLIDE3 = "/videos/slide-3.mp4"
SLIDE3_POSTER = "/videos/hero-bg-poster.jpg"

SLIDE1_HASHES = (
    "cfe716ebeb9d1a0676a59f41aa92b2e678dce13c-2887x1800.jpg",
    "86f18c27c5853ee326c8418f1e8e97911092056d-1417x1999.jpg",
)
SLIDE2_HASHES = (
    "457833e548c061d08e21f99cae765b488c1489b1-1843x1003.jpg",
    "7fe6426b99b805680fdde5f94132ac75697ea425-1286x2000.jpg",
)

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


def replace_hash_urls(text: str, hash_name: str, new_path: str) -> str:
    pattern = re.compile(
        rf"/sanity-cdn/images/xei5vqg0/production/{re.escape(hash_name)}(?:\?[^\"'\s>]*)?"
    )
    return pattern.sub(new_path, text)


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


def patch() -> dict:
    text = ROOT.read_text(encoding="utf-8", errors="ignore")
    original = text

    for h in SLIDE1_HASHES:
        text = replace_hash_urls(text, h, SLIDE1)
    for h in SLIDE2_HASHES:
        text = replace_hash_urls(text, h, SLIDE2)

    if RSC_SLIDE3_OLD not in text:
        raise RuntimeError("Slide 3 RSC block not found")
    text = text.replace(RSC_SLIDE3_OLD, RSC_SLIDE3_NEW, 1)

    text = replace_slide3_imgs(text)

    if text == original:
        raise RuntimeError("No changes applied")

    ROOT.write_text(text, encoding="utf-8")

    return {
        "slide1_count": text.count(SLIDE1),
        "slide2_count": text.count(SLIDE2),
        "slide3_count": text.count(SLIDE3),
        "rsc_video": '\\"type\\":\\"video\\"' in text[text.find(RSC_SLIDE3_NEW[:40]) : text.find(RSC_SLIDE3_NEW[:40]) + 500]
        if RSC_SLIDE3_NEW[:40] in text
        else False,
        "slide3_desktop_video": VIDEO_DESKTOP in text,
        "slide3_mobile_video": VIDEO_MOBILE in text,
        "old_slide1_hash_remaining": text.count(SLIDE1_HASHES[0]),
        "old_slide2_hash_remaining": text.count(SLIDE2_HASHES[0]),
        "old_slide3_hash_remaining": text.count("62dddffa9563718a6437deb91cb2a91ceb0e01f2"),
    }


if __name__ == "__main__":
    print(patch())
