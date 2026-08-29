from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(10000)

        result = page.evaluate(
            """() => ({
          title: document.title,
          hasError: document.body.innerText.includes('Something went wrong'),
          hasMainHero: !!document.querySelector('[class*="MainHero"]'),
          video: document.querySelector('video')?.currentSrc || null,
          imgCount: document.querySelectorAll('img').length,
          hasGownHash: document.documentElement.innerHTML.includes('cfe716ebeb'),
          hasHeroPhoto: document.documentElement.innerHTML.includes('hero-photo'),
        })"""
        )
        print(result)
        ok = (
            not result["hasError"]
            and result["hasMainHero"]
            and result["hasGownHash"]
            and not result["hasHeroPhoto"]
        )
        print("VERIFY_OK" if ok else "VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
