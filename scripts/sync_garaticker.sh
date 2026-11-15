#!/bin/sh
# Copy the public Garaticker guides into this site. They are written in
# the Garaticker repo and built there with Zensical; this site only keeps
# the generated HTML (studio decision 0004). Never edit the copies here:
# change guides/ in Garaticker and run this script again.
#   scripts/sync_garaticker.sh help [artists]   (Garaticker repo: $GARATICKER,
#                                                default ../projects/garaticker/code)
set -eu
SITE="$(cd "$(dirname "$0")/.." && pwd)"
G=${GARATICKER:-"$SITE/../projects/garaticker/code"}
[ $# -gt 0 ] || { echo "usage: $0 help [artists]" >&2; exit 2; }
for s in "$@"; do
  case $s in help|artists) ;; *) echo "unknown guide: $s (help or artists)" >&2; exit 2 ;; esac
done

# strict build: broken links or em dashes stop here, before anything is copied
(cd "$G" && uv run garaticker docs)

# Only these four folders ever leave the Garaticker repo: site/internal/
# is never read. A draft (the legal review banner) refuses the whole sync.
for s in "$@"; do
  for src in "$G/site/garaticker/$s" "$G/site/en/garaticker/$s"; do
    [ -f "$src/index.html" ] || { echo "missing build: $src" >&2; exit 1; }
    if grep -rlE "Borrador pendiente|Draft pending" "$src" --include=*.html >&2; then
      echo "refusing: the files above are drafts pending legal review" >&2; exit 1
    fi
  done
done

for s in "$@"; do
  rsync -a --delete "$G/site/garaticker/$s/" "$SITE/garaticker/$s/"
  rsync -a --delete "$G/site/en/garaticker/$s/" "$SITE/en/garaticker/$s/"
done
echo "synced Garaticker guides: $*"
python3 "$SITE/scripts/check_site.py"
