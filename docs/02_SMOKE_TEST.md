# Windows Smoke Test Checklist

## Setup
1. Install dependencies:
   * `python -m pipenv install --dev`
2. Make sure `sequences.json` contains the steps you want to practice.

## Launch
1. Start the desktop app:
   * `python -m pipenv run python -m salsabeat`
2. Confirm the window shows:
   * The **"This is the one!"** button
   * A ready status message
   * Tap progress, BPM, and current step labels
3. If you changed `sequences.json`, confirm startup finishes without an audio-cache error.

## Calibration Flow
1. Play a metronome or salsa track on the same computer.
2. Tap the button 12 times on the landmark counts `1`, `5`, `1`, `5`, ...
3. Confirm:
   * Tap progress reaches `Tap 12/12`
   * The estimated BPM updates during tapping
   * The button becomes disabled after tap 12

## Lead-In And Dictation
1. After tap 12, confirm the app plays:
   * `uno`
   * `cinco`
   * `uno`
2. Confirm the first step name is spoken on the next count `5`.
3. Confirm the current step label switches from the waiting state to an actual step on the following count `1`.
4. Keep dancing through at least 3 step changes.
5. Confirm each next step is spoken before the transition.

## Recovery And Restart
1. Close and reopen the app.
2. Confirm the session resets to the initial ready state.
3. If timing drifts or the song changes, restart and recalibrate.
