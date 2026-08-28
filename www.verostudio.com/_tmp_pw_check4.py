# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json

# Try likely vero paths
URLS = [
    "http://127.0.0.1:8080/index.html",
    "http://127.0.0.1:8080/vero",
    "http://127.0.0.1:8080/home",
    "http://127.0.0.1:8080/?vero=1",
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    for url in URLS:
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=20000)
            info = page.evaluate("""() => ({
              title: document.title,
              hasFull: document.documentElement.innerHTML.includes('FullSizeScroller'),
              has6: document.documentElement.innerHTML.includes('6lubt4tb'),
            })""")
            print(url, resp.status if resp else None, info)
        except Exception as e:
            print(url, "ERR", e)

    # Read serve rewrite by fetching /index.html directly after checking
    page.goto("http://127.0.0.1:8080/index.html", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(5000)
    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) el.scrollIntoView({block:'center'});
    }""")
    page.wait_for_timeout(1500)
    result = page.evaluate("""() => {
      const out = {stylesheetHit:false, items:[], allItemIds:[]};
      document.querySelectorAll('[class*="FullSizeScrollerStepperItem"]').forEach(el => {
        if (el.className.includes('Beacon')) return;
        out.allItemIds.push(el.id);
      });
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.cssText && rule.cssText.includes('6lubt4tb')) out.stylesheetHit = true;
          }
        } catch(e) {}
      }
      out.allItemIds.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const cs = getComputedStyle(el);
        const parallax = el.querySelector('[class*="Parallax"]');
        const pInner = parallax ? parallax.querySelector('[class*="container"]') : null;
        const img = el.querySelector('img');
        out.items.push({
          id,
          inline: el.getAttribute('style'),
          computedMask: cs.getPropertyValue('--mask-progress').trim(),
          clipPath: cs.clipPath,
          opacity: cs.opacity,
          visibility: cs.visibility,
          display: cs.display,
          rect: {w: Math.round(el.getBoundingClientRect().width), h: Math.round(el.getBoundingClientRect().height), t: Math.round(el.getBoundingClientRect().top)},
          parallaxStyle: parallax ? parallax.getAttribute('style') : null,
          parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
          innerTransform: pInner ? getComputedStyle(pInner).transform : null,
          imgComplete: img ? img.complete : null,
          imgNW: img ? img.naturalWidth : null,
        });
      });
      const section = document.querySelector('[data-type="full-size-scroller-stepper"] section') || document.querySelector('[class*="FullSizeScrollerStepper"]');
      out.sectionInline = section ? section.getAttribute('style') : null;
      out.sectionActive = section ? getComputedStyle(section).getPropertyValue('--active').trim() : null;
      out.cssLinks = [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.getAttribute('href')).filter(h => h && h.includes('basln'));
      return out;
    }""")
    print(json.dumps(result, indent=2))

    # scroll deeper
    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) window.scrollTo(0, el.offsetTop + 1800);
    }""")
    page.wait_for_timeout(1200)
    result2 = page.evaluate("""() => [...document.querySelectorAll('[class*="FullSizeScrollerStepperItem"]')].filter(el => !el.className.includes('Beacon')).map(el => {
      const cs = getComputedStyle(el);
      const parallax = el.querySelector('[class*="Parallax"]');
      const pInner = parallax ? parallax.querySelector('[class*="container"]') : null;
      return {
        id: el.id,
        computedMask: cs.getPropertyValue('--mask-progress').trim(),
        clipPath: cs.clipPath,
        parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
        innerTransform: pInner ? getComputedStyle(pInner).transform : null,
      };
    })""")
    print("AFTER_SCROLL", json.dumps(result2, indent=2))
    browser.close()
