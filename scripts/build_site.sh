#!/bin/sh
# Copy the published files, and only those, into _site/ (served by Pages and by Workers).
# An allowlist on purpose: a new internal file (README, HANDOFF, AGENTS...)
# stays private unless it is added here.
#   scripts/build_site.sh
set -eu
cd "$(dirname "$0")/.."
rm -rf _site
mkdir -p _site/scripts
cp -R index.html 404.html robots.txt sitemap.xml \
      en garaticker tabaibi legal fonts img styles _site/
cp _headers _site/
cp scripts/lang.js _site/scripts/
echo "built _site/"
