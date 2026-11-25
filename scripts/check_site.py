#!/usr/bin/env python3
"""Pre-push checks for the site: no em dashes, no broken internal links,
every Spanish page has its /en/ twin, every page is in the sitemap, plus the
SEO checks C-01..C-15 (errors) and W-01..W-04 (warnings) proposed in
docs/seo/checklist.md (24-nov-2026, approved by Alex the same day). C-15
checks that the vendored brand copies are in sync with brand/ (skipped
when brand/ is not next to the repo, e.g. in CI).

    python3 scripts/check_site.py [dir]     local checks (default: the repo;
                                            run on _site/ after build_site.sh)
    python3 scripts/check_site.py --live    live checks L-01..L-05 against
                                            https://sanchesque.com, to run by
                                            hand after each deploy

Exit 1 on any error. Standard library only.
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parent.parent
LIVE = "--live" in sys.argv
args = [a for a in sys.argv[1:] if a != "--live"]
SITE = Path(args[0]).resolve() if args else REPO
BASE = "https://sanchesque.com"
SKIP = {"fonts", ".git", ".github", "_site"}
LINK = re.compile(r'(?:href|src)="([^"#?]*)')
# copies built by Zensical in the product repos: they ship their own sitemap
GENERATED = ("garaticker/help", "garaticker/artists")
BLOCKED_SAMEAS = ("wa.me", "whatsapp.com", "giphy.com")  # fixed site rules
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")  # Cloudflare 403s bare Python-urllib (H-B8)

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def is_generated(rel):
    return any(g in str(rel) for g in GENERATED)


def page_url(rel):
    """Canonical URL of an index.html path relative to SITE."""
    rel = rel.as_posix()
    if rel == "index.html":
        return BASE + "/"
    return BASE + "/" + rel[: -len("index.html")]


def url_to_rel(url):
    """Reverse of page_url: /tabaibi/ -> tabaibi/index.html."""
    path = url[len(BASE):] if url.startswith(BASE) else None
    if path is None:
        return None
    path = path.strip("/")
    return (path + "/index.html") if path else "index.html"


def own_pages():
    return [p for p in pages if not is_generated(p.relative_to(SITE)) and p.name != "404.html"]


def generated_pages():
    return [p for p in pages if is_generated(p.relative_to(SITE)) and p.name != "404.html"]


def tag(text, pattern):
    return re.findall(pattern, text, re.S)


pages = sorted(p for p in SITE.rglob("*.html") if not SKIP & set(p.relative_to(SITE).parts))

# --- original checks: em dash, broken links, /en/ twin, sitemap membership ---
for path in pages + [p for p in (SITE / "README.md", SITE / "sitemap.xml") if p.exists()]:
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "—" in line:
            err(f"{path.relative_to(SITE)}:{n}: em dash")

for page in pages:
    for target in LINK.findall(page.read_text(encoding="utf-8")):
        if not target or re.match(r"[a-z]+:", target):
            continue  # external, mailto or same-page anchor
        base = SITE if target.startswith("/") else page.parent
        dest = (base / target.lstrip("/")).resolve()
        if dest.is_dir():
            dest = dest / "index.html"
        if not dest.exists():
            err(f"{page.relative_to(SITE)}: broken link {target}")

sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
for page in pages:
    rel = page.relative_to(SITE)
    if rel.name == "404.html" or is_generated(rel):
        continue
    url = page_url(rel)
    if f"<loc>{url}</loc>" not in sitemap:
        err(f"{rel}: missing from sitemap.xml ({url})")
    if rel.parts[0] != "en" and not (SITE / "en" / rel).exists():
        err(f"{rel}: no English twin at en/{rel}")

# --- SEO checks (docs/seo/checklist.md) ---
texts = {p: p.read_text(encoding="utf-8") for p in pages}
ALL = own_pages() + generated_pages()


def canonical_of(text):
    m = tag(text, r'<link rel="canonical" href="([^"]+)"')
    return m


def hreflangs_of(text):
    return {h: u for h, u in tag(text, r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"')}


# C-01 canonical: single, absolute, trailing slash, equal to the page URL
for p in ALL:
    rel = p.relative_to(SITE)
    c = canonical_of(texts[p])
    if len(c) != 1 or c[0] != page_url(rel) or not c[0].endswith("/"):
        err(f"C-01 {rel}: canonical {c} (expected [{page_url(rel)}])")

# C-02 hreflang: es/en/x-default, self in group, twin group identical,
# x-default -> Spanish version, own hreflang matches <html lang>
for p in ALL:
    rel = p.relative_to(SITE)
    text = texts[p]
    group = hreflangs_of(text)
    lang = tag(text, r'<html lang="([^"]+)"')[0]
    url = page_url(rel)
    if set(group) != {"es", "en", "x-default"}:
        err(f"C-02 {rel}: hreflang set {sorted(group)}")
        continue
    if group.get(lang) != url:
        err(f"C-02 {rel}: hreflang {lang} points to {group.get(lang)}")
    if group["x-default"] != group["es"]:
        err(f"C-02 {rel}: x-default {group['x-default']} != es {group['es']}")
    twin = SITE / "en" / rel if rel.parts[0] != "en" else SITE / rel.relative_to("en")
    if twin.exists() and hreflangs_of(texts[twin]) != group:
        err(f"C-02 {rel}: twin {twin.relative_to(SITE)} has a different hreflang group")

# C-03 / W-01 titles: present, unique site-wide, 30..65 chars
titles = {}
for p in ALL:
    rel = p.relative_to(SITE)
    t = tag(texts[p], r"<title>([^<]*)</title>")
    if len(t) != 1:
        err(f"C-03 {rel}: {len(t)} <title> tags")
        continue
    titles.setdefault(t[0], []).append(rel)
    n = len(t[0])
    if p in own_pages() and not 30 <= n <= 65:
        err(f"C-03 {rel}: title is {n} chars")
    elif p in generated_pages() and not 30 <= n <= 65:
        warn(f"W-01 {rel}: title is {n} chars (H-B3, fix in Garaticker)")
for t, where in titles.items():
    if len(where) > 1:
        err(f"C-03: duplicated title {t!r} in {where}")

# C-04 description: present, unique, 50..160 chars (own and generated)
descs = {}
for p in ALL:
    rel = p.relative_to(SITE)
    d = tag(texts[p], r'<meta name="description" content="([^"]*)"')
    if len(d) != 1:
        err(f"C-04 {rel}: {len(d)} meta descriptions")
        continue
    descs.setdefault(d[0], []).append(rel)
    if not 50 <= len(d[0]) <= 160:
        err(f"C-04 {rel}: description is {len(d[0])} chars")
for d, where in descs.items():
    if len(where) > 1:
        err(f"C-04: duplicated description in {where}")

# C-05 Open Graph / Twitter (own and generated)
for p in ALL:
    rel = p.relative_to(SITE)
    text = texts[p]
    og = dict(tag(text, r'<meta property="(og:[^"]+)" content="([^"]*)"'))
    tw = dict(tag(text, r'<meta name="(twitter:[^"]+)" content="([^"]*)"'))
    lang = tag(text, r'<html lang="([^"]+)"')[0]
    for key in ("og:title", "og:description", "og:url", "og:image", "og:image:alt", "og:locale"):
        if key not in og:
            err(f"C-05 {rel}: missing {key}")
    if og.get("og:url") != page_url(rel):
        err(f"C-05 {rel}: og:url {og.get('og:url')} != canonical")
    img = og.get("og:image", "")
    if img.startswith(BASE + "/"):
        if not (SITE / img[len(BASE) + 1:]).exists():
            err(f"C-05 {rel}: og:image {img} not in the build")
    elif img:
        err(f"C-05 {rel}: og:image not absolute: {img}")
    want_locale = "es_ES" if lang == "es" else "en_GB"
    if og.get("og:locale") != want_locale:
        err(f"C-05 {rel}: og:locale {og.get('og:locale')} != {want_locale}")
    if "twitter:card" not in tw:
        err(f"C-05 {rel}: missing twitter:card")

# C-06 headings and images (own pages only; generated are Garaticker's, H-B6/H-B7)
for p in own_pages():
    rel = p.relative_to(SITE)
    text = texts[p]
    if len(tag(text, r"<h1[ >]")) != 1:
        err(f"C-06 {rel}: {len(tag(text, r'<h1[ >]'))} <h1> tags")
    for img in tag(text, r"<img ([^>]*)>"):
        if not re.search(r'alt="', img):
            err(f"C-06 {rel}: <img> without alt: {img[:60]}")
        if not (re.search(r'width="', img) and re.search(r'height="', img)):
            err(f"C-06 {rel}: <img> without width/height: {img[:60]}")

# C-07 sitemap: every <loc> exists, hreflang links match the page, lastmod reliable
for m in re.finditer(r"<url>(.*?)</url>", sitemap, re.S):
    block = m.group(1)
    loc = re.search(r"<loc>([^<]+)</loc>", block).group(1)
    rel = url_to_rel(loc)
    if rel is None or not (SITE / rel).exists():
        err(f"C-07: sitemap loc {loc} has no file in the build")
        continue
    page_group = {h: u for h, u in tag(block, r'<xhtml:link rel="alternate" hreflang="([^"]+)" href="([^"]+)"')}
    if page_group != hreflangs_of(texts[SITE / rel]):
        err(f"C-07: sitemap hreflang of {loc} differs from the page")
    lastmod = re.search(r"<lastmod>([^<]+)</lastmod>", block)
    if lastmod:
        try:
            out = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%cs", "--", rel],
                                 capture_output=True, text=True, timeout=10)
            if out.returncode == 0 and out.stdout.strip() and out.stdout.strip() > lastmod.group(1):
                # aviso, no error: lastmod solo debe reflejar cambios de contenido
                # visible (H-M1); legal cambió de cabeceras (OG, 24-nov) sin lastmod
                warn(f"C-07 {loc}: lastmod {lastmod.group(1)} is older than its last commit {out.stdout.strip()}")
        except Exception:
            pass  # no git: skip

# C-08 noindex: only on 404 pages
for p in pages:
    rel = p.relative_to(SITE)
    has_noindex = 'content="noindex' in texts[p] or "content='noindex" in texts[p]
    if rel.name == "404.html":
        if not has_noindex:
            err(f"C-08 {rel}: 404 page without noindex")
    elif f"<loc>{page_url(rel)}</loc>" in sitemap and has_noindex:
        err(f"C-08 {rel}: sitemap page with noindex")

# C-09 robots.txt: no Disallow with path, three sitemaps that exist, no AI-bot block
robots_path = SITE / "robots.txt"
if robots_path.exists():
    robots = robots_path.read_text(encoding="utf-8")
    for n, line in enumerate(robots.splitlines(), 1):
        if re.match(r"Disallow:\s*\S", line, re.I):
            err(f"C-09 robots.txt:{n}: Disallow with path ({line.strip()})")
        if re.search(r"GPTBot|OAI-SearchBot", line, re.I):
            err(f"C-09 robots.txt:{n}: mentions an AI bot ({line.strip()})")
    smaps = re.findall(r"Sitemap:\s*(\S+)", robots, re.I)
    if len(smaps) != 3:
        err(f"C-09 robots.txt: {len(smaps)} sitemaps listed (expected 3)")
    for s in smaps:
        rel = url_to_rel(s.rstrip("/") + "/") if s.rstrip("/") != BASE else None
        if s.endswith(".xml"):
            rel = s[len(BASE) + 1:] if s.startswith(BASE + "/") else None
        if rel is None or not (SITE / rel).exists():
            err(f"C-09: sitemap {s} from robots.txt not in the build")

# C-10 JSON-LD: valid JSON; on / and /en/ Organization + WebSite; publisher ids resolve
ids = set()
for p in ALL:
    rel = p.relative_to(SITE)
    for block in tag(texts[p], r'<script type="application/ld\+json">(.*?)</script>'):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            err(f"C-10 {rel}: invalid JSON-LD ({e})")
            continue
        for node in data if isinstance(data, list) else [data]:
            if isinstance(node, dict) and "@id" in node:
                ids.add(node["@id"])
for p in (SITE / "index.html", SITE / "en" / "index.html"):
    if not p.exists():
        continue
    types = [json.loads(b) for b in tag(texts[p], r'<script type="application/ld\+json">(.*?)</script>')]
    by_type = {n.get("@type"): n for n in types if isinstance(n, dict)}
    org = by_type.get("Organization", {})
    web = by_type.get("WebSite", {})
    if org.get("@id") != BASE + "/#organization":
        err(f"C-10 {p.relative_to(SITE)}: Organization @id {org.get('@id')}")
    if web.get("@id") != BASE + "/#website":
        err(f"C-10 {p.relative_to(SITE)}: WebSite @id {web.get('@id')}")
    for n in types:
        pub = n.get("publisher", {}) if isinstance(n, dict) else {}
        if isinstance(pub, dict) and pub.get("@id") and pub["@id"] not in ids:
            err(f"C-10 {p.relative_to(SITE)}: publisher {pub['@id']} does not resolve")
    for key in ("logo", "image", "url"):
        v = org.get(key)
        if isinstance(v, str) and v.startswith(BASE + "/") and not (SITE / v[len(BASE) + 1:]).exists():
            err(f"C-10 {p.relative_to(SITE)}: Organization {key} {v} not in the build")

# C-11 sameAs: identical in / and /en/, no WhatsApp, no GIPHY while D-07 is open
def sameas_of(p):
    for block in tag(texts[p], r'<script type="application/ld\+json">(.*?)</script>'):
        data = json.loads(block)
        if isinstance(data, dict) and data.get("@type") == "Organization":
            return data.get("sameAs", [])
    return None

sa_es, sa_en = sameas_of(SITE / "index.html"), sameas_of(SITE / "en" / "index.html")
if sa_es is not None and sa_es != sa_en:
    err(f"C-11: sameAs differs between / ({sa_es}) and /en/ ({sa_en})")
for sa in (sa_es, sa_en):
    for u in sa or []:
        if any(b in u for b in BLOCKED_SAMEAS):
            err(f"C-11: blocked profile in sameAs: {u}")

# C-12 fixed URLs: /tabaibi/ and /en/tabaibi/ with their canonicals
for rel, canon in (("tabaibi/index.html", BASE + "/tabaibi/"), ("en/tabaibi/index.html", BASE + "/en/tabaibi/")):
    p = SITE / rel
    if not p.exists():
        err(f"C-12: missing {rel}")
    elif canonical_of(texts[p]) != [canon]:
        err(f"C-12 {rel}: canonical {canonical_of(texts[p])} != [{canon}]")

# C-13 nothing of garaticker/artists and no Garaticker privacy page published
gar = SITE / "garaticker"
if gar.exists():
    extra = [e.name for e in gar.iterdir() if e.name not in ("index.html", "help")]
    if extra:
        err(f"C-13: unexpected under garaticker/: {extra} (artists guide and privacy stay out)")

# C-14 no internal link to index.html or to a folder without trailing slash
for p in own_pages():
    rel = p.relative_to(SITE)
    for target in LINK.findall(texts[p]):
        if not target or re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        last = target.rstrip("/").rsplit("/", 1)[-1]
        if target.endswith("index.html") or ("." not in last and not target.endswith("/")):
            err(f"C-14 {rel}: link to {target} (H-B1: use the folder with trailing slash)")

# C-15 vendored brand copies (styles/brand, img/brand, fonts) in sync with
# brand/ (decision 0004). Only when brand/ exists next to the repo; CI
# checks out this repo alone and skips it. Running sync_brand.sh refreshes
# the copies, so any diff against HEAD means they were stale.
if SITE == REPO and (REPO.parent / "brand").is_dir():
    try:
        subprocess.run(["sh", str(REPO / "scripts" / "sync_brand.sh")],
                       check=True, capture_output=True, timeout=60)
        out = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--",
                              "styles/brand", "img/brand", "fonts"],
                             capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            err("C-15: styles/brand, img/brand or fonts/ differ from brand/ after "
                "scripts/sync_brand.sh; commit the refreshed copies (decision 0004)")
    except Exception as e:
        err(f"C-15: could not verify the brand copies ({e})")

# W-02 page weight: own HTML under 100 KB; images under 300 KB except og-image
for p in own_pages():
    if p.stat().st_size > 100 * 1024:
        warn(f"W-02 {p.relative_to(SITE)}: {p.stat().st_size // 1024} KB of HTML")
imgdir = SITE / "img"
if imgdir.exists():
    for f in imgdir.rglob("*"):
        if f.is_file() and f.stat().st_size > 300 * 1024 and "og-image" not in f.name:
            warn(f"W-02 {f.relative_to(SITE)}: {f.stat().st_size // 1024} KB")

# W-03 target=_blank without rel=noopener (all pages)
for p in pages:
    rel = p.relative_to(SITE)
    for a in tag(texts[p], r'<a ([^>]*)>'):
        if 'target="_blank"' in a and "noopener" not in a:
            warn(f"W-03 {rel}: target=_blank without noopener")

# W-04 orphan own pages (in the sitemap but nothing links to them)
linked = set()
for p in pages:
    for target in LINK.findall(texts[p]):
        if not target or re.match(r"[a-z]+:", target):
            continue
        base = SITE if target.startswith("/") else p.parent
        dest = (base / target.lstrip("/")).resolve()
        if dest.is_dir():
            dest = dest / "index.html"
        if dest.exists():
            linked.add(dest)
for p in own_pages():
    if p.resolve() not in linked:
        warn(f"W-04 {p.relative_to(SITE)}: no internal links point here")


# --- live checks L-01..L-05 (docs/seo/checklist.md), run by hand after deploy ---
def fetch(url, ua=UA, redirect=True):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    handlers = [] if redirect else [NoRedirect()]
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode("utf-8", "replace")


def live_checks():
    # L-01 http, www and folder without slash: a single 301 to the canonical URL
    for url, want in (("http://sanchesque.com/", BASE + "/"),
                      ("https://www.sanchesque.com/", BASE + "/"),
                      (BASE + "/tabaibi", BASE + "/tabaibi/")):
        code, headers, _ = fetch(url, redirect=False)
        loc = urljoin(url, headers.get("Location", ""))
        if code != 301 or loc != want:
            err(f"L-01 {url}: {code} -> {loc} (expected 301 {want})")

    # L-02 invented path: real 404 with noindex
    code, _, body = fetch(BASE + "/no-existe-esto-404/", redirect=False)
    if code != 404 or "noindex" not in body:
        err(f"L-02 /no-existe-esto-404/: {code}, noindex={'noindex' in body}")

    # L-03 every URL of the three sitemaps answers 200 without redirect
    for smap in ("/sitemap.xml", "/garaticker/help/sitemap.xml", "/en/garaticker/help/sitemap.xml"):
        code, _, body = fetch(BASE + smap)
        if code != 200:
            err(f"L-03 sitemap {smap}: {code}")
            continue
        for loc in re.findall(r"<loc>([^<]+)</loc>", body):
            code, headers, _ = fetch(loc, redirect=False)
            if code != 200:
                err(f"L-03 {loc}: {code} -> {urljoin(loc, headers.get('Location', ''))}")

    # L-04 no request a page of the help loads a 404 (H-A1: .../help/*/sitemap.xml)
    for smap in ("/garaticker/help/sitemap.xml", "/en/garaticker/help/sitemap.xml"):
        _, _, body = fetch(BASE + smap)
        for loc in re.findall(r"<loc>([^<]+)</loc>", body):
            code, _, _ = fetch(loc + "sitemap.xml", redirect=False)
            if code == 404:
                err(f"L-04 {loc}sitemap.xml: 404 (H-A1)")
            elif code not in (200, 301):
                err(f"L-04 {loc}sitemap.xml: {code}")

    # L-05 search and AI bots get 200 on / and /robots.txt
    bots = ("Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot")
    for bot in bots:
        ua = UA if bot == "Googlebot" else f"{bot} (test)"
        if bot == "Googlebot":
            ua = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        if bot == "Bingbot":
            ua = "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
        for path in ("/", "/robots.txt"):
            code, _, _ = fetch(BASE + path, ua=ua)
            if code != 200:
                err(f"L-05 {bot} {path}: {code}")


if LIVE:
    live_checks()

for w in warnings:
    print(f"aviso: {w}")
if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    sys.exit(1)
print(f"ok: {len(pages)} pages checked, {len(warnings)} warnings"
      + (", live checks L-01..L-05 passed" if LIVE else ""))
sys.exit(0)
