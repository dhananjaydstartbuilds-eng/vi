const ICONS = {
  spark: `<svg class="hero-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2 13.6 9l6.8.4-5.4 4.3 1.9 6.5L12 16.6 7.1 20.2l1.9-6.5L3.6 9.4 10.4 9 12 2.2Z"/></svg>`,
  rocket: `<svg class="hero-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2c3.2 2.1 5.4 5.7 5.8 10.2.3 3.2-1 6.2-3.3 8.1l-2.5-2.5-2.5 2.5C7.2 18.4 5.9 15.4 6.2 12.2 6.6 7.7 8.8 4.1 12 2Zm0 8.2a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/></svg>`,
  code: `<svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M8 8 3 12l5 4M16 8l5 4-5 4M14 5l-4 14"/></svg>`,
  scale: `<svg class="hero-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v18M4 8h16M7 8 4 14h6L7 8Zm10 0-3 6h6l-3-6Z"/></svg>`,
  briefcase: `<svg class="hero-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 6V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1h4a2 2 0 0 1 2 2v3H3V8a2 2 0 0 1 2-2h4Zm12 7v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5h18Z"/></svg>`,
};

const HERO_VIDEO_END = "57% top";
const HERO_TRACK_START = "48% top";
const HERO_EXPAND_END = "90% bottom";

const AUDIENCES = [
  {
    id: "everyone",
    label: "For Everyone",
    headline: [
      { text: "Building " },
      { text: "design‑led", highlight: true },
      { text: " digital products " },
      { icon: "spark" },
      { text: " one at a time." },
    ],
  },
  {
    id: "founders",
    label: "Founders",
    headline: [
      { text: "Less process, more of " },
      { icon: "rocket" },
      { text: " " },
      { text: "shipping it faster", highlight: true },
      { text: " over obsessing to get it perfect." },
    ],
  },
  {
    id: "developers",
    label: "Developers",
    headline: [
      { text: "Designed with " },
      { text: "real constraints", highlight: true },
      { text: " " },
      { icon: "code" },
      { text: " not just beautiful mockups." },
    ],
  },
  {
    id: "pms",
    label: "PMs",
    headline: [
      { text: "Tradeoffs over aesthetics " },
      { icon: "scale" },
      { text: " I " },
      { text: "think in scope", highlight: true },
      { text: ", not just screens." },
    ],
  },
  {
    id: "recruiters",
    label: "Recruiters",
    headline: [
      { text: "Not a portfolio " },
      { icon: "briefcase" },
      { text: " actually " },
      { text: "shipping live products", highlight: true },
      { text: "." },
    ],
  },
  {
    id: "designers",
    label: "Designers",
    headline: [
      { text: "The details most people skip " },
      { icon: "spark" },
      { text: " " },
      { text: "that's where I live", highlight: true },
      { text: "." },
    ],
  },
];

const BRANDS = [
  { name: "Mist AI", url: "https://www.mist.com/" },
  { name: "Noccarc", logo: "/hero/logos/noccarc.png", logoClass: "is-noccarc", url: "https://www.noccarc.com/" },
  { name: "onlinesales.ai", url: "https://www.osmos.ai/" },
  { name: "KiwiQ AI", url: "https://kiwiq.ai/" },
  { name: "Nobel" },
  { name: "Retainr", url: "https://www.retainr.io/" },
  { name: "FinnovationZ by Prasad", url: "https://www.finnovationz.com/" },
  { name: "CakeEquity", logo: "/hero/logos/cakeequity.svg", logoClass: "is-cake", url: "https://www.cakeequity.com/au" },
  { name: "Tathya Earth", url: "https://www.tathya.earth/" },
  {
    name: "Better Driving Theory",
    url: "https://play.google.com/store/apps/details?id=dev.seventytwodays.drivingtheory&hl=en_IN",
  },
];

