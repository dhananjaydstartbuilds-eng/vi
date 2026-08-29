from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(10000)

        html = page.content()
        print("html has slide-1:", "slide-1.avif" in html)
        print("html has slide-2:", "slide-2.jpg" in html)
        print("html has slide-3:", "slide-3.mp4" in html)
        print("html has FullSizeScroller:", "FullSizeScrollerStepper" in html)
        print("html has Your dress:", "Your dress" in html)

        try:
            page.wait_for_selector('[class*="FullSizeScrollerStepper"]', timeout=30000)
        except Exception as exc:
            print("scroller wait failed:", exc)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.4)")
        page.wait_for_timeout(5000)

        result = page.evaluate(
            """() => {
          const html = document.documentElement.innerHTML;
          const scroller = document.querySelector('[class*="FullSizeScrollerStepper"]');
          const imgs = Array.from(document.querySelectorAll('img'));
          const videos = Array.from(document.querySelectorAll('video'));
          return {
            scrollerFound: !!scroller,
            allSlide1: imgs.filter((el) => (el.currentSrc || el.src || '').includes('slide-1.avif')).length,
            allSlide2: imgs.filter((el) => (el.currentSrc || el.src || '').includes('slide-2.jpg')).length,
            allSlide3: videos.filter((el) => (el.currentSrc || el.src || '').includes('slide-3.mp4')).length,
            htmlSlide1: html.includes('slide-1.avif'),
            htmlSlide2: html.includes('slide-2.jpg'),
            htmlSlide3: html.includes('slide-3.mp4'),
            scrollerInHtml: html.includes('FullSizeScrollerStepper'),
          };
        }"""
        )
        print("result:", result)
        browser.close()


if __name__ == "__main__":
    main()
