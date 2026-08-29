from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(5000)

        for pct in (0.2, 0.35, 0.5, 0.65):
            page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {pct})")
            page.wait_for_timeout(1500)

        result = page.evaluate(
            """() => {
          const html = document.documentElement.innerHTML;
          const heroPhotoImgs = Array.from(document.querySelectorAll('img')).filter((img) =>
            (img.currentSrc || img.src || '').includes('hero-photo')
          );
          const dressAlts = Array.from(document.querySelectorAll('img[alt="Your dress"]'));
          const scroller = document.querySelector('[class*="FullSizeScrollerStepper"]');
          return {
            title: document.title,
            htmlHasHeroPhoto: html.includes('/images/hero-photo.jpg'),
            htmlHasOldHash: html.includes('cfe716ebeb9d1a0676a59f41aa92b2e678dce13c'),
            heroPhotoImgs: heroPhotoImgs.slice(0, 4).map((img) => ({
              alt: img.getAttribute('alt'),
              currentSrc: img.currentSrc,
              naturalWidth: img.naturalWidth,
              className: img.className,
            })),
            dressAltCount: dressAlts.length,
            scrollerFound: !!scroller,
            scrollerClass: scroller ? scroller.className : null,
          };
        }"""
        )

        print("result:", result)
        ok = (
            result.get("htmlHasHeroPhoto")
            and not result.get("htmlHasOldHash")
            and len(result.get("heroPhotoImgs", [])) > 0
            and all(img.get("naturalWidth", 0) > 0 for img in result.get("heroPhotoImgs", []))
        )
        print("VERIFY_OK" if ok else "VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
