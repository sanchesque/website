#!/bin/sh
# Rastreo semanal en vivo de sanchesque.com (subsesión «Sanchesque.com · SEO»).
# Corre check_site.py --live y guarda la salida con fecha (UTC) en docs/seo/.
# ALERTA (exit 2) si fallan L-03 (URL de las sitemaps) o L-04 (404 que pide
# la ayuda de Garaticker, H-A1). Pensado para un cron semanal; también vale
# a mano tras cualquier despliegue.
#   scripts/seo_weekly.sh
set -u
cd "$(dirname "$0")/.."
out="docs/seo/live-$(date -u +%Y-%m-%d).txt"
python3 scripts/check_site.py --live > "$out" 2>&1
code=$?
echo "guardado: $out (exit $code)"
if grep -q 'ERROR: L-0[34]' "$out"; then
  echo "ALERTA SEO: fallan L-03/L-04:" >&2
  grep 'ERROR: L-0[34]' "$out" >&2
  exit 2
fi
exit "$code"
