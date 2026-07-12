#!/usr/bin/env python3
# Build a DIVERSE Pantone palette library for the design quiz.
# Curated hex sets across categories (monotone / B&W / neon / pastel / earthy /
# jewel / duotone / warm-neutral / cool / vivid ...), each color matched to the
# nearest real Pantone via the pantone-palette skill. Emits JS-ready JSON.
import sys, os, json
sys.path.insert(0, os.path.expanduser("~/.claude/skills/pantone-palette/scripts"))
from pantone_db import nearest_pantone

# category, name(EN), name(KO), mood tags (which quiz moods it fits), curated hexes
PALETTES = [
 ("warm-neutral","Ivory & Gold","아이보리 골드",["bright","warm","calm"],
    ["#F1EBDF","#FBF7EF","#C9A96A","#A8823E","#2A2620"]),
 ("mono","Ink Monotone","잉크 모노톤",["dark","cool","calm"],
    ["#0B0D10","#2A2F36","#5B6470","#9AA3B0","#E6EAF0"]),
 ("mono-warm","Sepia Monotone","세피아 모노톤",["warm","calm"],
    ["#2A1B10","#6B4A2E","#A8823E","#D8B87A","#F3E6CE"]),
 ("bw","Black & White","흑백",["bright","calm","bold"],
    ["#111111","#4A4A4A","#9B9B9B","#DDDDDD","#FFFFFF"]),
 ("neon","Neon on Black","네온 온 블랙",["dark","bold","experimental"],
    ["#0A0A0F","#13131A","#39FF14","#FF10F0","#00E5FF"]),
 ("neon-cyber","Cyber Sunset","사이버 선셋",["dark","bold","experimental"],
    ["#0D0221","#241734","#F72585","#7209B7","#4CC9F0"]),
 ("pastel","Soft Pastel","소프트 파스텔",["bright","warm","calm"],
    ["#F7D6E0","#F2E9E4","#C9E4DE","#DBCDF0","#F2C6A0"]),
 ("earthy","Earthy Muted","어시 뮤트",["warm","calm"],
    ["#E6D9C9","#B08968","#7F5539","#5A6650","#2E2A26"]),
 ("jewel","Jewel Tones","주얼 톤",["dark","bold"],
    ["#0F2A24","#0B7A6E","#7B1E3B","#1E3A8A","#E9D8A6"]),
 ("duotone","Cobalt & Coral","코발트 코랄",["bright","bold"],
    ["#0A2540","#2563EB","#FF6B5E","#EAF0F6","#0A2540"]),
 ("vivid","Vivid Play","비비드 플레이",["bright","bold","experimental"],
    ["#111014","#F5F14E","#FF5A3C","#6C4CF1","#F7F7F5"]),
 ("cool-corp","Cool Corporate","쿨 코퍼릿",["bright","cool","calm"],
    ["#FFFFFF","#F1F5F9","#2563EB","#0F172A","#64748B"]),
 ("sunset","Warm Sunset","웜 선셋",["warm","bold"],
    ["#2B1B2F","#7A2E4A","#E0736B","#F2A65A","#F6E7CB"]),
 ("sage","Forest Sage","포레스트 세이지",["bright","calm","warm"],
    ["#F3F1E9","#A3B18A","#588157","#3A5A40","#344E41"]),
 ("noir-gold","Champagne Noir","샴페인 누아르",["dark","warm","calm"],
    ["#0A0E0F","#12191C","#E6B15E","#57B7C1","#ECEFEC"]),
 ("mono-blush","Blush Monotone","블러시 모노톤",["bright","warm","calm"],
    ["#3A1F2B","#7D3F53","#C77D91","#E9BFC9","#FBEEF1"]),
]

out = []
for cid, en, ko, moods, hexes in PALETTES:
    colors = []
    for h in hexes:
        m = nearest_pantone(h, n=1)
        # nearest_pantone returns list of dicts or tuples; normalize
        p = m[0] if isinstance(m, (list, tuple)) else m
        name = p.get("name") if isinstance(p, dict) else (p[0] if isinstance(p, (list, tuple)) else str(p))
        colors.append({"hex": h.upper(), "pantone": name})
    out.append({"id": cid, "en": en, "ko": ko, "moods": moods, "colors": colors})

open("palettes.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(f"{len(out)} palettes built ->", os.path.abspath("palettes.json"))
for p in out:
    print(f"  {p['ko']:12} {p['en']:18}", " ".join(c['pantone'] for c in p['colors'])[:70])
