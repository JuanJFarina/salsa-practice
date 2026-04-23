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
2. Tap the button 16 times on the landmark counts `1`, `5`, `1`, `5`, ...
3. Confirm:
   * Tap progress reaches `Tap 16/16`
   * The estimated BPM updates during tapping
   * The button becomes disabled after tap 16

## Lead-In And Dictation
1. After tap 16, confirm the app plays:
   * `uno`
   * `cinco`
   * `uno`
2. Confirm the first step name is spoken on beat `4`, just before the next count `5`.
3. Confirm the current step label switches from the waiting state to an actual step on the following count `1`.
4. Keep dancing through at least 3 step changes.
5. Confirm each next step is spoken before the transition.

## Recovery And Restart
1. Click **Reset** during or after a session.
2. Confirm the app returns to the initial ready state.
3. Confirm tap progress returns to `Tap 0/16` and the tap button is active again.
4. If timing drifts or the song changes, press **Reset** and recalibrate.
