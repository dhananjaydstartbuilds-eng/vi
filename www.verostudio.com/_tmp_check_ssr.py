from pathlib import Path

html = Path(
    r"d:/Node/personal/3d/www.verostudio.com/www.verostudio.com/vero/index.html"
).read_text(encoding="utf-8", errors="ignore")

idx = html.find('slide-3.mp4')
print("slide-3 context:")
print(html[max(0, idx - 300) : idx + 300])

# Check SSR still has scroller section in initial HTML (before scripts)
body_start = html.find("<body")
body_end = html.find('<script>(self.__next_f')
print("\nSSR has scroller:", "FullSizeScrollerStepper" in html[body_start:body_end])
print("SSR has slide-1:", "slide-1.avif" in html[body_start:body_end])
print("SSR has slide-3 video:", "slide-3.mp4" in html[body_start:body_end])
