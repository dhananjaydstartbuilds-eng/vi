from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.on("console", lambda msg: errors.append(f"console:{msg.type}:{msg.text}") if msg.type == "error" else None)
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(15000)
    print("errors:", errors[:20])
    print("main text len:", page.evaluate("() => document.querySelector('main')?.innerText?.length || 0"))
    print("sections:", page.evaluate("() => Array.from(document.querySelectorAll('main section')).map(s => s.className).slice(0,10)"))
    browser.close()
