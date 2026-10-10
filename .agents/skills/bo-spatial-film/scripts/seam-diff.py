"""Show where a seam pair differs, OUTSIDE the presenter zone, so the overlay's own motion doesn't mask a real pop.

usage: py -3.12 seam-diff.py <a.png> <b.png> <out.png> [kape_box x0,y0,x1,y1]
Prints the % of pixels differing (>12/255) with and without the Kape zone, and writes a strip a | b | diff.
"""
import sys
import numpy as np
from PIL import Image

a, b = (np.asarray(Image.open(p).convert("RGB")).astype(np.int16) for p in sys.argv[1:3])
box = [int(v) for v in (sys.argv[4] if len(sys.argv) > 4 else "0,960,520,1920").split(",")]
d = np.abs(a - b).max(-1) > 12
mask = np.ones_like(d)
mask[box[1]:box[3], box[0]:box[2]] = False
print(f"all {d.mean() * 100:.2f}%  outside-kape {d[mask].mean() * 100:.2f}%")
heat = np.zeros_like(a, dtype=np.uint8)
heat[d] = (255, 40, 40)
strip = np.concatenate([a.astype(np.uint8), b.astype(np.uint8), heat], 1)
Image.fromarray(strip).resize((strip.shape[1] // 3, strip.shape[0] // 3)).save(sys.argv[3])
