"""Generate SCRIPT.md narration with ElevenLabs. Key from env EL. Usage: python el-tts.py <film_dir> name=voice_id ..."""
import json, os, sys, urllib.request

film = sys.argv[1]
txt = open(os.path.join(film, 'SCRIPT.md'), encoding='utf-8').read()
lines = [l[4:] for l in txt.splitlines() if l.startswith('    ') and l.strip()]
text = "\n\n".join(lines)
out = os.path.join(film, 'src', 'audio', 'voice-candidates')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'script.txt'), 'w', encoding='utf-8').write(text)
print(len(text), 'chars')
for pair in sys.argv[2:]:
    name, vid = pair.split('=')
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ['EL'], "Content-Type": "application/json"})
    open(os.path.join(out, f'{name}.mp3'), 'wb').write(urllib.request.urlopen(req).read())
    print('ok', name)
