import urllib.request

BASE = "http://127.0.0.1:8080"


def fetch(url: str, head: bool = False):
    req = urllib.request.Request(url, method="HEAD" if head else "GET")
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.status, response.headers.get("Content-Type"), response.headers.get("Content-Length")


checks = [
    ("/images/hero-photo.jpg", True),
    (
        "/sanity-cdn/images/xei5vqg0/production/cfe716ebeb9d1a0676a59f41aa92b2e678dce13c-2887x1800.jpg",
        True,
    ),
    ("/vero", False),
]

for path, head in checks:
    try:
        status, ctype, clen = fetch(BASE + path, head=head)
        print(f"{path}: {status} {ctype} len={clen}")
    except Exception as exc:
        print(f"{path}: ERROR {exc}")

html = urllib.request.urlopen(BASE + "/vero", timeout=15).read().decode("utf-8", "replace")
print("hero-photo in /vero html:", html.count("/images/hero-photo.jpg"))
print("old desktop hash in /vero html:", html.count("cfe716ebeb9d1a0676a59f41aa92b2e678dce13c"))
print("Gaming setup alt in /vero html:", html.count("Gaming setup"))
print("Your dress in /vero html:", html.count("Your dress"))
