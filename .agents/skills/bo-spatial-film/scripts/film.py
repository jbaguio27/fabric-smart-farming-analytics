"""Shared loader for film.json (the one source of scene timing). Imported by assemble.py, make-harness.py
and seam-check.py; run every script from the film project root."""
import json, os, sys

ROOT = os.getcwd()


def load():
    p = os.path.join(ROOT, 'film.json')
    if not os.path.exists(p):
        sys.exit('film.json not found - run this from the film project root')
    f = json.load(open(p, encoding='utf-8'))
    beat = 60 / f['bpm']
    bar = beat * f.get('beats_per_bar', 4)
    scenes, t = [], 0.0
    for sid, bars in f['scenes']:
        if sid[0].isdigit():
            sys.exit(f'scene id {sid!r} starts with a digit - lint rejects it (use s01-...)')
        scenes.append({'id': sid, 'start': round(t, 4), 'dur': round(bars * bar, 4)})
        t += bars * bar
    f.update(beat=beat, bar=bar, total=round(t, 4), scene_list=scenes,
             starts={s['id']: s for s in scenes})
    return f


def cue_time(expr, f, k=None):
    """A cue time is seconds (1.09) or an expression in beats/bars: "4*b", "6*b+0.05", "2*b*k"."""
    if isinstance(expr, (int, float)):
        return float(expr)
    return float(eval(expr, {'__builtins__': {}}, {'b': f['beat'], 'bar': f['bar'], 'k': k}))


def hf(f):
    return f'hyperframes@{f["hyperframes"]}'
