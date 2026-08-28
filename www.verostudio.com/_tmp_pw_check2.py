# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = None
    for channel in ("msedge", "chrome", "chrome-beta"):
        try:
            browser = p.chromium.launch(channel=channel, headless=True)
            print("USING", channel)
            break
        except Exception as e:
            print("fail", channel, e)
    if not browser:
        raise SystemExit("no browser")

    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(r"file:///d:/Node/personal/3d/www.verostudio.com/_tmp_cascade.html")
    page.wait_for_timeout(300)
    print("CASCADE_TITLE", page.title())

    page.goto("http://127.0.0.1:8080/", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)

    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) el.scrollIntoView({block:'center'});
    }""")
    page.wait_for_timeout(1500)

    result = page.evaluate("""() => {
      const out = {items:[], stylesheetHit:false, allItemIds:[]};
      document.querySelectorAll('.FullSizeScrollerStepper-module-scss-module__K-7siW__FullSizeScrollerStepperItem').forEach(el => {
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
        if (!el) { out.items.push({id, missing:true}); return; }
        const cs = getComputedStyle(el);
        const parallax = el.querySelector('[class*="Parallax"]');
        const pInner = el.querySelector('[class*="Parallax"] [class*="container"]') || el.querySelector('[class*="yFfC6G__container"]');
        const img = el.querySelector('img');
        out.items.push({
          id,
          inline: el.getAttribute('style'),
          computedMask: cs.getPropertyValue('--mask-progress').trim(),
          clipPath: cs.clipPath,
          opacity: cs.opacity,
          visibility: cs.visibility,
          display: cs.display,
          rect: {w: el.getBoundingClientRect().width, h: el.getBoundingClientRect().height, t: el.getBoundingClientRect().top},
          parallaxStyle: parallax ? parallax.getAttribute('style') : null,
          parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
          innerTransform: pInner ? getComputedStyle(pInner).transform : null,
          img: img ? {nw: img.naturalWidth, complete: img.complete, curr: (img.currentSrc||'').slice(-40)} : null,
        });
      });
      const section = document.querySelector('[class*="FullSizeScrollerStepper"][style]');
      out.sectionInline = section ? section.getAttribute('style') : null;
      out.sectionActive = section ? getComputedStyle(section).getPropertyValue('--active').trim() : null;
      return out;
    }""")
    print(json.dumps(result, indent=2))

    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) window.scrollTo(0, el.offsetTop + Math.min(el.offsetHeight*0.7, 2500));
    }""")
    page.wait_for_timeout(1200)
    result2 = page.evaluate("""() => {
      return [...document.querySelectorAll('.FullSizeScrollerStepper-module-scss-module__K-7siW__FullSizeScrollerStepperItem')].map(el => {
        const cs = getComputedStyle(el);
        const parallax = el.querySelector('[class*="Parallax"]');
        const pInner = el.querySelector('[class*="yFfC6G__container"]');
        return {
          id: el.id,
          computedMask: cs.getPropertyValue('--mask-progress').trim(),
          clipPath: cs.clipPath,
          parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
          innerTransform: pInner ? getComputedStyle(pInner).transform : null,
        };
      });
    }""")
    print("AFTER_SCROLL", json.dumps(result2, indent=2))
    browser.close()
