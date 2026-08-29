from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8080"


def check_vero(page, label: str) -> dict:
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(f"{BASE}/vero", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    result = page.evaluate(
        """() => ({
          pathname: location.pathname,
          hasAppError: document.body.innerText.includes('Application error'),
          hasSomethingWrong: document.body.innerText.includes('Something went wrong'),
          hasMainHero: !!document.querySelector('[class*="MainHero"]'),
          hasScroller: !!document.querySelector('[class*="FullSizeScrollerStepper"]'),
          mainTextLen: document.querySelector('main')?.innerText?.length || 0,
        })"""
    )
    result["errors"] = errors[:5]
    result["label"] = label
    return result


def check_home(page) -> dict:
    page.goto(BASE + "/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2000)
    return page.evaluate(
        """() => ({
          title: document.title,
          hasHero: !!document.getElementById('hero-section'),
          hasVeroFrame: !!document.getElementById('vero-frame'),
          iframeSrc: document.getElementById('vero-frame')?.getAttribute('data-src') || null,
        })"""
    )


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        home = check_home(page)
        vero = check_vero(page, "local")
        print("HOME:", home)
        print("VERO:", vero)
        ok = (
            home.get("hasHero")
            and home.get("iframeSrc") == "/vero"
            and vero.get("pathname") == "/"
            and not vero.get("hasAppError")
            and not vero.get("hasSomethingWrong")
            and vero.get("hasMainHero")
            and not vero.get("errors")
        )
        print("VERIFY_OK" if ok else "VERIFY_FAIL")
        browser.close()


if __name__ == "__main__":
    main()
