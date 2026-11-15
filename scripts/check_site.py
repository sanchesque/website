#!/usr/bin/env python3
"""Pre-push checks for the site: no em dashes, no broken internal links,
every Spanish page has its /en/ twin, and every page is in the sitemap.

    python3 scripts/check_site.py      (exit code 1 if anything fails)
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SKIP = {"fonts", ".git", ".github"}
LINK = re.compile(r'(?:href|src)="([^"#?]*)')

pages = sorted(p for p in SITE.rglob("*.html") if not SKIP & set(p.relative_to(SITE).parts))
errors = []

for path in pages + [SITE / "README.md", SITE / "sitemap.xml"]:
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
    if rel.name == "404.html":
        continue
    url = "https://sanchesque.com/" + str(rel.parent).replace(".", "").strip("/")
    url = url.rstrip("/") + "/"
    if f"<loc>{url}</loc>" not in sitemap:
        errors.append(f"{rel}: missing from sitemap.xml ({url})")
    if rel.parts[0] != "en" and not (SITE / "en" / rel).exists():
        errors.append(f"{rel}: no English twin at en/{rel}")

print("\n".join(errors) or f"ok: {len(pages)} pages checked")
sys.exit(1 if errors else 0)
