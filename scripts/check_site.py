#!/usr/bin/env python3
"""Pre-push checks for the site: no em dashes, no broken internal links,
every Spanish page has its /en/ twin, and every page is in the sitemap.

    python3 scripts/check_site.py [dir]   (default: the repo; exit 1 on failure)

Run it on _site/ after scripts/build_site.sh to check what Pages publishes.
"""
import re
import sys
from pathlib import Path

SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKIP = {"fonts", ".git", ".github", "_site"}
LINK = re.compile(r'(?:href|src)="([^"#?]*)')
# copies built by Zensical in the product repos: they ship their own sitemap
GENERATED = ("garaticker/help", "garaticker/artists")

pages = sorted(p for p in SITE.rglob("*.html") if not SKIP & set(p.relative_to(SITE).parts))
errors = []

for path in pages + [p for p in (SITE / "README.md", SITE / "sitemap.xml") if p.exists()]:
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "—" in line:
            errors.append(f"{path.relative_to(SITE)}:{n}: em dash")

for page in pages:
    for target in LINK.findall(page.read_text(encoding="utf-8")):
        if not target or re.match(r"[a-z]+:", target):
            continue  # external, mailto or same-page anchor
        base = SITE if target.startswith("/") else page.parent
        dest = (base / target.lstrip("/")).resolve()
        if dest.is_dir():
            dest = dest / "index.html"
        if not dest.exists():
            errors.append(f"{page.relative_to(SITE)}: broken link {target}")

sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
for page in pages:
    rel = page.relative_to(SITE)
    if rel.name == "404.html" or any(g in str(rel) for g in GENERATED):
        continue
    url = "https://sanchesque.com/" + str(rel.parent).replace(".", "").strip("/")
    url = url.rstrip("/") + "/"
    if f"<loc>{url}</loc>" not in sitemap:
        errors.append(f"{rel}: missing from sitemap.xml ({url})")
    if rel.parts[0] != "en" and not (SITE / "en" / rel).exists():
        errors.append(f"{rel}: no English twin at en/{rel}")

print("\n".join(errors) or f"ok: {len(pages)} pages checked")
sys.exit(1 if errors else 0)
