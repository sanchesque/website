#!/bin/sh
# Copy the published files, and only those, into _site/, the only folder Workers serves.
# An allowlist on purpose: a new internal file (README, HANDOFF, AGENTS...)
# stays private unless it is added here.
#   scripts/build_site.sh
set -eu
cd "$(dirname "$0")/.."
rm -rf _site
mkdir -p _site/scripts
cp -R index.html 404.html robots.txt sitemap.xml \
      en garaticker tabaibi legal fonts img styles _site/
cp _headers speculationrules.json _site/
cp scripts/lang.js scripts/lang-redirect.js _site/scripts/
# Workers: 301 (not its default 307) from /folder to /folder/, as GitHub Pages does
(cd _site && find . -mindepth 2 -name index.html | sort | sed 's#^\./\(.*\)/index.html$#/\1 /\1/ 301#') > _site/_redirects
echo "built _site/"
