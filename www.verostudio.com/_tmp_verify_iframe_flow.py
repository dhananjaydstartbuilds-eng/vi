from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8080"


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(BASE + "/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

        # Scroll through hero to trigger iframe load
        for pct in (0.3, 0.5, 0.7, 0.85):
            page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {pct})")
            page.wait_for_timeout(1200)

        result = page.evaluate(
            """() => {
          const iframe = document.getElementById('vero-frame');
          const doc = iframe?.contentDocument;
          return {
            iframeSrc: iframe?.getAttribute('src') || null,
            iframeLoaded: !!iframe?.getAttribute('src'),
            iframePath: doc?.location?.pathname || null,
            iframeAppError: doc?.body?.innerText?.includes('Application error') || false,
            iframeMainHero: !!doc?.querySelector('[class*="MainHero"]'),
          };
        }"""
        )
        print(result)
        ok = (
            result.get("iframeLoaded")
            and result.get("iframePath") == "/"
            and not result.get("iframeAppError")
            and result.get("iframeMainHero")
        )
        print("IFRAME_VERIFY_OK" if ok else "IFRAME_VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
