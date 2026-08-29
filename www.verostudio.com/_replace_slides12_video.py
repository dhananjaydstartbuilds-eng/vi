"""Replace slides 1 and 2 images with videos in vero/index.html."""
from __future__ import annotations

import re
from pathlib import Path

HTML = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
POSTER = "/videos/hero-bg-poster.jpg"

SLIDES = {
    "Your dress": {
        "src": "/videos/slide-1.mp4",
        "label": "Abstract motion background",
        "width": 2887,
        "height": 1800,
        "desktop_hash": "cfe716ebeb9d1a0676a59f41aa92b2e678dce13c-2887x1800.jpg",
        "mobile_hash": "86f18c27c5853ee326c8418f1e8e97911092056d-1417x1999.jpg",
        "mobile_width": 1417,
        "mobile_height": 1999,
    },
    "From data": {
        "src": "/videos/slide-2.mp4",
        "label": "Blue glass background",
        "width": 1843,
        "height": 1003,
        "desktop_hash": "457833e548c061d08e21f99cae765b488c1489b1-1843x1003.jpg",
        "mobile_hash": "7fe6426b99b805680fdde5f94132ac75697ea425-1286x2000.jpg",
        "mobile_width": 1286,
        "mobile_height": 2000,
    },
}


def video_tag(alt: str, variant: str, src: str, label: str) -> str:
    return (
        f'<video playsInline="" autoPlay="" muted="" loop="" '
        f'class="Media-module-scss-module__lFYlva__{variant} '
        f'FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
        f'preload="metadata" src="{src}" aria-label="{label}"></video>'
    )


def replace_ssr_imgs(text: str) -> str:
    img_pattern = re.compile(
        r'<img alt="(?P<alt>Your dress|From data)" loading="lazy" decoding="async" data-nimg="1" '
        r'class="Media-module-scss-module__lFYlva__(?P<variant>desktop|mobile) '
        r'FullSizeScrollerStepper-module-scss-module__K-7siW__media" '
        r'style="color:transparent" sizes="100.00vw" src="[^"]*"/>'
    )
    seen: dict[str, set[str]] = {alt: set() for alt in SLIDES}

    def repl(match: re.Match[str]) -> str:
        alt = match.group("alt")
        variant = match.group("variant")
        if variant in seen[alt]:
            return match.group(0)
        seen[alt].add(variant)
        info = SLIDES[alt]
        return video_tag(alt, variant, info["src"], info["label"])

    updated, count = img_pattern.subn(repl, text)
    if count != 4:
        raise RuntimeError(f"Expected 4 SSR img replacements, got {count}")
    return updated


def replace_rsc_blocks(text: str) -> str:
    for alt, info in SLIDES.items():
        old = (
            '{\\"media\\":{\\"type\\":\\"image\\",\\"desktop\\":{\\"src\\":\\"/sanity-cdn/images/xei5vqg0/production/'
            + info["desktop_hash"]
            + '\\",\\"alt\\":\\"'
            + alt
            + '\\",\\"width\\":'
            + str(info["width"])
            + ',\\"height\\":'
            + str(info["height"])
            + '},\\"mobile\\":{\\"src\\":\\"/sanity-cdn/images/xei5vqg0/production/'
            + info["mobile_hash"]
            + '\\",\\"alt\\":\\"'
            + alt
            + '\\",\\"width\\":'
            + str(info["mobile_width"])
            + ',\\"height\\":'
            + str(info["mobile_height"])
            + "}}"
        )
        new = (
            '{\\"media\\":{\\"type\\":\\"video\\",\\"fallback\\":{\\"src\\":\\"'
            + POSTER
            + '\\",\\"alt\\":\\"'
            + alt
            + '\\",\\"width\\":'
            + str(info["width"])
            + ',\\"height\\":'
            + str(info["height"])
            + '},\\"desktop\\":{\\"src\\":\\"'
            + info["src"]
            + '\\",\\"aria-label\\":\\"'
            + info["label"]
            + '\\"},\\"mobile\\":{\\"src\\":\\"'
            + info["src"]
            + '\\",\\"aria-label\\":\\"'
            + info["label"]
            + '\\"}}'
        )
        if old not in text:
            raise RuntimeError(f"RSC block not found for {alt}")
        text = text.replace(old, new, 1)
    return text


def main() -> None:
    text = HTML.read_text(encoding="utf-8", errors="ignore")
    text = replace_ssr_imgs(text)
    text = replace_rsc_blocks(text)
    HTML.write_text(text, encoding="utf-8")
    print(
        {
            "slide1_video": text.count("/videos/slide-1.mp4"),
            "slide2_video": text.count("/videos/slide-2.mp4"),
            "slide1_img": len(re.findall(r'FullSizeScrollerStepper[^>]*img[^>]*Your dress', text)),
            "rsc_video_blocks": text.count('\\"type\\":\\"video\\"'),
        }
    )


if __name__ == "__main__":
    main()
