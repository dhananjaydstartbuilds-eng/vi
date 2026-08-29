from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector('[class*="FullSizeScrollerStepper"]', timeout=45000)
        page.wait_for_timeout(8000)

        for pct in (0.2, 0.35, 0.5, 0.65, 0.8):
            page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {pct})")
            page.wait_for_timeout(1200)

        result = page.evaluate(
            """() => {
          const scroller = document.querySelector('[class*="FullSizeScrollerStepper"]');
          const slide1 = Array.from(document.querySelectorAll('[class*="FullSizeScrollerStepper"] img[alt="Your dress"]'));
          const slide2 = Array.from(document.querySelectorAll('[class*="FullSizeScrollerStepper"] img[alt="From data"]'));
          const slide3 = Array.from(document.querySelectorAll('[class*="FullSizeScrollerStepper"] video')).filter((el) =>
            (el.currentSrc || el.src || '').includes('slide-3.mp4')
          );
          return {
            scrollerFound: !!scroller,
            slide1Srcs: slide1.map((el) => el.currentSrc || el.src),
            slide1Loaded: slide1.length > 0 && slide1.every((el) => el.naturalWidth > 0),
            slide1UsesLocal: slide1.every((el) => (el.currentSrc || el.src || '').includes('/images/slide-1.jpg')),
            slide2Srcs: slide2.map((el) => el.currentSrc || el.src),
            slide2Loaded: slide2.length > 0 && slide2.every((el) => el.naturalWidth > 0),
            slide2UsesLocal: slide2.every((el) => (el.currentSrc || el.src || '').includes('/images/slide-2.jpg')),
            slide3Count: slide3.length,
            slide3Ready: slide3.some((el) => el.readyState >= 2),
            diamondCount: document.querySelectorAll('[class*="FullSizeScrollerStepper"] [role="tab"]').length,
            hasFixScript: !!document.querySelector('script[src="/vero/slide-media-fix.js"]'),
          };
        }"""
        )

        malformed = [e for e in errors if "Malformed asset" in e]
        print("malformed_errors:", len(malformed))
        print("result:", result)
        ok = (
            not malformed
            and result.get("scrollerFound")
            and result.get("slide1UsesLocal")
            and result.get("slide1Loaded")
            and result.get("slide2UsesLocal")
            and result.get("slide2Loaded")
            and result.get("slide3Count", 0) >= 1
            and result.get("diamondCount") == 3
            and result.get("hasFixScript")
        )
        print("VERIFY_OK" if ok else "VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
