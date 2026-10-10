"""Generates an elegant, ambient electronic audio bed (110 BPM) and crisp UI SFX
for spatial showcase films using numpy and python's built-in wave module + ffmpeg.
Run: python synth-audio.py [output_dir]"""
import os, struct, subprocess, sys
import numpy as np

def generate_audio(out_dir):
    audio_dir = os.path.join(out_dir, "assets", "audio")
    sfx_dir = os.path.join(audio_dir, "sfx")
    os.makedirs(sfx_dir, exist_ok=True)

    sr = 44100
    bpm = 110
    beat_dur = 60.0 / bpm  # ~0.5454s
    total_sec = 47.0
    total_samples = int(sr * total_sec)
    t = np.linspace(0, total_sec, total_samples, endpoint=False)

    # 1. Base ambient drone / chord progression (Fm - Ab - Eb - Db in 110 BPM)
    drone = 0.25 * np.sin(2 * np.pi * 65.41 * t) + 0.15 * np.sin(2 * np.pi * 130.81 * t)
    # Slow filter sweep / swell
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * (1.0 / 8.0) * t)
    drone *= swell

    # 2. Rhythmic warm pulse on each beat
    beat_pulse = np.zeros(total_samples, dtype=np.float32)
    beat_samples = int(sr * beat_dur)
    env_beat = np.exp(-np.linspace(0, 8, beat_samples))
    for b in range(int(total_sec / beat_dur)):
        idx = int(b * beat_samples)
        if idx + beat_samples <= total_samples:
            freq = 110.0 if b % 4 == 0 else 165.0
            sig = np.sin(2 * np.pi * freq * np.linspace(0, beat_dur, beat_samples)) * env_beat
            beat_pulse[idx:idx + beat_samples] += 0.20 * sig

    # 3. Soft high-frequency shimmer / hi-hat tick every quarter beat
    sub_tick = np.zeros(total_samples, dtype=np.float32)
    sub_dur = beat_dur / 4.0
    sub_samples = int(sr * sub_dur)
    noise = np.random.normal(0, 1, sub_samples)
    noise_env = np.exp(-np.linspace(0, 30, sub_samples))
    tick_sig = noise * noise_env
    for s in range(int(total_sec / sub_dur)):
        idx = int(s * sub_samples)
        if idx + sub_samples <= total_samples:
            sub_tick[idx:idx + sub_samples] += (0.04 if s % 4 != 0 else 0.08) * tick_sig

    mix = drone + beat_pulse + sub_tick
    # Fade in / fade out
    fade_len = int(sr * 1.5)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    mix[:fade_len] *= fade_in
    mix[-fade_len:] *= fade_out

    # Normalize to -3dB
    mix = mix / (np.max(np.abs(mix)) + 1e-6) * 0.70
    int16_audio = (mix * 32767).astype(np.int16)

    # Stereo interleaving
    stereo = np.empty((total_samples, 2), dtype=np.int16)
    stereo[:, 0] = int16_audio
    stereo[:, 1] = int16_audio

    bgm_path = os.path.join(audio_dir, "bgm-edit.wav")
    import wave
    with wave.open(bgm_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())
    print(f"Generated BGM: {bgm_path}")

    # SFX Generation using ffmpeg lavfi
    sfx_defs = {
        "click.mp3": "sine=frequency=1200:duration=0.08,afade=t=out:st=0.02:d=0.06",
        "whoosh.mp3": "anoisesrc=d=0.35:c=pink:r=44100,lowpass=f=1800,afade=t=in:st=0:d=0.1,afade=t=out:st=0.15:d=0.2",
        "pop.mp3": "sine=frequency=750:duration=0.12,afade=t=out:st=0.02:d=0.10",
        "punch.mp3": "sine=frequency=140:duration=0.25,afade=t=out:st=0.05:d=0.20",
        "impact.mp3": "sine=frequency=90:duration=0.45,afade=t=out:st=0.08:d=0.37",
        "stamp.mp3": "sine=frequency=280:duration=0.18,afade=t=out:st=0.03:d=0.15",
    }
    for fname, lavfi in sfx_defs.items():
        out_f = os.path.join(sfx_dir, fname)
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", lavfi, "-q:a", "2", out_f],
                       capture_output=True, check=True)
        print(f"Generated SFX: {out_f}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_audio(target)
