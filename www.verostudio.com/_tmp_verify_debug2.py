from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(12000)

    result = page.evaluate(
        """() => {
      const all = Array.from(document.querySelectorAll('*')).filter((el) =>
        (el.className || '').toString().includes('FullSizeScrollerStepper')
      );
      return {
        count: all.length,
        samples: all.slice(0, 5).map((el) => ({
          tag: el.tagName,
          className: el.className,
          hidden: el.hidden,
          display: getComputedStyle(el).display,
          visibility: getComputedStyle(el).visibility,
          rect: el.getBoundingClientRect(),
        })),
        bodyChildCount: document.body.children.length,
        mainExists: !!document.querySelector('main'),
      };
    }"""
    )
    print(result)
    browser.close()
