#!/usr/bin/env python3
# Regenerate index-ivory.html from index.html: identical copy/structure,
# only the color palette swapped to Warm Ivory / Champagne. Run after any copy edit.
import sys

SRC = "index.html"
OUT = "index-ivory.html"
s = open(SRC, encoding="utf-8").read()

# (find, replace) — dark theme -> ivory theme. Each must hit at least once.
SUBS = [
    ("--bg:#0A0E0F; --bg2:#0D1315; --panel:#12191C; --panel2:#161F22;",
     "--bg:#F1EBDF; --bg2:#F6F1E7; --panel:#FBF7EF; --panel2:#F3ECDF;"),
    ("--line:rgba(232,240,238,.10); --line2:rgba(232,240,238,.16);",
     "--line:rgba(42,38,32,.12); --line2:rgba(42,38,32,.22);"),
    ("--ink:#ECEFEC; --muted:#93A09D; --faint:#5D6A67;",
     "--ink:#2A2620; --muted:#867C6E; --faint:#A99E8D;"),
    ("--gold:#E6B15E; --gold2:#F2C982; --teal:#57B7C1;",
     "--gold:#A8823E; --gold2:#C9A96A; --teal:#3F857B;"),
    ("rgba(87,183,193,.10),transparent 55%", "rgba(201,169,106,.14),transparent 55%"),
    ("rgba(230,177,94,.07),transparent 60%", "rgba(168,130,62,.08),transparent 60%"),
    ("::selection{background:var(--gold);color:#12100A;}",
     "::selection{background:var(--gold);color:#FBF7EF;}"),
    ("header.solid{background:rgba(10,14,15,.82);",
     "header.solid{background:rgba(241,235,223,.86);"),
    ("color:#C6CECB;max-width:18ch;", "color:#3A352C;max-width:18ch;"),   # manifesto
    ('font-size:clamp(24px,3.2vw,40px);line-height:1.25;color:#D8DFDC;',
     'font-size:clamp(24px,3.2vw,40px);line-height:1.25;color:#3A352C;'),  # sample .st
    ("overflow:hidden;aspect-ratio:16/11;",
     "overflow:hidden;aspect-ratio:16/11;box-shadow:0 30px 60px -30px rgba(42,38,32,.25);"),
    ("background:linear-gradient(135deg,#0e1416,#0a0e0f);",
     "background:linear-gradient(150deg,#FFFDF8,#F1EBDF);"),
    (".sample-frame .bar{position:absolute;top:0;left:0;right:0;height:34px;background:rgba(0,0,0,.35);",
     ".sample-frame .bar{position:absolute;top:0;left:0;right:0;height:34px;background:rgba(42,38,32,.05);"),
]

for find, rep in SUBS:
    n = s.count(find)
    if n < 1:
        sys.exit(f"NOT FOUND (index.html changed?): {find[:50]}")
    s = s.replace(find, rep)

open(OUT, "w", encoding="utf-8").write(s)
print(f"wrote {OUT} ({len(SUBS)} palette subs applied)")
