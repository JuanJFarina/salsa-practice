# Technical Specification: "SalsaBeat Coach"

## 1. Overview
A Windows desktop application built in Python that helps the user practice salsa on1 by dictating dance sequences in time with music. For V1, the app does not perform automatic BPM detection. Instead, the user calibrates the tempo manually by tapping a single button eight times on the salsa landmark counts (`1` and `5`).

After the final tap, the app plays a short spoken lead-in (`one`, `five`, `one`) to give the user time to get ready. The first sequence name is then spoken on the next count `5`, and the dancer starts that sequence on the following count `1`. After that, the app dictates randomized sequences loaded from a JSON file.

The application is optimized for short 1-2 minute practice sessions. If the song or timing changes, the expected workflow is to restart the session and recalibrate.

## 2. Tech Stack
* **Language:** Python 3.10+
* **GUI:** `tkinter`
* **Timing:** `time.perf_counter()` for high-resolution timestamps and scheduling
* **TTS Generation:** `pyttsx3` (offline)
* **Audio Playback:** Windows `winsound` for playback of pre-generated `.wav` clips
* **Data Storage:** `JSON`
* **Cached Audio Directory:** `assets/audio/tts/`

## 3. Functional Requirements

### 3.1. Manual Tempo Capture
* The UI exposes a single primary button labeled **"This is the one!"**.
* The user must tap the button **8 times** on alternating salsa landmark counts (`1`, `5`, `1`, `5`, ...).
* Each tap records a timestamp using a high-resolution clock.
* Consecutive taps are treated as being **one 4-beat measure apart**, so the tempo is derived as:
  * `measure_duration = average_time_between_taps`
  * `beat_duration = measure_duration / 4`
  * `BPM = 60 / beat_duration = 240 / measure_duration`
* The app should display tap progress (for example, `Tap 3/8`) and the estimated BPM once enough taps have been recorded.
* Taps that are too close together should be ignored to reduce accidental double-taps.
* After the 8th tap, the button is disabled for the remainder of the session.

### 3.2. Synchronization and Lead-In
* After the 8th tap, the app locks the tempo and starts a spoken lead-in.
* Because the 8th tap lands on count `5`, the lead-in consists of the cues **"one"**, **"five"**, **"one"**, spaced **one measure apart**.
* The purpose of the lead-in is to give the user time to begin dancing and verify that the app feels synchronized with the music.
* After that lead-in, the app announces the first sequence name on the next count `5`.
* The dancer begins the first sequence on the following count `1`.
* For V1, this startup phrase is fixed and not user-configurable.
* The implementation should define the calibration phase so that the spoken cues and first-step announcement start on the correct landmark counts after the final tap.

### 3.3. Sequence Engine
* The app reads a `sequences.json` file.
* Each entry contains:
  * `step`: the name of the sequence to speak
  * `eight_counts`: the number of full 8-beat salsa cycles that the sequence lasts
  * `start_position`: the logical position required to begin the sequence
  * `end_position`: the logical position produced when the sequence ends
* The session starts from a default logical position such as `neutral`.
* The app selects the next sequence randomly from the set of sequences whose `start_position` matches the current `end_position`.
* If no compatible sequence exists, the app may fall back to a recovery rule such as:
  * selecting a sequence with `start_position: "any"`
  * resetting the logical position to a default state such as `neutral`
* A newly selected sequence starts on count `1`.
* To give the dancer time to react, the next sequence should be announced before it starts. For V1, the preferred trigger point is count `5` of the final cycle of the current sequence.

### 3.4. TTS Asset Pipeline
* Spoken audio should be generated **ahead of time** and saved to disk.
* The app should **not** synthesize TTS live during a practice session.
* At minimum, the application must have cached audio clips for:
  * `one`
  * `five`
  * every sequence name present in `sequences.json`
* Missing audio clips may be generated at startup or by a separate utility script.
* The recommended output format is `.wav` for simple and predictable playback on Windows.
* During practice, the app only queues and plays pre-generated audio files from `assets/audio/tts/`.

## 4. Data Schema (`sequences.json`)
```json
[
  {
    "step": "Basic Step",
    "eight_counts": 1,
    "start_position": "neutral",
    "end_position": "neutral"
  },
  {
    "step": "Cross Body Lead",
    "eight_counts": 1,
    "start_position": "closed",
    "end_position": "open"
  },
  {
    "step": "Right Turn",
    "eight_counts": 1,
    "start_position": "open",
    "end_position": "open"
  },
  {
    "step": "Dile que no",
    "eight_counts": 1,
    "start_position": "open",
    "end_position": "closed"
  },
  {
    "step": "Setenta",
    "eight_counts": 2,
    "start_position": "closed",
    "end_position": "closed"
  }
]
```

## 5. UI Requirements (Tkinter)
* **Primary Button:** **"This is the one!"** used for the 8 calibration taps
* **Button State:** Shows progress and becomes disabled after tap 8
* **Labels:** Display session status, estimated BPM, and the name of the current step
* **Minimal UI:** No extra configuration controls are required for V1
* **Reset Behavior:** Restarting the application resets the session

## 6. Future Enhancement (Optional)
* A future hybrid mode may estimate BPM from Windows system audio (for example via WASAPI loopback) while still keeping manual synchronization through the final tap flow.
