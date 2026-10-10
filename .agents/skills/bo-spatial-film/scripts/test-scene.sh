#!/usr/bin/env bash
# Lint + snapshot ONE scene in its isolated harness (never touches the shared index.html).
# Run from the film project root:  bash <skill>/scripts/test-scene.sh <scene_id> "<t1,t2,...>"
# Snapshots: .hyperframes/test/<id>/snaps/frame-NN-at-Xs.png + contact-sheet.jpg (read the sheet first).
set -u
id="$1"; times="$2"
[ -f film.json ] || { echo "run from the film project root (film.json not found)"; exit 1; }
V=$(node -p "require('./film.json').hyperframes")
T=".hyperframes/test/$id"
[ -d "$T" ] || { echo "no harness for $id - run: python <skill>/scripts/make-harness.py"; exit 1; }
[ -f "compositions/$id.html" ] || { echo "compositions/$id.html not written yet"; exit 1; }
cp "compositions/$id.html" "$T/compositions/$id.html"
echo "== lint $id"
npx --yes "hyperframes@$V" lint "$T" 2>&1 | tail -40
echo "== snapshot $id at $times"
rm -rf "$T/snaps"
npx --yes "hyperframes@$V" snapshot "$T" --at "$times" --no-end --describe false -o "$T/snaps" 2>&1 | tail -6
