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
        page.wait_for_timeout(3000)

        for pct in (0.2, 0.35, 0.5, 0.65, 0.8):
            page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {pct})")
            page.wait_for_timeout(1200)

        result = page.evaluate(
            """() => {
          const scroller = document.querySelector('[class*="FullSizeScrollerStepper"]');
          const videos = Array.from(document.querySelectorAll('[class*="FullSizeScrollerStepper"] video'));
          const imgs = Array.from(document.querySelectorAll('[class*="FullSizeScrollerStepper"] img'));
          const slide1 = videos.filter((el) => (el.currentSrc || el.src || '').includes('slide-1.mp4'));
          const slide2 = videos.filter((el) => (el.currentSrc || el.src || '').includes('slide-2.mp4'));
          const slide3 = videos.filter((el) => (el.currentSrc || el.src || '').includes('slide-3.mp4'));
          return {
            scrollerFound: !!scroller,
            videoCount: videos.length,
            imgCount: imgs.length,
            slide1Count: slide1.length,
            slide2Count: slide2.length,
            slide3Count: slide3.length,
            slide1Ready: slide1.some((el) => el.readyState >= 2),
            slide2Ready: slide2.some((el) => el.readyState >= 2),
            slide3Ready: slide3.some((el) => el.readyState >= 2),
            diamondCount: document.querySelectorAll('[class*="FullSizeScrollerStepper"] [role="tab"]').length,
          };
        }"""
        )

        malformed = [e for e in errors if "Malformed asset" in e]
        print("malformed_errors:", len(malformed))
        print("result:", result)
        ok = (
            not malformed
            and result.get("scrollerFound")
            and result.get("imgCount", 1) == 0
            and result.get("slide1Count", 0) >= 1
            and result.get("slide2Count", 0) >= 1
            and result.get("slide3Count", 0) >= 1
            and result.get("diamondCount") == 3
        )
        print("VERIFY_OK" if ok else "VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
