#!/bin/sh
# Refresh the copies of the studio brand (sanchesque/brand) that this site
# serves. GitHub Pages only publishes this repo, so the files are vendored;
# never edit them here: change brand/ and run this script.
#   scripts/sync_brand.sh [path/to/brand]   (default: ../brand)
set -eu
BRAND=${1:-"$(dirname "$0")/../../brand"}
SITE="$(dirname "$0")/.."
cp "$BRAND/dist/sanchesque.css" "$SITE/styles/brand/sanchesque.css"
for f in favicon.svg favicon.ico apple-touch-icon.png og-image.png; do
  cp "$BRAND/logos/sanchesque/favicon/$f" "$SITE/img/brand/$f"
done
for v in primary horizontal; do
  cp "$BRAND/logos/sanchesque/svg/sanchesque-$v-black.svg" "$SITE/img/brand/"
done
mkdir -p "$SITE/fonts/manrope"
# web files only; brand also keeps desktop TTFs in ttf/
cp "$BRAND/fonts/manrope/"*.woff2 "$BRAND/fonts/manrope/manrope.css" "$BRAND/fonts/manrope/OFL.txt" "$SITE/fonts/manrope/"
# raster logo for structured data (search engines expect PNG/JPG)
cp "$BRAND/logos/sanchesque/png/sanchesque-primary-black-500.png" "$SITE/img/brand/"
# Tabaibi product page: logo, raster logo and social preview
mkdir -p "$SITE/img/brand/tabaibi"
cp "$BRAND/logos/tabaibi/svg/tabaibi-primary-color.svg" \
   "$BRAND/logos/tabaibi/png/tabaibi-primary-color-500.png" "$SITE/img/brand/tabaibi/"
cp "$BRAND/logos/tabaibi/favicon/og-image.png" "$SITE/img/brand/tabaibi/og-image.png"
# Garaticker product page: logo and raster logo for structured data (decision 0016), social preview
mkdir -p "$SITE/img/brand/garaticker"
cp "$BRAND/logos/garaticker/svg/garaticker-primary-black.svg" \
   "$BRAND/logos/garaticker/png/garaticker-primary-black-500.png" "$SITE/img/brand/garaticker/"
cp "$BRAND/logos/garaticker/favicon/og-image.png" "$SITE/img/brand/garaticker/og-image.png"
# email templates (brand/email/): mail clients block SVG, so they load these PNGs from here
mkdir -p "$SITE/img/brand/email"
cp "$BRAND/logos/sanchesque/png/sanchesque-horizontal-black-1000.png" \
   "$BRAND/logos/tabaibi/png/tabaibi-horizontal-white-1000.png" "$SITE/img/brand/email/"
echo "synced brand files from $BRAND"
