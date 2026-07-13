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
 # --- 색 모노 (단일 색상 틴트 6종, 색상환 전반) ---
 ("huemono","mono-azure","Azure Tint","애저 틴트",["bright","cool","calm"],["#0B1F3A","#12467E","#2E7BD6","#7FB2ED","#DCEBFB"]),
 ("huemono","mono-emerald-t","Emerald Tint","에메랄드 틴트",["bright","cool","calm"],["#06231A","#0B5A3F","#1E9E70","#73CBA6","#D6F0E4"]),
 ("huemono","mono-ruby-t","Ruby Tint","루비 틴트",["bright","warm","bold"],["#2A0710","#7A1330","#C42A4E","#E87B93","#FBDBE2"]),
 ("huemono","mono-violet","Violet Tint","바이올렛 틴트",["bright","cool","calm"],["#1C0F33","#43277A","#7B52C9","#B39BE6","#EBE2FA"]),
 ("huemono","mono-amber-t","Amber Tint","앰버 틴트",["bright","warm","calm"],["#2E1A05","#7A4A0E","#C9861F","#E8BA6B","#FBEBCB"]),
 ("huemono","mono-teal-t","Teal Tint","틸 틴트",["bright","cool","calm"],["#032826","#0A5C58","#159C95","#69C9C3","#D3F0EE"]),
 # --- 레트로 ---
 ("retro","retro-70s","Harvest 70s","하비스트 70s",["warm","bold"],["#5B3A1A","#A8611E","#D99A2B","#8A8B2C","#E9D9B0"]),
 ("retro","retro-80s","Miami 80s","마이애미 80s",["bright","bold","experimental"],["#0E2A3A","#0BB5C9","#FF5D8F","#FFC24B","#F2F7F6"]),
 ("retro","retro-90s","Grunge 90s","그런지 90s",["dark","calm"],["#211F1C","#5B4A3A","#8A7B5C","#6E7A55","#C9BFA6"]),
 # --- 그라데이션 ---
 ("gradient","grad-sunset","Sunset Fade","선셋 페이드",["warm","bold"],["#2B1055","#7A2C6B","#C43C6E","#F26D52","#FBB03B"]),
 ("gradient","grad-aurora","Aurora","오로라",["cool","experimental"],["#05121F","#123B5E","#1E8F8F","#4FD1A5","#BFF3D9"]),
 ("gradient","grad-dusk","Dusk","더스크",["cool","calm"],["#1A1E33","#3B3B6E","#6A5A9E","#B58BB0","#F1C9B8"]),
 ("gradient","grad-peach","Peach Sky","피치 스카이",["bright","warm","calm"],["#FCE9DE","#F9C6B0","#F2937E","#D96A8A","#8A4C7C"]),
 # --- 보태니컬 (그린 계열) ---
 ("botanical","bot-olive","Olive Garden","올리브 가든",["warm","calm"],["#25281B","#4A5230","#7C8A4E","#B7C089","#EDEFDC"]),
 ("botanical","bot-eucalyptus","Eucalyptus","유칼립투스",["cool","calm"],["#20302B","#3E5A4E","#6E9484","#AEC9BC","#E7F0EB"]),
 ("botanical","bot-fern","Deep Fern","딥 펀",["dark","calm"],["#0C1A12","#173D28","#2C6B45","#5AA06E","#CDE7D2"]),
 # --- 아쿠아 (블루 계열) ---
 ("aqua","aqua-ocean","Deep Ocean","딥 오션",["dark","cool","calm"],["#04141F","#0A3A54","#0E6E92","#3FA9C9","#CDEBF4"]),
 ("aqua","aqua-lagoon","Lagoon","라군",["bright","cool"],["#053B3B","#0E7C7B","#2BB6A8","#8AD9CE","#E5F6F2"]),
 ("aqua","aqua-denim","Denim","데님",["cool","calm"],["#1B2A3A","#33506E","#5B7FA6","#9DB8D2","#E4ECF4"]),
 # --- 베리 (핑크·퍼플) ---
 ("berry","berry-rasp","Raspberry","라즈베리",["bright","bold"],["#2A0A1B","#7A123F","#C21E63","#E85C93","#F9CFDE"]),
 ("berry","berry-plum","Plum Wine","플럼 와인",["dark","calm"],["#1C0F1A","#3E1B38","#6E2E5C","#A85A8E","#E7C6DA"]),
 ("berry","berry-magenta","Magenta Pop","마젠타 팝",["bright","bold","experimental"],["#160A1F","#5A147A","#A31FB0","#E24AE2","#F7CFF3"]),
 # --- 시트러스 (옐로·오렌지) ---
 ("citrus","citrus-lime","Lemon Lime","레몬 라임",["bright","bold"],["#1E2A05","#4E6E12","#8FB01E","#C6E24A","#F2F7CF"]),
 ("citrus","citrus-tang","Tangerine","탠저린",["bright","warm","bold"],["#3A1405","#8A3410","#D9631E","#F29A4B","#FBDFB0"]),
 ("citrus","citrus-mango","Mango","망고",["bright","warm"],["#3A2205","#9A6410","#E0A21E","#F2C94C","#FBEFC6"]),
 # --- 비비드 추가 ---
 ("vivid","vivid-pop","Pop Art","팝 아트",["bright","bold","experimental"],["#FFFFFF","#FF2E63","#08D9D6","#FFD93D","#252A34"]),
 ("vivid","vivid-tropical","Tropical","트로피컬",["bright","bold"],["#0A3A2A","#12A15A","#F2C94C","#F2664B","#FDF6EC"]),
 ("vivid","vivid-festival","Festival","페스티벌",["bright","bold","experimental"],["#2B1E5A","#E23FA0","#FF8A3D","#3FD0E2","#FBF3E8"]),
 # --- 네온 추가 ---
 ("neon","neon-miami","Miami Neon","마이애미 네온",["dark","bold","experimental"],["#0A0F1F","#1B1035","#F531A0","#31E0F5","#FDE24A"]),
 ("neon","neon-toxic","Toxic","톡식",["dark","bold","experimental"],["#060A06","#12210F","#7CFF3F","#39FFC2","#E9FFD6"]),
 # --- 듀오톤 추가 ---
 ("duotone","duo-navy-gold","Navy & Gold","네이비 골드",["dark","warm"],["#0A1A33","#13294F","#C9A96A","#F0E6D2","#0A1A33"]),
 ("duotone","duo-forest-cream","Forest & Cream","포레스트 크림",["warm","calm"],["#1E3A2E","#2F5D45","#EAE3D0","#C6B893","#1E3A2E"]),
 # --- 주얼 추가 ---
 ("jewel","jewel-sapphire","Sapphire","사파이어",["dark","bold"],["#060E2A","#122A6E","#2E56C9","#C9A96A","#EAF0FB"]),
 ("jewel","jewel-amethyst","Amethyst","아메시스트",["dark","calm"],["#140A24","#3A1E5C","#6E3FA0","#B18AD6","#EEE4F7"]),
 # --- 어시 추가 ---
 ("earthy","earthy-rust","Rust & Clay","러스트 클레이",["warm","bold"],["#2A130B","#7A331A","#B85C34","#D99A6C","#F0DEC9"]),
]
CATNAMES={"neutral":"뉴트럴","mono":"모노톤","bw":"흑백","neon":"네온","pastel":"파스텔",
 "earthy":"어시","jewel":"주얼","duotone":"듀오톤","vivid":"비비드","cool":"쿨","dark":"다크",
 "huemono":"색 모노","retro":"레트로","gradient":"그라데이션","botanical":"보태니컬",
 "aqua":"아쿠아","berry":"베리","citrus":"시트러스"}

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
