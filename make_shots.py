#!/usr/bin/env python3
"""115개 템플릿 zip → 실렌더 스크린샷 썸네일 (assets/shots/<slug>.jpg).

외장(/Volumes/Pool)에 잠깐 풀고 헤드리스 크롬으로 캡처 후 즉시 삭제 —
내장 디스크는 결과 썸네일(≈40KB)만 사용. 이미 있는 썸네일은 건너뜀.

사용: python3 make_shots.py            # 전체
      python3 make_shots.py kane       # 이름 필터
"""
import os, re, sys, shutil, zipfile, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE   = os.path.dirname(os.path.abspath(__file__))
SRC    = "/Volumes/Pool/Cloud/2_user-biz/Design/Portfolio"
WORK   = "/Volumes/Pool/Cloud/2_user-biz/Design/.atelier-shots-work"
OUT    = os.path.join(HERE, "assets", "shots")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SKIP_DIR = re.compile(r'(^|/)(documentation|docs?|licen[cs]e|readme|__macosx|source[-_ ]?files?|psd|sketch-?files?)(/|$)', re.I)
PREFER   = re.compile(r'(^|/)(main|html|demo|template|dist|build|preview|site)(/|$)', re.I)

def pick_entry(root):
    htmls = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not SKIP_DIR.search(d)]
        for f in fn:
            if f.lower().endswith((".html", ".htm")):
                rel = os.path.relpath(os.path.join(dp, f), root)
                if not SKIP_DIR.search(rel):
                    htmls.append(rel)
    if not htmls:
        return None
    def score(rel):
        base = os.path.basename(rel).lower()
        return (0 if base in ("index.html", "index.htm") else 1,
                0 if re.search(r'(^|/)(index|home|main)\.html?$', rel, re.I) else 1,
                0 if PREFER.search(rel) else 1,
                rel.count(os.sep), len(rel), rel.lower())
    return sorted(htmls, key=score)[0]

def shoot(zname):
    slug = re.sub(r'\.zip$', '', zname)
    out = os.path.join(OUT, slug + ".jpg")
    if os.path.exists(out):
        return slug, "skip(exists)"
    dest = os.path.join(WORK, slug)
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest, exist_ok=True)
    try:
        with zipfile.ZipFile(os.path.join(SRC, zname)) as zf:
            for m in zf.namelist():
                if m.startswith("/") or ".." in m.split("/"):
                    continue
                zf.extract(m, dest)
        entry = pick_entry(dest)
        if not entry:
            return slug, "no-html"
        png = os.path.join(dest, "__shot.png")
        url = "file://" + os.path.join(dest, entry)
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--window-size=1280,860", "--virtual-time-budget=30000",
                            "--timeout=20000", "--screenshot=" + png, url],
                           capture_output=True, timeout=60)
        if not os.path.exists(png) or os.path.getsize(png) < 5000:
            return slug, "chrome-fail"
        subprocess.run(["sips", "-Z", "640", "-s", "format", "jpeg",
                        "-s", "formatOptions", "72", png, "--out", out],
                       capture_output=True, timeout=30)
        if not os.path.exists(out):
            return slug, "sips-fail"
        return slug, "ok(%dKB)" % (os.path.getsize(out) // 1024)
    except Exception as e:
        return slug, "err:" + str(e)[:60]
    finally:
        shutil.rmtree(dest, ignore_errors=True)

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    zips = sorted(z for z in os.listdir(SRC) if z.lower().endswith(".zip") and filt in z)
    print("대상:", len(zips), flush=True)
    done = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for slug, st in ex.map(shoot, zips):
            done += 1
            print(f"[{done}/{len(zips)}] {st:14s} {slug[:52]}", flush=True)
    shutil.rmtree(WORK, ignore_errors=True)
    n = len([f for f in os.listdir(OUT) if f.endswith('.jpg')])
    print("완료 — 썸네일", n, "개", flush=True)

if __name__ == "__main__":
    main()
