# Turns the raw clips into "old radio" clips, and makes the static sound.
# Put raw files in raw/, named by year (1924.mp3, 2026.m4a, ...).
# Set where each clip starts and how long it is in eras.json.
# Run: python prepare_audio.py

import glob, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "clips"), exist_ok=True)

# Step 1: read the settings
eras = json.load(open(os.path.join(HERE, "eras.json")))

def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)

# Step 2: radio static (8 s loop)
ffmpeg("-f", "lavfi", "-i", "anoisesrc=color=pink:duration=8:amplitude=0.35",
       "-af", "highpass=f=400,lowpass=f=4000", "-ar", "22050", "-ac", "1",
       os.path.join(HERE, "static.wav"))
print("made static.wav")

# Step 3: each clip -> cut, mono, narrow band like an old radio, same loudness
for path in sorted(glob.glob(os.path.join(HERE, "raw", "*"))):
    year = os.path.basename(path)[:4]
    if not year.isdigit():
        print("skip (name must start with a year):", path)
        continue
    cfg = eras.get(year, {})
    if isinstance(cfg, str):
        cfg = {}
    start, length = str(cfg.get("start", 0)), str(cfg.get("length", 60))
    # the newest era stays clear, the older ones sound like an old radio
    radio = "" if int(year) >= 2000 else "highpass=f=300,lowpass=f=3400,"
    ffmpeg("-ss", start, "-t", length, "-i", path,
           "-af", radio + "afade=t=in:d=0.5,loudnorm",
           "-ar", "22050", "-ac", "1", os.path.join(HERE, "clips", f"{year}.ogg"))
    print(f"made clips/{year}.ogg  (from {start}s, {length}s long)")

print("Done. Now run: python era_phonograph.py")
