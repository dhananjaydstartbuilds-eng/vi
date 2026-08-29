from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/vero"

FOOTER_CHECK = """() => {
  const footer = document.querySelector('[class*="RootLayoutFooter"]');
  const legals = footer?.querySelector('[class*="__legals"]');
  const credits = footer?.querySelector('[class*="__credits"]');
  const copyright = footer?.querySelector('[class*="__copyright"]');
  const style = (el) => (el ? getComputedStyle(el).display : null);
  const visible = (el) => {
    if (!el) return false;
    const s = getComputedStyle(el);
    return s.display !== "none" && s.visibility !== "hidden" && Number(s.opacity) !== 0;
  };
  const creditLinks = credits
    ? [...credits.querySelectorAll("a,button")].map((el) => ({
        tag: el.tagName,
        text: el.textContent.trim(),
        display: getComputedStyle(el).display,
      }))
    : [];
  return {
    hasFooter: !!footer,
    legalsDisplay: style(legals),
    copyrightVisible: visible(copyright),
    copyrightText: copyright?.textContent?.trim() || null,
    creditLinks,
    bodyHasAccessibility: document.body.innerText.includes("Accessibility"),
    bodyHasCredits: document.body.innerText.includes("Credits"),
    bodyHasAllRights: document.body.innerText.includes("All Rights Reserved"),
  };
}"""


def check(page):
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    return page.evaluate(FOOTER_CHECK)


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        desktop = browser.new_page(viewport={"width": 1440, "height": 900})
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        desktop_result = check(desktop)
        mobile_result = check(mobile)
        browser.close()

    print("DESKTOP", desktop_result)
    print("MOBILE", mobile_result)

    ok = (
        desktop_result["hasFooter"]
        and mobile_result["hasFooter"]
        and desktop_result["legalsDisplay"] == "none"
        and mobile_result["legalsDisplay"] == "none"
        and all(link["display"] == "none" for link in desktop_result["creditLinks"])
        and all(link["display"] == "none" for link in mobile_result["creditLinks"])
        and desktop_result["copyrightVisible"]
        and mobile_result["copyrightVisible"]
        and desktop_result["bodyHasAllRights"]
        and mobile_result["bodyHasAllRights"]
        and not desktop_result["bodyHasAccessibility"]
        and not mobile_result["bodyHasAccessibility"]
        and not desktop_result["bodyHasCredits"]
        and not mobile_result["bodyHasCredits"]
    )
    print("VERIFY_OK" if ok else "VERIFY_FAIL")


if __name__ == "__main__":
    main()
