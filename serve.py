#!/usr/bin/env python3
"""Career Atelier 라이브러리 로컬 서버 — 온디맨드 데모 미리보기.

내장 디스크는 거의 꽉 차 있으므로, 클릭한 템플릿 하나만 그때그때
외장(/Volumes/Pool)의 캐시 폴더에 풀어서 보여준다. 캐시는 최근 CACHE_MAX개만
유지하고 오래된 건 자동 삭제한다. 내장에는 아무것도 쓰지 않는다.

사용:
  cd ~/projects/atelier
  python3 serve.py            # 기본 http://localhost:8080
  python3 serve.py 9000       # 포트 지정
그다음 브라우저에서 http://localhost:8080/library.html

라우트:
  /                       → library.html
  /<file>                 → atelier 폴더의 정적 파일 (html/json/css)
  /demo?z=<zip이름>       → 해당 zip을 캐시에 전개 후 데모 index로 302
  /pv/<slug>/<path>       → 전개된 데모 파일 서빙 (외장 캐시)
"""
import os, re, sys, json, zipfile, urllib.parse, posixpath, shutil, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE  = os.path.dirname(os.path.abspath(__file__))
SRC   = "/Volumes/Pool/Cloud/2_user-biz/Design/Portfolio"
CACHE = "/Volumes/Pool/Cloud/2_user-biz/Design/.atelier-previews"
CACHE_MAX = 8            # 동시에 유지할 전개본 개수
PORT  = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

SKIP_DIR = re.compile(r'(^|/)(documentation|docs?|licen[cs]e|readme|__macosx|source[-_ ]?files?|psd|sketch-?files?)(/|$)', re.I)
PREFER   = re.compile(r'(^|/)(main|html|demo|template|dist|build|preview|site)(/|$)', re.I)
MIME = {".html":"text/html",".htm":"text/html",".css":"text/css",".js":"application/javascript",
        ".json":"application/json",".svg":"image/svg+xml",".png":"image/png",".jpg":"image/jpeg",
        ".jpeg":"image/jpeg",".gif":"image/gif",".webp":"image/webp",".ico":"image/x-icon",
        ".woff":"font/woff",".woff2":"font/woff2",".ttf":"font/ttf",".otf":"font/otf",
        ".mp4":"video/mp4",".webm":"video/webm",".map":"application/json",".txt":"text/plain"}

def mime(p):
    return MIME.get(os.path.splitext(p)[1].lower(), "application/octet-stream")

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
        return (0 if base in ("index.html","index.htm") else 1,
                0 if re.search(r'(^|/)(index|home|main)\.html?$', rel, re.I) else 1,
                0 if PREFER.search(rel) else 1,
                rel.count(os.sep), len(rel), rel.lower())
    return sorted(htmls, key=score)[0]

def evict():
    """캐시가 CACHE_MAX를 넘으면 오래된(접근시각 기준) 것부터 삭제."""
    try:
        dirs = [os.path.join(CACHE, d) for d in os.listdir(CACHE)]
        dirs = [d for d in dirs if os.path.isdir(d)]
    except FileNotFoundError:
        return
    if len(dirs) <= CACHE_MAX:
        return
    dirs.sort(key=lambda d: os.path.getmtime(d))
    for d in dirs[:len(dirs) - CACHE_MAX]:
        shutil.rmtree(d, ignore_errors=True)

def ensure(slug):
    """slug(=zip이름 without .zip)을 캐시에 전개하고 진입 상대경로를 돌려준다."""
    dest = os.path.join(CACHE, slug)
    zpath = os.path.join(SRC, slug + ".zip")
    if not os.path.isfile(zpath):
        return None, "zip을 찾을 수 없어요: " + slug + ".zip"
    if not (os.path.isdir(dest) and os.listdir(dest)):
        os.makedirs(dest, exist_ok=True)
        try:
            with zipfile.ZipFile(zpath) as zf:
                for m in zf.namelist():
                    if m.startswith("/") or ".." in m.split("/"):
                        continue
                    zf.extract(m, dest)
        except Exception as e:
            shutil.rmtree(dest, ignore_errors=True)
            return None, "전개 실패: " + str(e)
        evict()
    else:
        os.utime(dest, None)  # LRU 갱신
    entry = pick_entry(dest)
    if not entry:
        return None, "이 템플릿엔 HTML 데모가 없어요 (피그마/스케치/PSD 소스)."
    return entry.replace(os.sep, "/"), None

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 조용히
        pass
    def _send(self, code, body=b"", ctype="text/html; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)
    def _err(self, msg):
        html = ("<meta charset=utf-8><body style='font-family:system-ui;background:#0A0E0F;color:#ECEFEC;"
                "padding:60px;text-align:center'><h2 style='color:#C9A96A'>데모를 열 수 없어요</h2>"
                "<p style='color:#AAB4B1'>" + msg + "</p>"
                "<p><a href='/library.html' style='color:#C9A96A'>← 라이브러리로</a></p>")
        self._send(404, html.encode("utf-8"))
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(u.path)
        # 1) 데모 전개 요청
        if path == "/demo":
            q = urllib.parse.parse_qs(u.query)
            zname = (q.get("z") or [""])[0]
            slug = re.sub(r'\.zip$', '', zname, flags=re.I)
            if not slug:
                return self._err("템플릿이 지정되지 않았어요.")
            entry, err = ensure(slug)
            if err:
                return self._err(err)
            loc = "/pv/" + urllib.parse.quote(slug) + "/" + urllib.parse.quote(entry)
            return self._send(302, b"", extra={"Location": loc})
        # 2) 전개된 데모 파일 서빙
        if path.startswith("/pv/"):
            rest = path[4:]
            seg = rest.split("/", 1)
            slug = seg[0]
            rel = seg[1] if len(seg) > 1 else "index.html"
            base = os.path.realpath(os.path.join(CACHE, slug))
            full = os.path.realpath(os.path.join(base, rel))
            if not full.startswith(base + os.sep) and full != base:
                return self._err("경로 오류")
            if os.path.isdir(full):
                full = os.path.join(full, "index.html")
            if not os.path.isfile(full):
                return self._err("파일 없음: " + rel)
            os.utime(base, None)  # LRU 갱신
            with open(full, "rb") as f:
                data = f.read()
            return self._send(200, data, ctype=mime(full))
        # 3) 정적 파일 (atelier 폴더)
        rel = path.lstrip("/") or "library.html"
        rel = posixpath.normpath(rel)
        if rel.startswith("..") or rel.startswith("/"):
            return self._err("경로 오류")
        full = os.path.join(HERE, rel)
        if not os.path.isfile(full):
            return self._err("없는 파일: " + rel)
        with open(full, "rb") as f:
            data = f.read()
        return self._send(200, data, ctype=mime(full) + ("; charset=utf-8" if full.endswith((".html",".js",".json",".css",".svg")) else ""))

def main():
    for label, p in (("소스(zip)", SRC), ("캐시", CACHE)):
        pass
    if not os.path.isdir(SRC):
        print("[!] 소스 폴더가 없어요:", SRC, "\n    외장(/Volumes/Pool)이 연결돼 있나요?")
        sys.exit(1)
    os.makedirs(CACHE, exist_ok=True)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    print("Career Atelier 라이브러리 서버")
    print("  소스 :", SRC)
    print("  캐시 :", CACHE, "(최근", CACHE_MAX, "개 유지, 내장 디스크 미사용)")
    print("  열기 : http://localhost:%d/library.html" % PORT)
    print("  종료 : Ctrl+C")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n종료합니다.")

if __name__ == "__main__":
    main()
