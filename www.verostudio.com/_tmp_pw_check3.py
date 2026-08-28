# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    resp = page.goto("http://127.0.0.1:8080/", wait_until="domcontentloaded", timeout=60000)
    print("status", resp.status if resp else None, "url", page.url)
    page.wait_for_timeout(2000)
    info = page.evaluate("""() => ({
      title: document.title,
      len: document.documentElement.innerHTML.length,
      hasStepperType: !!document.querySelector('[data-type="full-size-scroller-stepper"]'),
      has6lu: document.documentElement.innerHTML.includes('6lubt4tb'),
      hasFullSize: document.documentElement.innerHTML.includes('FullSizeScrollerStepper'),
      itemCount: document.querySelectorAll('[class*="FullSizeScrollerStepperItem"]').length,
      linkHrefs: [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href).slice(0,8),
      bodyStart: document.body ? document.body.innerHTML.slice(0,300) : null,
    })""")
    print(json.dumps(info, indent=2))

    # Force-wait for content
    page.wait_for_timeout(5000)
    info2 = page.evaluate("""() => ({
      has6lu: document.documentElement.innerHTML.includes('6lubt4tb'),
      itemCount: document.querySelectorAll('[id*="6lubt4tb"]').length,
      anyItem: [...document.querySelectorAll('[class*="ScrollerStepperItem"]')].slice(0,5).map(e => ({id:e.id, cls:e.className.slice(0,80)})),
      textHit: document.body.innerText.includes('DRESS') || document.body.innerText.includes('SCULPTURE'),
      textSample: document.body.innerText.slice(0,500),
    })""")
    print(json.dumps(info2, indent=2))
    browser.close()