const TESTIMONIALS = [
  {
    quote: "I would recommend Kunal to anyone who is looking for a responsible, creative and quick professional!",
    name: "Aditya Prakash",
    role: "Founder, Ryzr",
  },
  {
    quote: "He always brought new ideas and made our designs much better.",
    name: "Joao Genio",
    role: "CEO, Digitecla",
  },
  {
    quote: "His ideas and creativity makes him an asset to any organisation he works with.",
    name: "Aditi Gupta",
    role: "Frontend Developer, Nobel",
  },
  {
    quote: "He went above and beyond the scope of work to deliver an outstanding website design and Framer development.",
    name: "Vidhoo Raam",
    role: "Co-founder, Second Thought",
  },
  {
    quote: "His expertise and creativity were invaluable in helping us complete the website on Framer.",
    name: "Alind Agarwal",
    role: "Product Designer, Second Thought Studio",
  },
  {
    quote: "I was looking for someone with strong Design & Front-end skills and thankfully I found them.",
    name: "Archie Otu",
    role: "Co-Founder, BrightPay",
  },
  {
    quote: "Kunal have been a great +1 to our team for webflow development.",
    name: "Elise Peate",
    role: "CMO, Cake Equity",
  },
];

function headlineHtml(parts) {
  return parts
    .map((part) => {
      if (part.icon) return ICONS[part.icon] || "";
      if (part.highlight) return `<span class="hl">${part.text}</span>`;
      return part.text;
    })
    .join("");
}

function pinPageTop() {
  if (window.location.hash) return;
  window.scrollTo(0, 0);
  document.documentElement.scrollTop = 0;
  document.body.scrollTop = 0;
}

function setupScroll() {
  const section = document.getElementById("hero-section");
  const video = document.getElementById("hero-video");
  const overlay = document.getElementById("hero-overlay");
  const sticky = document.getElementById("hero-sticky");
  if (!section || !overlay) return;

  if ("scrollRestoration" in history) history.scrollRestoration = "manual";

  let userMoved = window.scrollY > 1;

  const markMoved = () => {
    if (window.scrollY > 1) userMoved = true;
  };

  if (!window.location.hash) pinPageTop();
  gsap.registerPlugin(ScrollTrigger);

  let scrubStarted = false;

  const refreshTriggers = () => {
    const y = window.scrollY;
    ScrollTrigger.refresh();
    if (Math.abs(window.scrollY - y) > 1) window.scrollTo(0, y);
  };

  const startScrub = () => {
    if (scrubStarted) return true;
    if (!video || !video.duration) return false;
    scrubStarted = true;
    video.pause();
    const state = { time: 0 };
    let last = -Infinity;
    gsap.to(state, {
      time: video.duration,
      ease: "none",
      onUpdate: () => {
        if (Math.abs(state.time - last) < 1 / 24) return;
        last = state.time;
        video.currentTime = state.time;
      },
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: HERO_VIDEO_END,
        scrub: true,
      },
    });
    refreshTriggers();
    return true;
  };

  gsap.to(overlay, {
    autoAlpha: 0,
    ease: "none",
    scrollTrigger: {
      trigger: section,
      start: "top top",
      end: "17% top",
      scrub: 0.3,
    },
  });

  if (video) {
    video.addEventListener("error", () => sticky.classList.add("is-fallback"));
    ["loadedmetadata", "loadeddata", "canplay"].forEach((eventName) => {
      video.addEventListener(eventName, startScrub);
    });
    video.load();
    const unlock = video.play();
    if (unlock && typeof unlock.then === "function") {
      unlock.then(() => video.pause()).catch(() => {});
    }
    startScrub();
  } else {
    sticky.classList.add("is-fallback");
  }

  window.addEventListener("load", () => {
    refreshTriggers();
  });
  window.addEventListener("pageshow", (event) => {
    if (!event.persisted) return;
    if (window.location.hash) return;
    if (window.scrollY > 1 || userMoved) return;
    pinPageTop();
    gsap.set(overlay, { autoAlpha: 1 });
    refreshTriggers();
  });
  window.addEventListener("scroll", markMoved, { passive: true });
  window.addEventListener("wheel", markMoved, { passive: true });
  window.addEventListener("touchstart", markMoved, { passive: true });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(refreshTriggers).catch(() => {});
  }
}

