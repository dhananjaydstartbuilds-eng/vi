# Attach this hero homepage to another project

Copy everything below this line and paste it into Cursor (or another AI coding assistant) in the other project, with this unzipped kit attached.

---

Use the attached **homepage-hero-kit** as the homepage of this project.

## Goal

Replace the landing page (`/` or the main home route) with this full-viewport scroll-scrub hero. Match the look and motion of the kit. Do **not** add a works collage, footer CTA card, resources page, or case-study pages unless I ask later.

## Files in the kit

- `index.html` — markup and overlay structure
- `css/hero.css` — all hero styles (plain CSS, no Tailwind required)
- `js/hero.js` — GSAP ScrollTrigger video scrub, overlay fade, audience tabs, brand ticker, testimonials
- `videos/hero.webm` — hero background video (optional `videos/hero.mp4` if present)
- `logos/noccarc.png` and `logos/cakeequity.svg`

## What to build

1. Put assets where this stack expects static files (e.g. `public/videos/hero.webm`, `public/logos/...`, or keep the kit folder and point paths at it).
2. Recreate this layout:
   - Outer section height **400vh**
   - Inner **sticky** full viewport (`100dvh`) black stage
   - Muted, playsinline video covering the stage (`object-fit: cover`)
   - Film-grain overlay
   - UI overlay on top that fades out as you scroll
3. Motion (GSAP + ScrollTrigger):
   - Pause the video; scrub `currentTime` from 0 → duration while scrolling the section (`start: top top`, `end: 85% bottom`, `scrub: true`)
   - Fade the overlay to `autoAlpha: 0` from `top top` to `30% top` with `scrub: 0.3`
4. Overlay content (keep this copy and these links unless I change them):
   - Name: **Kunal** / **Product Designer & Builder**
   - Book a Call → `https://cal.com/uxkunal/15min`
   - Audience tabs + italic Playfair headline (`#ffcf79` highlights) from `js/hero.js` `AUDIENCES`
   - Brand ticker + microlink hover preview from `BRANDS`
   - Rotating testimonials from `TESTIMONIALS`
   - Badges: Contra Unicorn Club, Framer Expert, Dribbble X Pitaka Award Winner
5. Fonts: **Inter** (UI) and **Playfair Display** italic (headline). Load from Google Fonts if this project does not already have them.
6. If this project is React / Next / Vite: add `gsap`, port the HTML into a homepage component, and keep the same ScrollTrigger values. If it is plain HTML, you can drop in `index.html`, `css/hero.css`, and `js/hero.js` as-is (load GSAP from CDN as in the kit).
7. Serve over http (not `file://`) so the video can load.

Match spacing, type sizes, and colors from `css/hero.css`. Do not restyle it into a generic hero.
