# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # 1) Cascade test
    page.goto(r"file:///d:/Node/personal/3d/www.verostudio.com/_tmp_cascade.html")
    page.wait_for_timeout(200)
    print("CASCADE_TITLE", page.title())

    # 2) Live site
    page.goto("http://127.0.0.1:8080/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1500)

    # Scroll to stepper
    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) el.scrollIntoView({block:'center'});
    }""")
    page.wait_for_timeout(800)

    result = page.evaluate("""() => {
      const ids = ['_R_6lubt4tb_-0','_R_6lubt4tb_-1','_R_6lubt4tb_-2'];
      const out = {items:[], stylesheetHit:false, allItemIds:[]};
      document.querySelectorAll('.FullSizeScrollerStepper-module-scss-module__K-7siW__FullSizeScrollerStepperItem').forEach(el => {
        out.allItemIds.push(el.id);
      });
      // check if our rule exists
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.selectorText && rule.selectorText.includes('6lubt4tb')) out.stylesheetHit = true;
          }
        } catch(e) {}
      }
      for (const id of ids) {
        const el = document.getElementById(id);
        if (!el) { out.items.push({id, missing:true}); continue; }
        const cs = getComputedStyle(el);
        const parallax = el.querySelector('.Parallax-module-scss-module__yFfC6G__Parallax');
        const pInner = el.querySelector('.Parallax-module-scss-module__yFfC6G__container');
        const img = el.querySelector('img');
        out.items.push({
          id,
          inline: el.getAttribute('style'),
          computedMask: cs.getPropertyValue('--mask-progress').trim(),
          clipPath: cs.clipPath,
          opacity: cs.opacity,
          visibility: cs.visibility,
          zIndex: cs.zIndex,
          display: cs.display,
          rect: el.getBoundingClientRect().toJSON(),
          parallaxStyle: parallax ? parallax.getAttribute('style') : null,
          parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
          innerTransform: pInner ? getComputedStyle(pInner).transform : null,
          imgNatural: img ? {w: img.naturalWidth, h: img.naturalHeight, complete: img.complete, src: img.currentSrc||img.src} : null,
        });
      }
      const section = document.querySelector('.FullSizeScrollerStepper-module-scss-module__K-7siW__FullSizeScrollerStepper');
      out.sectionActive = section ? getComputedStyle(section).getPropertyValue('--active').trim() : null;
      out.sectionInline = section ? section.getAttribute('style') : null;
      return out;
    }""")
    print(json.dumps(result, indent=2))

    # Scroll deeper through stepper to see if progress advances
    page.evaluate("""() => {
      const el = document.querySelector('[data-type="full-size-scroller-stepper"]');
      if (el) window.scrollTo(0, el.offsetTop + el.offsetHeight * 0.6);
    }""")
    page.wait_for_timeout(800)
    result2 = page.evaluate("""() => {
      return ['_R_6lubt4tb_-0','_R_6lubt4tb_-1','_R_6lubt4tb_-2'].map(id => {
        const el = document.getElementById(id);
        if (!el) return {id, missing:true};
        const cs = getComputedStyle(el);
        const parallax = el.querySelector('.Parallax-module-scss-module__yFfC6G__Parallax');
        const pInner = el.querySelector('.Parallax-module-scss-module__yFfC6G__container');
        return {
          id,
          computedMask: cs.getPropertyValue('--mask-progress').trim(),
          clipPath: cs.clipPath,
          parallaxWidth: parallax ? getComputedStyle(parallax).getPropertyValue('--parallax-width').trim() : null,
          innerTransform: pInner ? getComputedStyle(pInner).transform : null,
        };
      });
    }""")
    print("AFTER_SCROLL", json.dumps(result2, indent=2))
    browser.close()
