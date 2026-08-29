from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:8080/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(5000)
    result = page.evaluate(
        """() => ({
          title: document.title,
          hasHero: !!document.querySelector('#hero-section'),
          hasIframe: !!document.querySelector('#vero-frame'),
          iframeSrc: document.querySelector('#vero-frame')?.getAttribute('data-src') || null,
        })"""
    )
    print(result)
    browser.close()
