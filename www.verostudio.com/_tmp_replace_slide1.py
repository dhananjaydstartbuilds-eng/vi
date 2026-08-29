import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "www.verostudio.com"
NEW_IMAGE = "/images/hero-photo.jpg"
NEW_ALT = "Gaming setup"

DESKTOP_PATTERN = re.compile(
    r"/sanity-cdn/images/xei5vqg0/production/"
    r"cfe716ebeb9d1a0676a59f41aa92b2e678dce13c-2887x1800\.jpg"
    r"(?:\?[^\"'\s>]*)?"
)
MOBILE_PATTERN = re.compile(
    r"/sanity-cdn/images/xei5vqg0/production/"
    r"86f18c27c5853ee326c8418f1e8e97911092056d-1417x1999\.jpg"
    r"(?:\?[^\"'\s>]*)?"
)


def patch_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    text = DESKTOP_PATTERN.sub(NEW_IMAGE, text)
    text = MOBILE_PATTERN.sub(NEW_IMAGE, text)

    # Slide 1 SSR imgs use this alt twice (desktop + mobile).
    text = text.replace('alt="Your dress"', f'alt="{NEW_ALT}"', 2)
    text = text.replace('"alt":"Your dress"', f'"alt":"{NEW_ALT}"')

    if text == original:
        return {"path": str(path), "changed": False}

    path.write_text(text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": True,
        "old_desktop_remaining": len(DESKTOP_PATTERN.findall(text)),
        "old_mobile_remaining": len(MOBILE_PATTERN.findall(text)),
        "new_image_count": text.count(NEW_IMAGE),
    }


targets = [ROOT / "index.html", ROOT / "vero" / "index.html"]
for target in targets:
    if target.exists():
        print(patch_file(target))
    else:
        print({"path": str(target), "exists": False})
