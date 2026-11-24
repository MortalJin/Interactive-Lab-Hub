# The Era Phonograph
# Turn the dial to tune through NYC history. Static between eras,
# a clip fades in when you land on an era. The PiTFT shows the year.
#
# Run: python era_phonograph.py
# Clips go in clips/ as <year>.ogg (made by prepare_audio.py).
# Captions come from eras.json.

import glob, json, os, time
import pygame

# Step 1: settings
STEPS_PER_ERA = 4          # dial clicks from one era to the next
CLIP_VOL = {0: 1.0, 1: 0.35, 2: 0.0, 3: 0.35}   # how clear the clip is at each click
HERE = os.path.dirname(os.path.abspath(__file__))

# Step 2: load the eras from the clips folder
files = sorted(glob.glob(os.path.join(HERE, "clips", "*.ogg")))
eras = [(int(os.path.basename(f)[:4]), f) for f in files]
if not eras:
    raise SystemExit("No clips found. Put files like clips/1925.ogg in the clips folder.")
captions = {}
if os.path.exists(os.path.join(HERE, "eras.json")):
    for y, cfg in json.load(open(os.path.join(HERE, "eras.json"))).items():
        captions[y] = cfg if isinstance(cfg, str) else cfg.get("caption", "")
print("Eras:", [y for y, _ in eras], "| turn clockwise to go forward in time")

# Step 3: audio (static loops on one channel, the clip on another)
pygame.mixer.init(frequency=22050, channels=1)
static = pygame.mixer.Sound(os.path.join(HERE, "static.wav"))
static_ch = pygame.mixer.Channel(0)
clip_ch = pygame.mixer.Channel(1)
static_ch.play(static, loops=-1)
sounds = {}

def play_era(i):
    year, path = eras[i]
    if path not in sounds:
        sounds[path] = pygame.mixer.Sound(path)
    clip_ch.play(sounds[path], loops=-1, fade_ms=600)

# Step 4: input (Qwiic rotary encoder, or the two PiTFT buttons as backup)
import board, digitalio
encoder = None
try:
    from adafruit_seesaw import seesaw, rotaryio
    ss = seesaw.Seesaw(board.I2C(), addr=0x36)
    encoder = rotaryio.IncrementalEncoder(ss)
    print("Using the rotary encoder.")
except Exception as e:
    print("No encoder, using the PiTFT buttons instead:", e)
btn_back = digitalio.DigitalInOut(board.D24); btn_back.switch_to_input(pull=digitalio.Pull.UP)
btn_fwd = digitalio.DigitalInOut(board.D23); btn_fwd.switch_to_input(pull=digitalio.Pull.UP)

# Step 5: display (Mini PiTFT)
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
bl = digitalio.DigitalInOut(board.D22); bl.switch_to_output(); bl.value = True
disp = st7789.ST7789(board.SPI(), cs=digitalio.DigitalInOut(board.D5),
                     dc=digitalio.DigitalInOut(board.D25), rst=None, baudrate=64000000,
                     width=135, height=240, x_offset=53, y_offset=40, rotation=90)
W, H = 240, 135
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
big = ImageFont.truetype(FONT, 56)
small = ImageFont.truetype(FONT, 16)
AMBER, DIM = (255, 176, 0), (90, 60, 0)

def fit_caption(d, text):
    """Shrink the caption until it fits; wrap to two lines if it is still too long."""
    for size in (16, 14, 12):
        f = ImageFont.truetype(FONT, size)
        if d.textbbox((0, 0), text, font=f)[2] <= W - 12:
            return [text], f
    f = ImageFont.truetype(FONT, 12)
    words, lines = text.split(), [""]
    for w in words:
        test = (lines[-1] + " " + w).strip()
        if d.textbbox((0, 0), test, font=f)[2] <= W - 12:
            lines[-1] = test
        else:
            lines.append(w)
    return lines[:2], f

def draw(year, caption, signal):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    text = str(year)
    box = d.textbbox((0, 0), text, font=big)
    d.text(((W - box[2]) / 2, 14), text, font=big, fill=AMBER if signal > 0.9 else DIM)
    lines, f = fit_caption(d, caption)
    y = 84 if len(lines) == 1 else 80
    for line in lines:
        box = d.textbbox((0, 0), line, font=f)
        d.text(((W - box[2]) / 2, y), line, font=f, fill=AMBER)
        y += box[3] + 2
    for i in range(10):   # signal bar like an old tuning meter
        color = AMBER if i < signal * 10 else (40, 30, 0)
        d.rectangle((40 + i * 16, 118, 52 + i * 16, 128), fill=color)
    disp.image(img)

# Step 6: main loop
pos, current, last_shown, last_raw = 0, None, None, None
max_pos = (len(eras) - 1) * STEPS_PER_ERA
last_btn = 0
try:
    while True:
        # read the dial (only the change since last time, so turning past
        # either end doesn't leave "hidden" clicks you have to undo)
        if encoder:
            raw = -encoder.position
            if last_raw is None:
                last_raw = raw
            pos += raw - last_raw
            last_raw = raw
        elif time.time() - last_btn > 0.15:
            if not btn_fwd.value:
                pos += 1; last_btn = time.time()
            elif not btn_back.value:
                pos -= 1; last_btn = time.time()
        pos = max(0, min(max_pos, pos))
        p = pos

        # nearest era and how far off-center the dial is
        i, off = divmod(p, STEPS_PER_ERA)
        if off > STEPS_PER_ERA // 2 and i + 1 < len(eras):
            i, off = i + 1, off - STEPS_PER_ERA
        vol = CLIP_VOL[off % STEPS_PER_ERA]
        clip_ch.set_volume(vol)
        static_ch.set_volume(1.0 - 0.85 * vol)
        if i != current:
            play_era(i)
            current = i

        # rolling year between eras
        base, nxt = p // STEPS_PER_ERA, min(p // STEPS_PER_ERA + 1, len(eras) - 1)
        y0, y1 = eras[base][0], eras[nxt][0]
        year = round(y0 + (y1 - y0) * (p % STEPS_PER_ERA) / STEPS_PER_ERA)
        caption = captions.get(str(eras[i][0]), "") if vol >= 1.0 else "~ ~ ~"
        shown = (year, caption, vol)
        if shown != last_shown:
            draw(year, caption, vol)
            last_shown = shown
        time.sleep(0.03)
except KeyboardInterrupt:
    pygame.mixer.stop()
    disp.image(Image.new("RGB", (W, H), (0, 0, 0)))
