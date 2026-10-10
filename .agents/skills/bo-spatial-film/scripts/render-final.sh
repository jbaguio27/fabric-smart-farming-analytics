#!/usr/bin/env bash
# Final render from the CLI with the hardware GPU path, logged to a file, then verified with ffprobe.
# Run from the film project root:  bash <skill>/scripts/render-final.sh <name> [extra render args, e.g. --resolution 4k]
# Launch it with run_in_background and read renders/<name>.log for progress (never pipe through | tail).
# If you stop it, kill the node process tree (Windows: taskkill /T /F /PID <pid>; macOS/Linux: pkill -f "hyperframes.*render")
# - stopping only the shell leaves the render running.
set -u
name="${1:-film-1080p60}"; shift || true
[ -f film.json ] || { echo "run from the film project root"; exit 1; }
V=$(node -p "require('./film.json').hyperframes"); FPS=$(node -p "require('./film.json').fps")
mkdir -p renders
log="renders/$name.log"
start=$(date +%s)
npx --yes "hyperframes@$V" render --fps "$FPS" --browser-gpu --workers 6 -o "renders/$name.mp4" "$@" > "$log" 2>&1
code=$?
echo "exit $code after $(( $(date +%s) - start ))s - log $log"
mode=$(grep -o -m1 '"browserGpuMode":"[a-z]*"' "$log" | cut -d'"' -f4)
[ "$mode" = "hardware" ] && echo "gpu mode: hardware" || echo "WARNING: gpu mode '${mode:-unknown}' - expected hardware (software is ~15x slower)"
[ -f "renders/$name.mp4" ] && ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames:format=duration,size -of default=nw=1 "renders/$name.mp4"
exit $code
