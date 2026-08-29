#!/usr/bin/env python3
"""Apply serve.py Sanity URL patches at Vercel build time."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "www.verostudio.com"

PATCH_REPLACEMENTS = (
    ("https://xei5vqg0.api.sanity.io", "/sanity-api"),
    ("https://api.sanity.io", "/api-sanity"),
    ('"apiHost":"/api-sanity"', '"apiHost":"/sanity-api"'),
    ("'apiHost':'/api-sanity'", "'apiHost':'/sanity-api'"),
    ("https://cdn.sanity.io", "/sanity-cdn"),
)

PATCH_EXTENSIONS = {".html", ".js", ".css", ".mjs", ".json"}


def patch_text(text: str, origin: str) -> str:
    for old, new in PATCH_REPLACEMENTS:
        text = text.replace(old, new)

    text = text.replace('"/api-sanity"', '"/sanity-api"')
    text = text.replace("'/api-sanity'", "'/sanity-api'")
    text = text.replace('\\"/api-sanity\\"', '\\"/sanity-api\\"')
    text = text.replace('apiHost:"/api-sanity"', 'apiHost:"/sanity-api"')
    text = text.replace("apiHost:'/api-sanity'", "apiHost:'/sanity-api'")

    api_host = f"{origin}/sanity-api"
    api_host_patterns = (
        ('"apiHost":"/sanity-api"', f'"apiHost":"{api_host}"'),
        ("'apiHost':'/sanity-api'", f"'apiHost':'{api_host}'"),
        ('\\"apiHost\\":\\"/sanity-api\\"', f'\\"apiHost\\":\\"{api_host}\\"'),
        ('apiHost:"/sanity-api"', f'apiHost:"{api_host}"'),
        ("apiHost:'/sanity-api'", f"apiHost:'{api_host}'"),
        (f'"apiHost":"{origin}/api-sanity"', f'"apiHost":"{api_host}"'),
        (f'\\"apiHost\\":\\"{origin}/api-sanity\\"', f'\\"apiHost\\":\\"{api_host}\\"'),
    )
    for old, new in api_host_patterns:
        text = text.replace(old, new)

    for path in ("/sanity-api", "/ingest", "/sanity-cdn"):
        absolute = f"{origin}{path}"
        text = text.replace(f'"{path}"', f'"{absolute}"')
        text = text.replace(f"'{path}'", f"'{absolute}'")
        text = text.replace(f'\\"{path}\\"', f'\\"{absolute}\\"')

    cdn_prefix = f"{origin}/sanity-cdn/"
    text = text.replace('"/sanity-cdn/', f'"{cdn_prefix}')
    text = text.replace("'/sanity-cdn/", f"'{cdn_prefix}")
    text = text.replace('\\"/sanity-cdn/', f'\\"{cdn_prefix}')

    text = text.replace('api_host:"/ingest"', f'api_host:"{origin}/ingest"')
    text = text.replace('"useProjectHostname":true', '"useProjectHostname":false')
    text = text.replace('\\"useProjectHostname\\":true', '\\"useProjectHostname\\":false')
    text = text.replace("useProjectHostname:!0", "useProjectHostname:!1")
    return text


def main() -> int:
    vercel_url = (
        os.environ.get("VERCEL_PROJECT_PRODUCTION_URL", "").strip()
        or os.environ.get("VERCEL_URL", "").strip()
    )
    if vercel_url:
        origin = f"https://{vercel_url}"
    else:
        origin = os.environ.get("VERCEL_PATCH_ORIGIN", "https://vi-drab.vercel.app")

    targets = [
        SITE / "vero" / "index.html",
        SITE / "_next" / "static",
    ]

    patched = 0
    for target in targets:
        if target.is_file():
            files = [target]
        elif target.is_dir():
            files = [
                p
                for p in target.rglob("*")
                if p.is_file() and p.suffix in PATCH_EXTENSIONS
            ]
        else:
            continue

        for path in files:
            original = path.read_text(encoding="utf-8", errors="ignore")
            updated = patch_text(original, origin)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                patched += 1

    print(f"patch_for_vercel: origin={origin} patched_files={patched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