function setupAudiences() {
  const tabs = document.getElementById("hero-tabs");
  const headline = document.getElementById("hero-headline");
  if (!tabs || !headline) return;

  let selected = AUDIENCES[0].id;
  headline.innerHTML = headlineHtml(AUDIENCES[0].headline);

  const renderTabs = () => {
    tabs.innerHTML = AUDIENCES.map(
      (item) =>
        `<button type="button" class="hero-tab${item.id === selected ? " is-active" : ""}" role="tab" data-id="${item.id}" aria-selected="${item.id === selected}">${item.label}</button>`,
    ).join("");
  };

  const show = (id) => {
    if (id === selected) return;
    selected = id;
    renderTabs();
    const next = AUDIENCES.find((item) => item.id === id) || AUDIENCES[0];
    const timeline = gsap.timeline();
    timeline
      .to(headline, { opacity: 0, filter: "blur(4px)", duration: 0.2, ease: "none" })
      .add(() => {
        headline.innerHTML = headlineHtml(next.headline);
      })
      .to(headline, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power1.out" });
  };

  renderTabs();
  tabs.addEventListener("click", (event) => {
    const button = event.target.closest("[data-id]");
    if (button) show(button.dataset.id);
  });
  tabs.addEventListener("keydown", (event) => {
    const index = AUDIENCES.findIndex((item) => item.id === selected);
    if (event.key === "ArrowRight") {
      event.preventDefault();
      show(AUDIENCES[(index + 1) % AUDIENCES.length].id);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      show(AUDIENCES[(index - 1 + AUDIENCES.length) % AUDIENCES.length].id);
    }
  });
}

function setupTicker() {
  const row = document.getElementById("hero-ticker");
  if (!row) return;

  const itemHtml = (brand) => {
    const label = brand.logo
      ? `<span class="hero-brand-logo" data-url="${brand.url || ""}" data-name="${brand.name}"><img src="${brand.logo}" alt="${brand.name}" class="${brand.logoClass || ""}" /></span>`
      : `<span class="hero-brand" data-url="${brand.url || ""}" data-name="${brand.name}">${brand.name}</span>`;
    return `<span class="hero-ticker-item">${label}<span class="hero-dot" aria-hidden="true"></span></span>`;
  };

  row.innerHTML = [...BRANDS, ...BRANDS].map(itemHtml).join("");

  let preview;
  const hide = () => {
    row.style.animationPlayState = "running";
    preview?.remove();
    preview = null;
  };

  row.addEventListener("mouseenter", (event) => {
    const target = event.target.closest("[data-url]");
    if (!target) return;
    row.style.animationPlayState = "paused";
    const url = target.dataset.url;
    if (!url) return;
    const box = target.getBoundingClientRect();
    preview?.remove();
    preview = document.createElement("div");
    preview.className = "hero-preview";
    preview.style.left = `${box.left + box.width / 2}px`;
    preview.style.top = `${box.top}px`;
    preview.innerHTML = `<img src="https://api.microlink.io/?url=${encodeURIComponent(url)}&screenshot=true&meta=false&embed=screenshot.url" alt="${target.dataset.name} website preview" /><span>${url.replace(/^https?:\/\//, "")}</span>`;
    document.body.appendChild(preview);
  }, true);

  row.addEventListener("mouseleave", hide);
}

function clipLimit() {
  if (window.matchMedia("(min-width: 1024px)").matches) return 85;
  if (window.matchMedia("(min-width: 640px)").matches) return 75;
  return 55;
}

function setupTestimonials() {
  const root = document.getElementById("hero-quotes");
  if (!root) return;

  const slots = [
    { index: 0, extra: "" },
    { index: 1, extra: "is-sm" },
    { index: 2, extra: "is-lg" },
  ];
  let tick = 3;
  const hovered = [false, false, false];
  let tip;

  const paint = () => {
    const limit = clipLimit();
    root.innerHTML = slots
      .map((slot, i) => {
        const item = TESTIMONIALS[slot.index % TESTIMONIALS.length];
        const clipped = item.quote.length > limit ? `${item.quote.slice(0, limit).trimEnd()}…` : item.quote;
        return `<div class="hero-quote ${slot.extra}" data-slot="${i}"><span class="hero-quote-text" data-slot="${i}">“${clipped}”</span><span class="hero-quote-role">— ${item.role}</span></div>`;
      })
      .join("");
  };

  const hideTip = () => {
    tip?.remove();
    tip = null;
  };

  paint();
  window.addEventListener("resize", paint);

  root.addEventListener("mouseenter", (event) => {
    const text = event.target.closest("[data-slot]");
    if (!text) return;
    const i = Number(text.dataset.slot);
    hovered[i] = true;
    const item = TESTIMONIALS[slots[i].index % TESTIMONIALS.length];
    const box = text.getBoundingClientRect();
    hideTip();
    tip = document.createElement("div");
    tip.className = "hero-tip";
    tip.style.left = `${box.left + box.width / 2}px`;
    tip.style.top = `${box.top}px`;
    tip.innerHTML = `<p class="italic">“${item.quote}”</p><p class="meta">— ${item.name}, ${item.role}</p>`;
    document.body.appendChild(tip);
  }, true);

  root.addEventListener("mouseleave", (event) => {
    const text = event.target.closest("[data-slot]");
    if (!text) return;
    hovered[Number(text.dataset.slot)] = false;
    hideTip();
  }, true);

  slots.forEach((slot, i) => {
    const loop = () => {
      window.setTimeout(() => {
        if (hovered[i]) {
          loop();
          return;
        }
        const el = root.children[i];
        if (el) el.style.opacity = "0";
        window.setTimeout(() => {
          slot.index = tick % TESTIMONIALS.length;
          tick += 1;
          paint();
          loop();
        }, 700);
      }, 8000 + Math.random() * 6000);
    };
    loop();
  });
}

setupScroll();
setupAudiences();
setupTicker();
setupTestimonials();
setupVeroGlow();
setupVeroBridge();

function parentMaxScroll() {
  return Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
}

function atParentBottom() {
  return window.scrollY >= parentMaxScroll() - 1;
}

function splashFullyOpen() {
  const glow = document.getElementById("vero-embed");
  return Number(glow && glow.dataset.progress) >= 0.97;
}

function iframeIsReady(iframe) {
  try {
    const doc = iframe.contentDocument;
    const href = doc && (doc.URL || doc.location.href || "");
    return !!(doc && href && !href.startsWith("about:blank"));
  } catch (error) {
    return false;
  }
}

function iframeScrollState(iframe) {
  if (!iframeIsReady(iframe)) return null;
  const win = iframe.contentWindow;
  const doc = iframe.contentDocument;
  if (!win || !doc) return null;
  const el = doc.scrollingElement || doc.documentElement;
  const max = Math.max(0, el.scrollHeight - win.innerHeight);
  const scrollY = win.scrollY || el.scrollTop || 0;
  return { win, el, scrollY, max };
}

function hideVeroLoader(iframe) {
  const doc = iframe.contentDocument;
  if (!doc || !doc.head) return false;
  let style = doc.getElementById("hero-hide-vero-loader");
  if (!style) {
    style = doc.createElement("style");
    style.id = "hero-hide-vero-loader";
    doc.head.appendChild(style);
  }
  style.textContent =
    '[class*="RootLayoutLoader"]{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;}';
  return veroLoaderCleared(iframe);
}

function veroLoaderCleared(iframe) {
  if (!iframeIsReady(iframe)) return false;
  const doc = iframe.contentDocument;
  const win = iframe.contentWindow;
  if (!doc || !win) return false;
  const el = doc.querySelector('[class*="RootLayoutLoader"]');
  if (!el) return true;
  const style = win.getComputedStyle(el);
  return style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0;
}

function resizeVeroFrame(iframe) {
  try {
    iframe.contentWindow.dispatchEvent(new Event("resize"));
  } catch (error) {}
}

function setupVeroGlow() {
  const section = document.getElementById("hero-section");
  const glow = document.getElementById("vero-embed");
  if (!section || !glow) return;

  gsap.registerPlugin(ScrollTrigger);

  const fade = { o: 0 };
  const track = { p: 0 };
  const expand = { p: 0 };
  const closeW = 72;
  const closeH = 40;
  const closeScale = 1;
  const closeY = 50;
  const panelW = 38;
  const panelH = 21;
  const panelScale = 1.2;
  const panelY = 46;
  const openY = 50;

  const applyFade = () => {
    glow.dataset.fade = String(fade.o);
    const ready = glow.dataset.ready === "1";
    glow.style.setProperty("--glow-opacity", ready ? String(fade.o) : "0");
  };

  const applyLayout = () => {
    const t = track.p;
    const e = expand.p;
    const wTrack = closeW + (panelW - closeW) * t;
    const hTrack = closeH + (panelH - closeH) * t;
    const sTrack = closeScale + (panelScale - closeScale) * t;
    const yTrack = closeY + (panelY - closeY) * t;
    const holeW = wTrack + (100 - wTrack) * e;
    const scale = sTrack + (1 - sTrack) * e;
    const y = yTrack + (openY - yTrack) * e;
    glow.style.setProperty("--glow-open", String(e));
    glow.style.setProperty("--glow-w", `${holeW}vw`);
    glow.style.setProperty("--glow-h", `calc(${hTrack}vw * ${1 - e} + 100dvh * ${e})`);
    glow.style.setProperty("--glow-scale", String(scale));
    glow.style.setProperty("--glow-y", `${y}%`);
    glow.dataset.progress = String(e);
    glow.classList.toggle("is-open", e >= 0.97);
  };

  applyFade();
  applyLayout();

  gsap.to(fade, {
    o: 1,
    ease: "none",
    onUpdate: applyFade,
    scrollTrigger: {
      trigger: section,
      start: HERO_TRACK_START,
      end: HERO_VIDEO_END,
      scrub: 0.25,
    },
  });

  gsap.to(track, {
    p: 1,
    ease: "none",
    onUpdate: applyLayout,
    scrollTrigger: {
      trigger: section,
      start: HERO_TRACK_START,
      end: HERO_VIDEO_END,
      scrub: true,
    },
  });

  gsap.to(expand, {
    p: 1,
    ease: "none",
    onUpdate: applyLayout,
    scrollTrigger: {
      trigger: section,
      start: HERO_VIDEO_END,
      end: HERO_EXPAND_END,
      scrub: true,
    },
  });
}

function setupVeroBridge() {
  const section = document.getElementById("hero-section");
  const embed = document.getElementById("vero-embed");
  const iframe = document.getElementById("vero-frame");
  if (!embed || !iframe) return;

  let bridged = false;

  const loadFrame = () => {
    const src = iframe.getAttribute("data-src");
    if (!src || iframe.getAttribute("src")) return;
    iframe.setAttribute("src", src);
  };

  const glowScrollTop = () => {
    if (!section) return window.scrollY;
    return section.offsetTop + section.offsetHeight * 0.5;
  };

  const bindIframeScroll = () => {
    if (bridged || !iframeIsReady(iframe)) return;
    const win = iframe.contentWindow;
    const doc = iframe.contentDocument;
    if (!win || !doc) return;
    bridged = true;
    const revealGlow = () => {
      hideVeroLoader(iframe);
      resizeVeroFrame(iframe);
      if (!veroLoaderCleared(iframe)) return false;
      embed.dataset.ready = "1";
      embed.style.setProperty("--glow-opacity", embed.dataset.fade || "0");
      resizeVeroFrame(iframe);
      return true;
    };
    hideVeroLoader(iframe);
    [80, 250, 700, 1500, 3000].forEach((ms) => {
      window.setTimeout(() => {
        if (!revealGlow()) hideVeroLoader(iframe);
      }, ms);
    });
    revealGlow();

    const onIframeWheel = (event) => {
      if (!splashFullyOpen()) return;
      const state = iframeScrollState(iframe);
      if (!state) return;
      if (event.deltaY < 0 && state.scrollY <= 1) {
        event.preventDefault();
        window.scrollBy(0, event.deltaY);
      }
    };

    win.addEventListener("wheel", onIframeWheel, { passive: false });

    let lastY = null;
    win.addEventListener(
      "touchstart",
      (event) => {
        lastY = event.touches[0].clientY;
      },
      { passive: true },
    );
    win.addEventListener(
      "touchmove",
      (event) => {
        if (!splashFullyOpen()) return;
        if (lastY == null) return;
        const y = event.touches[0].clientY;
        const dy = lastY - y;
        lastY = y;
        const state = iframeScrollState(iframe);
        if (!state) return;
        if (dy < 0 && state.scrollY <= 1) {
          event.preventDefault();
          window.scrollBy(0, dy);
        }
      },
      { passive: false },
    );
  };

  iframe.addEventListener("load", () => {
    bridged = false;
    bindIframeScroll();
  });

  const startFrameAfterParentLoad = () => {
    const run = () => {
      if ("requestIdleCallback" in window) {
        window.requestIdleCallback(() => loadFrame(), { timeout: 1500 });
      } else {
        window.setTimeout(loadFrame, 0);
      }
    };
    if (document.readyState === "complete") run();
    else window.addEventListener("load", run, { once: true });
  };
  startFrameAfterParentLoad();

  window.addEventListener(
    "scroll",
    () => {
      if (!section) return;
      if (window.scrollY >= section.offsetHeight * 0.35) loadFrame();
      if (atParentBottom()) loadFrame();
    },
    { passive: true },
  );

  document.querySelectorAll('a[href="#vero-embed"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      loadFrame();
      window.scrollTo({ top: glowScrollTop(), behavior: "smooth" });
    });
  });
}
