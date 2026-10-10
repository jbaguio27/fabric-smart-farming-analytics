"""Word timestamps from ElevenLabs Scribe. Key from env EL. Usage: python el-words.py <audio> <out.json>"""
import json, os, sys, requests

r = requests.post("https://api.elevenlabs.io/v1/speech-to-text",
    headers={"xi-api-key": os.environ["EL"]},
    data={"model_id": "scribe_v1", "language_code": "en", "timestamps_granularity": "word"},
    files={"file": open(sys.argv[1], "rb")}, timeout=300)
r.raise_for_status()
words = [{"w": w["text"], "s": round(w["start"], 3), "e": round(w["end"], 3)}
         for w in r.json()["words"] if w.get("type") == "word"]
json.dump(words, open(sys.argv[2], "w", encoding="utf-8"), indent=0)
print(" ".join(f'{x["w"]}@{x["s"]}' for x in words))
