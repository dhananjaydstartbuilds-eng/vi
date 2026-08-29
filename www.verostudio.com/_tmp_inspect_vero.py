from pathlib import Path

p = Path(__file__).resolve().parent / "www.verostudio.com" / "vero" / "index.html"
t = p.read_text(encoding="utf-8")
print("len", len(t))
print("slide-media-fix", "slide-media-fix.js" in t)
print("replaceState boot", "replaceState" in t[:800])
print("bad brace 1", t.count('Abstract motion background\\"}}},\\"text\\"'))
print("good brace 1", t.count('Abstract motion background\\"}},\\"text\\"'))
print("bad brace 2", t.count('Blue glass background\\"}}},\\"text\\"'))
print("good brace 2", t.count('Blue glass background\\"}},\\"text\\"'))
print("starts with", t[:120])
