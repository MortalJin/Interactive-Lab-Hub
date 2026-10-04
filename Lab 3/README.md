# Chatterboxes

**Yangchen Jin**

---

# Part 1

## A. Text to Speech

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*

I created [`greet_yangchen.sh`](speech-scripts/greet_yangchen.sh) to have the Pi greet me using different TTS voices.

\*\***Then answer: Is the same greeting, in these different voices, the same greeting? Describe one concrete way the voice changed what the utterance seemed to mean or who seemed to be speaking.**\*\*

The words were the same, but the greeting did not feel the same. One voice was less clear and sounded slightly tired or reluctant, which made the greeting feel almost forced. The clearer voice sounded more confident and consistent, so it felt like a fully formed machine speaking to me rather than an uncertain person.

## B. Speech to Text

\*\***Record a few seconds of your own speech (`arecord -d 5 -f cd -c 1 -r 16000 test.wav`) and transcribe it with at least two model sizes. Report the real-time factor for each. At what point does the accuracy improvement stop being worth the delay, for a system that has to answer you?**\*\*

\*\***Write your own script that verbally asks for a numerical input (a phone number, zipcode, number of pets) and records the answer the respondent provides.**\*\* Numbers are a good stress test — transcription systems make characteristic errors on digit strings, and you will want to know what they are before you design around them.

## C. Turn-taking: knowing when someone has stopped talking

Everything so far has worked on fixed audio files. A real conversational device does not get told when to start and stop recording — it has to decide. This is the problem that makes speech interfaces hard, and it is mostly not a speech recognition problem.

We use a **voice activity detector** (VAD) to segment the microphone stream into utterances. `listen.py` runs Silero VAD continuously and hands each detected utterance to faster-whisper:

```
(.venv) $ cd speech-scripts
(.venv) $ python listen.py
```

Speak, pause, and watch it transcribe. Now change the endpointing threshold — the amount of silence the system requires before it decides your turn is over:

```
(.venv) $ python listen.py --min-silence 0.2
(.venv) $ python listen.py --min-silence 1.5
```

\*\***Try both extremes, and something in between. Describe what each one feels like to talk to. Note specifically: at 0.2s, what kinds of normal speech get cut off? At 1.5s, what does the delay make the system seem like?**\*\*

There is no correct value. A system that takes drink orders and a system that listens to someone think out loud want very different thresholds, and the right one depends on what your users are doing with their pauses.

### The complete loop

`echo_bot.py` puts the pieces together: it listens, endpoints, transcribes, and speaks a reply through Piper. The dialogue policy is deliberately trivial — it repeats what you said — so that everything you notice is a property of the timing rather than the content.

```
(.venv) $ python echo_bot.py
```

## D. Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.)

\*\***Post your storyboard and diagram here.**\*\*

## SATOR SQUARE Storyboard

*Speak now. Hear yourself later.*

<img width="428" height="348" alt="393e4957a9f310c57f0d86d54e2ca6f5" src="https://github.com/user-attachments/assets/87b9518e-0406-4f91-b689-022bdbb97bc6" />

*A voice interface that allows users to speak with a simulated future version of themselves and leave messages that return at a later point in time.*

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f974ae2e-d20f-41c4-87da-39649dc14f90" />




\*\***Please describe and document your process.**\*\*

**SATOR SQUARE:** Select a return point: tomorrow, one month, or one year.

**User:** One month.

**SATOR SQUARE:** Temporal channel open. This is a simulated connection to yourself one month from now. Tell me about a decision you have not been able to make.

**User:** I am unsure whether I should commit to something that may not succeed.

*After the user stops speaking, the device waits for 0.8 seconds of silence before ending the turn.*

**SATOR SQUARE:** I heard that you are deciding whether to commit to something that may not succeed. Is that correct?

*The device waits for the user’s confirmation. If the user remains silent for five seconds, it says, “Take your time. The line is still open.”*

**User:** Yes.

*The Wizard listens to the dilemma and selects one appropriate reflection card.*

**Simulated Future Self:** I cannot tell you what happened. What would you regret not doing?

**User:** I would regret never finding out what I was capable of.

*After the user stops speaking, the device waits for 0.8 seconds of silence before sealing the answer.*

**SATOR SQUARE:** Your answer has been sealed. Return date: October 27, 2026. You will hear your own voice again in one month. Connection closed.

### Alternative Response Cards

- **Regret:** What would you regret not doing?
- **Fear:** Are you choosing this because you want it, or because you fear the alternative?
- **Control:** Which part of this decision is still under your control?
- **Identity:** Which choice is closer to the person you want to become?
- **Time:** Will this still matter to you one year from now?


## E. Acting out the dialogue

https://youtu.be/3asdAFzKRhc

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

When I acted out the interaction, the opening instructions felt clear and natural. The problem appeared when SATOR SQUARE asked the user a reflective question. The question was broad and slightly abstract, so the participant was not sure how to respond. This showed me two possible directions: the question should either be simpler and more universal, or more personalized based on what the user has just said. I also started to question what the returned message means after one month. During the first interaction, the question already creates a useful moment of reflection. However, simply replaying the recording one month later may feel like only a time capsule. To give the return more meaning, the device could ask the user to compare their past concern with how they feel now, turning the message into evidence of change rather than just an old recording.


---

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings.
2. What are other modes of interaction *beyond speech* that you might also use to clarify how to interact? In particular: how does someone know when the device is listening, and when it is thinking? You have a screen and an LED.
3. Make a new storyboard, diagram and/or script based on these reflections.
4. (optional) Integrate [input devices](inputs.md) in the system

## Prototype your system

The system should:
* use the Raspberry Pi
* use one or more sensors
* require participants to speak to it

*Document how the system works.*

*Include videos or screencaptures of both the system and the controller.*

## Test the system

Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard *after* the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?
\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?
\*\**your answer here*\*\*

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?
\*\**your answer here*\*\*

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
