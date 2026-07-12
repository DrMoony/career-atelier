#!/usr/bin/env python3
# Diverse Pantone palette library for the design concept builder.
# Curated hexes across categories (neutral/mono/bw/neon/pastel/earthy/jewel/
# duotone/vivid/cool/dark), each color matched to nearest real Pantone.
import sys, os, json
sys.path.insert(0, os.path.expanduser("~/.claude/skills/pantone-palette/scripts"))
from pantone_db import nearest_pantone

# cat, id, en, ko, moods, hexes
P = [
 ("neutral","warm-neutral","Ivory & Gold","아이보리 골드",["bright","warm","calm"],["#F1EBDF","#FBF7EF","#C9A96A","#A8823E","#2A2620"]),
 ("neutral","sand","Warm Sand","웜 샌드",["bright","warm","calm"],["#EDE3D3","#DCC9AE","#B79B78","#7C6A54","#332B22"]),
 ("neutral","greige","Greige","그레이지",["bright","calm"],["#EFEDE8","#D8D3C8","#A9A296","#6E685E","#2B2925"]),
 ("mono","mono-ink","Ink Monotone","잉크 모노톤",["dark","cool","calm"],["#0B0D10","#2A2F36","#5B6470","#9AA3B0","#E6EAF0"]),
 ("mono","mono-sepia","Sepia Monotone","세피아 모노톤",["warm","calm"],["#2A1B10","#6B4A2E","#A8823E","#D8B87A","#F3E6CE"]),
 ("mono","mono-blush","Blush Monotone","블러시 모노톤",["bright","warm","calm"],["#3A1F2B","#7D3F53","#C77D91","#E9BFC9","#FBEEF1"]),
 ("mono","mono-slate","Slate Monotone","슬레이트 모노톤",["cool","calm"],["#141A1F","#33414B","#5E727E","#98A7B0","#DDE5EA"]),
 ("bw","bw-classic","Black & White","흑백",["bright","calm","bold"],["#111111","#4A4A4A","#9B9B9B","#DDDDDD","#FFFFFF"]),
 ("bw","bw-contrast","High Contrast","하이 콘트라스트",["bold"],["#000000","#1A1A1A","#808080","#F2F2F2","#FFFFFF"]),
 ("bw","bw-news","Newsprint","뉴스프린트",["warm","calm"],["#1B1A17","#4B4842","#8C877C","#D6D1C4","#F4F1E9"]),
 ("neon","neon-black","Neon on Black","네온 온 블랙",["dark","bold","experimental"],["#0A0A0F","#13131A","#39FF14","#FF10F0","#00E5FF"]),
 ("neon","neon-cyber","Cyber Sunset","사이버 선셋",["dark","bold","experimental"],["#0D0221","#241734","#F72585","#7209B7","#4CC9F0"]),
 ("neon","neon-vapor","Vaporwave","베이퍼웨이브",["dark","bold","experimental"],["#1A1030","#2D1B4E","#FF6AD5","#8C9EFF","#26F0F1"]),
 ("neon","neon-acid","Acid","애시드",["dark","bold","experimental"],["#0C0F06","#1B2410","#B6FF00","#FF4D00","#EAFFC7"]),
 ("pastel","pastel-soft","Soft Pastel","소프트 파스텔",["bright","warm","calm"],["#F7D6E0","#F2E9E4","#C9E4DE","#DBCDF0","#F2C6A0"]),
 ("pastel","pastel-candy","Candy","캔디",["bright","calm"],["#FFE5EC","#FFC2D1","#BDE0FE","#CDB4DB","#A2D2FF"]),
 ("pastel","pastel-sage","Sage Pastel","세이지 파스텔",["bright","warm","calm"],["#EEF1E6","#D8E2C6","#B7C9A8","#EAD9C4","#F6EFE6"]),
 ("earthy","earthy-muted","Earthy Muted","어시 뮤트",["warm","calm"],["#E6D9C9","#B08968","#7F5539","#5A6650","#2E2A26"]),
 ("earthy","earthy-terra","Terracotta","테라코타",["warm"],["#F3E4D7","#E0A06B","#C1614A","#7A3B2E","#2E1B15"]),
 ("earthy","earthy-desert","Desert","데저트",["warm","calm"],["#F1E3CE","#D9B48F","#B08046","#6E5A3A","#33291C"]),
 ("earthy","earthy-forest","Forest Sage","포레스트 세이지",["bright","calm","warm"],["#F3F1E9","#A3B18A","#588157","#3A5A40","#344E41"]),
 ("jewel","jewel-tones","Jewel Tones","주얼 톤",["dark","bold"],["#0F2A24","#0B7A6E","#7B1E3B","#1E3A8A","#E9D8A6"]),
 ("jewel","jewel-emerald","Emerald Noir","에메랄드 누아르",["dark","calm"],["#08110E","#0E3B2E","#1B7A5A","#C9A96A","#EAF4EE"]),
 ("jewel","jewel-ruby","Ruby & Ink","루비 잉크",["dark","bold"],["#120A0E","#2A1020","#8E1F3C","#D4A15A","#F1E4D0"]),
 ("duotone","duo-cobalt","Cobalt & Coral","코발트 코랄",["bright","bold"],["#0A2540","#2563EB","#FF6B5E","#EAF0F6","#0A2540"]),
 ("duotone","duo-plum","Plum & Gold","플럼 골드",["dark","warm"],["#1E1024","#4A1D52","#C9A96A","#F0E6D2","#1E1024"]),
 ("duotone","duo-teal","Teal & Orange","틸 오렌지",["bright","bold"],["#093A3E","#0E7C86","#FF8C42","#F4EFE6","#093A3E"]),
 ("vivid","vivid-play","Vivid Play","비비드 플레이",["bright","bold","experimental"],["#111014","#F5F14E","#FF5A3C","#6C4CF1","#F7F7F5"]),
 ("vivid","vivid-bauhaus","Bauhaus","바우하우스",["bright","bold"],["#F4EDE1","#E63946","#F4A11E","#1D4E89","#141414"]),
 ("cool","cool-corp","Cool Corporate","쿨 코퍼릿",["bright","cool","calm"],["#FFFFFF","#F1F5F9","#2563EB","#0F172A","#64748B"]),
 ("cool","cool-nordic","Nordic","노르딕",["bright","cool","calm"],["#F7F9FB","#E2E8EE","#9DB2C4","#4A6076","#1F2D3A"]),
 ("dark","noir-gold","Champagne Noir","샴페인 누아르",["dark","warm","calm"],["#0A0E0F","#12191C","#E6B15E","#57B7C1","#ECEFEC"]),
 ("dark","noir-wine","Wine & Gold","와인 골드",["dark","warm"],["#0E0608","#2A0E16","#7A1F35","#C9A96A","#F0E6D6"]),
]
CATNAMES={"neutral":"뉴트럴","mono":"모노톤","bw":"흑백","neon":"네온","pastel":"파스텔",
 "earthy":"어시","jewel":"주얼","duotone":"듀오톤","vivid":"비비드","cool":"쿨","dark":"다크"}

out=[]
for cat,cid,en,ko,moods,hexes in P:
    colors=[]
    for h in hexes:
        m=nearest_pantone(h,n=1); p=m[0] if isinstance(m,(list,tuple)) else m
        name=p.get("name") if isinstance(p,dict) else (p[0] if isinstance(p,(list,tuple)) else str(p))
        colors.append({"hex":h.upper(),"pantone":name})
    out.append({"id":cid,"cat":cat,"catko":CATNAMES[cat],"en":en,"ko":ko,"moods":moods,"colors":colors})

json.dump(out,open("palettes.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
cats={}
for p in out:cats[p['cat']]=cats.get(p['cat'],0)+1
print(f"{len(out)} palettes,", len(cats),"categories:",dict(cats))
