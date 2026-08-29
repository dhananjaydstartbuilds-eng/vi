from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("console", lambda msg: print("console:", msg.type, msg.text[:200]))
        page.goto(URL, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(8000)

        info = page.evaluate(
            """() => ({
          title: document.title,
          bodyLen: document.body ? document.body.innerHTML.length : 0,
          hasScrollerClass: !!document.querySelector('[class*="FullSizeScrollerStepper"]'),
          hasK7siW: !!document.querySelector('[class*="K-7siW"]'),
          videoCount: document.querySelectorAll('video').length,
          imgCount: document.querySelectorAll('img').length,
          slide1: document.querySelectorAll('[src*="slide-1"]').length,
          slide2: document.querySelectorAll('[src*="slide-2"]').length,
          slide3: document.querySelectorAll('[src*="slide-3"]').length,
          sampleClasses: Array.from(document.querySelectorAll('[class*="Scroller"]')).slice(0,5).map(el => el.className.slice(0,120)),
        })"""
        )
        print("info:", info)
        print("errors:", errors[:10])
        browser.close()


if __name__ == "__main__":
    main()
