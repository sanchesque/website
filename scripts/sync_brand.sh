#!/bin/sh
# Refresh the copies of the studio brand (sanchesque/brand) that this site
# serves. GitHub Pages only publishes this repo, so the files are vendored;
# never edit them here: change brand/ and run this script.
#   scripts/sync_brand.sh [path/to/brand]   (default: ../brand)
set -eu
BRAND=${1:-"$(dirname "$0")/../../brand"}
SITE="$(dirname "$0")/.."
cp "$BRAND/dist/sanchesque.css" "$SITE/styles/brand/sanchesque.css"
for f in favicon.svg favicon.ico apple-touch-icon.png; do
  cp "$BRAND/logos/sanchesque/favicon/$f" "$SITE/img/brand/$f"
done
cp "$BRAND/logos/sanchesque/svg/sanchesque-primary-black.svg" "$SITE/img/brand/"
echo "synced brand files from $BRAND"
