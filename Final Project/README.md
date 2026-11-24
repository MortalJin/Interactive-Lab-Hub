# The Era Phonograph
 
**Yangchen Jin (yj645)**
 
Turn the dial and tune through New York's history. Between eras you hear radio static. When you land on an era, a sound from that time fades in, and the little screen shows the year, like the frequency on an old radio.
 
**Help and influences:** My SATOR SQUARE project from Lab 3. Feedback from Prof. ___ on my first concept. Claude (AI) helped with debugging, the code, and organizing this README. My early sketches and notes were done by hand without AI.
 
---
 
## 1. Project Plan
 
### Big Idea
A radio-style device that lets people "tune in" to different eras of New York. Most people know a bit of the city's history, but reading about it doesn't give you a feeling of being there. Hearing the music, voices, and news of a time can do that in a few seconds. Most people at the showcase live in New York, so hearing their own city in another era makes it personal.
 
### Timeline
| Date | Goal |
|---|---|
| Nov 9 | First concept submitted (photos + events + narration) |
| Nov 11 | Feedback, changed to audio-first radio |
| By Nov 26 | Collect clips, core loop working: dial → static → clip |
| By Nov 30 | Cardboard prototype, first user test |
| Week of Dec 1 | Functional check-off, laser-cut enclosure |
| Dec 4–5 | Final enclosure, second user test |
| Dec 7 | Showcase |
 
### Parts
- Raspberry Pi 5
- Adafruit I2C rotary encoder (the dial)
- Mini PiTFT 240×135 (year display, its two buttons are the backup dial)
- USB speaker (the Pi 5 has no headphone jack)
- Laser-cut cardboard / wood enclosure
### Fall-back Plan
- If the encoder is not detected, the two PiTFT buttons step back and forward in time. (This already happened to me with Qwiic in Lab 6, so I built it in from the start.)
- If smooth fading is too hard, jump between eras with a short burst of static.
- If there is no good recording for an era, a synthetic voice with radio static reads one line about it.
- If the display fails, the years are engraved on the dial itself.
---
 
## 2. How the Idea Evolved
 
<img width="1800" height="660" alt="image" src="https://github.com/user-attachments/assets/c96dfa6f-383d-4fd5-8e08-525e1fbf0716" />

### v0: "Something about time"
My SATOR SQUARE project in Lab 3 got me interested in time. My first thought was a general "time machine" you could ask about any year. Honestly, at this stage it was a generative AI chatbot with a costume on.
 
*Problem:* too broad. Any year, any place, and nothing that makes it feel physical.
 
### v1: NYC Time Machine
I narrowed it to New York, because everyone at the showcase knows the city. I listed what you could "get back" from a year:
 
- a postcard written from that year
- an old radio broadcast
- street sounds of the time
- old photos
- a conversation with someone from that year
I dropped the conversation. Speech-to-text, a language model, and text-to-speech in a row would be too slow on a Pi, and people would get bored waiting.
 
### v2: Photo + Event + Old Radio Voice (submitted Nov 9)
Turn a knob to pick a year, press "Go", see a real public-domain photo and the biggest event of that year, and hear an old-radio voice read it.
 
*Problem I already knew about:* in Lab 5, Qwen made up almost every fact about Roosevelt Island. A history machine that gets history wrong in front of New Yorkers is bad. So I planned "fact cards" I write myself, and the AI would only rewrite them in old newspaper style.
 
I also thought about a thermal printer that prints a "time travel ticket", but I don't have one, so it became a stretch goal (or a QR code).
 
### v3: The Era Phonograph (after feedback)
Feedback on v2: *"Does it need the photo? Maybe you just surf back and forward in time, and you hear clips from different eras."*
 
At first it felt like a downgrade, but I agree now:
- Picking a year and looking at a photo is like flipping through an album. **Tuning** through time, with static in between, makes the search itself the experience.
- Sound leaves room for imagination. People fill in the picture themselves.
- No big screen means fewer parts that can break, and more time for the enclosure.
What changed: no HDMI screen, no "Go" button. The Mini PiTFT only shows the year, like a radio frequency display. The name changed to **The Era Phonograph**.
 
---
 
## 3. How It Works
 
(architecture diagram)
 
1. The rotary encoder gives a dial position. Every 4 clicks is one era.
2. The dial position sets two volumes: the clip is loudest exactly on an era, and static is loudest halfway between eras.
3. When the nearest era changes, the new clip starts and fades in.
4. The PiTFT shows a rolling year between eras, a caption when tuned, and a signal bar.
### Code
- [era_phonograph.py](era_phonograph.py): main program
- [prepare_audio.sh](prepare_audio.sh): turns raw clips into narrow-band "old radio" audio and makes the static
- [eras.json](eras.json): the caption for each era
### How to set it up
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pygame adafruit-circuitpython-seesaw adafruit-circuitpython-rgb-display pillow
sudo apt install -y ffmpeg
mkdir raw          # put clips here, named by year, e.g. raw/1925.mp3
./prepare_audio.sh
sudo systemctl stop piscreen.service
python era_phonograph.py
```
 
### Sound clips
| Year | What | Source |
|---|---|---|
| ___ | ___ | ___ |
 
---
 
## 4. Enclosure
 
(laser cutting files and photos)
 
Before the final enclosure I practiced laser cutting with a parts box. Things I learned the hard way:
- On the Epilog, thick lines get engraved instead of cut. They need to be hairlines.
- On the Trotec, color decides cut vs. engrave (black = cut in our Maker Lab), and the material preset matters.
- Cardboard joints came out loose at burn 0.1, so I used a higher burn and wider fingers.
---
 
## 5. User Testing
 
### Test 1: cardboard prototype (date ___)
(video)
- **Who:** ___
- **Before trying:** ___
- **What surprised them:** ___
- **What they would change:** ___
- **What I changed after:** ___
### Test 2: final enclosure (date ___)
(video)
- **Who:** ___
- **Before trying:** ___
- **What surprised them:** ___
- **What they would change:** ___
---
 
## 6. Reflection
(write after testing)
