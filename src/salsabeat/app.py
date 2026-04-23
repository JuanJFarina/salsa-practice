"""Tkinter application for SalsaBeat Coach."""

from __future__ import annotations

import heapq
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from .audio import AudioPlayer, MissingAudioAssetError, required_clip_names
from .models import ScheduledEvent, Sequence, SessionState
from .sequences import SequenceLibrary
from .tempo import TapTempoTracker
from .timeline import (
    build_lead_in,
    initial_sequence_announcement_time,
    initial_sequence_start_time,
    sequence_announcement_time,
    sequence_end_time,
)
from .tts_cache import sync_tts_cache

ROOT_DIR = Path(__file__).resolve().parents[2]
SEQUENCES_PATH = ROOT_DIR / "sequences.json"
AUDIO_DIR = ROOT_DIR / "assets" / "audio" / "tts"
EVENT_POLL_MS = 25


class SalsaBeatCoachApp:
    """Desktop controller for the SalsaBeat Coach MVP."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SalsaBeat Coach")
        self.root.minsize(420, 260)

        self.sequence_library = SequenceLibrary.from_path(SEQUENCES_PATH)
        self.audio_player = AudioPlayer(AUDIO_DIR)
        self.tap_tracker = TapTempoTracker()
        self.state = SessionState()
        self.measure_duration: float | None = None
        self.pending_events: list[ScheduledEvent] = []
        self.current_sequence: Sequence | None = None

        self.status_var = tk.StringVar(
            value=f"Ready: tap {self.tap_tracker.required_taps} times on salsa counts 1 and 5."
        )
        self.tap_progress_var = tk.StringVar(value=f"Tap 0/{self.tap_tracker.required_taps}")
        self.bpm_var = tk.StringVar(value="Estimated BPM: --")
        self.current_step_var = tk.StringVar(value="Current Step: waiting for session start")

        self._build_ui()
        self._sync_audio_cache()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(EVENT_POLL_MS, self._process_pending_events)

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        title = ttk.Label(container, text="SalsaBeat Coach", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")

        status_label = ttk.Label(
            container,
            textvariable=self.status_var,
            wraplength=380,
            justify="left",
        )
        status_label.grid(row=1, column=0, sticky="ew", pady=(10, 12))

        self.tap_button = ttk.Button(container, text="This is the one!", command=self.handle_tap)
        self.tap_button.grid(row=2, column=0, sticky="ew", pady=(0, 16))

        ttk.Label(container, textvariable=self.tap_progress_var).grid(row=3, column=0, sticky="w")
        ttk.Label(container, textvariable=self.bpm_var).grid(
            row=4, column=0, sticky="w", pady=(6, 0)
        )
        ttk.Label(container, textvariable=self.current_step_var).grid(
            row=5, column=0, sticky="w", pady=(6, 0)
        )

    def _sync_audio_cache(self) -> None:
        clip_names = required_clip_names(self.sequence_library.sequences)
        self.status_var.set("Syncing cached audio...")
        self.root.update_idletasks()

        try:
            report = sync_tts_cache(AUDIO_DIR, clip_names)
            self.audio_player.preload(list(report.required_clips))
        except (MissingAudioAssetError, OSError, RuntimeError) as exc:
            self.status_var.set(f"Audio sync failed: {exc}")
            self.tap_button.state(["disabled"])
            return

        self.status_var.set(
            f"Ready: tap {self.tap_tracker.required_taps} times on salsa counts 1 and 5."
        )

    def handle_tap(self) -> None:
        result = self.tap_tracker.register_tap()

        if not result.accepted:
            if result.ignored_reason == "double_tap":
                self.status_var.set(
                    "Ignored a quick double-tap. Keep tapping on counts 1 and 5."
                )
            elif result.ignored_reason == "session_locked":
                self.status_var.set("Session already calibrated. Restart the app to recalibrate.")
            return

        self.state.tap_count = result.snapshot.tap_count
        self.state.bpm = result.snapshot.bpm
        self.state.locked = result.snapshot.locked

        self.tap_progress_var.set(
            f"Tap {result.snapshot.tap_count}/{self.tap_tracker.required_taps}"
        )
        if result.snapshot.bpm is not None:
            self.bpm_var.set(f"Estimated BPM: {result.snapshot.bpm:.1f}")

        if result.snapshot.locked and result.final_tap_time is not None:
            if result.snapshot.measure_duration is None:
                self.status_var.set("Not enough tap data to start the session.")
                return
            self.tap_button.state(["disabled"])
            self._start_session(result.final_tap_time, result.snapshot.measure_duration)
            return

        self.status_var.set("Tap the next 1 or 5 landmark.")

    def _start_session(self, final_tap_time: float, measure_duration: float) -> None:
        self.measure_duration = measure_duration
        self.current_sequence = None
        first_sequence = self.sequence_library.choose_initial()
        self.current_step_var.set("Current Step: waiting for first step")
        self.status_var.set("Lead-in started: listen for uno, cinco, uno.")

        for cue in build_lead_in(final_tap_time, measure_duration):
            self._push_event(
                ScheduledEvent(
                    scheduled_time=cue.scheduled_time,
                    kind="spoken_cue",
                    clip_name=cue.name,
                )
            )

        announce_time = initial_sequence_announcement_time(final_tap_time, measure_duration)
        self._push_event(
            ScheduledEvent(
                scheduled_time=announce_time,
                kind="announce_next_sequence",
                clip_name=first_sequence.step,
                sequence=first_sequence,
            )
        )

        start_time = initial_sequence_start_time(final_tap_time, measure_duration)
        self._push_event(
            ScheduledEvent(
                scheduled_time=start_time,
                kind="start_sequence",
                sequence=first_sequence,
            )
        )

    def _push_event(self, event: ScheduledEvent) -> None:
        heapq.heappush(self.pending_events, event)

    def _process_pending_events(self) -> None:
        now = time.perf_counter()
        while self.pending_events and self.pending_events[0].scheduled_time <= now:
            event = heapq.heappop(self.pending_events)
            try:
                self._handle_event(event)
            except Exception as exc:
                self.pending_events.clear()
                self.status_var.set(f"Timed event failed: {exc}")
                self.current_step_var.set("Current Step: session stopped")
                self.audio_player.stop_all()
                break
        self.root.after(EVENT_POLL_MS, self._process_pending_events)

    def _handle_event(self, event: ScheduledEvent) -> None:
        if event.kind == "spoken_cue" and event.clip_name:
            self.audio_player.play(event.clip_name)
            self.status_var.set(f"Lead-in cue: {event.clip_name}")
            return

        if event.kind == "announce_next_sequence" and event.sequence and event.clip_name:
            self.audio_player.play(event.clip_name)
            self.status_var.set(f"Up next: {event.sequence.step}")
            return

        if event.kind == "start_sequence" and event.sequence:
            self._begin_sequence(event.sequence, event.scheduled_time)

    def _begin_sequence(self, sequence: Sequence, start_time: float) -> None:
        if self.measure_duration is None:
            raise RuntimeError("measure_duration must be set before sequences can start.")

        self.current_sequence = sequence
        self.current_step_var.set(f"Current Step: {sequence.step}")
        self.status_var.set(f"Dance now: {sequence.step}")

        next_sequence = self.sequence_library.choose_next(sequence.end_position)
        self._push_event(
            ScheduledEvent(
                scheduled_time=sequence_announcement_time(
                    start_time, self.measure_duration, sequence
                ),
                kind="announce_next_sequence",
                clip_name=next_sequence.step,
                sequence=next_sequence,
            )
        )
        self._push_event(
            ScheduledEvent(
                scheduled_time=sequence_end_time(start_time, self.measure_duration, sequence),
                kind="start_sequence",
                sequence=next_sequence,
            )
        )

    def _on_close(self) -> None:
        self.audio_player.stop_all()
        self.root.destroy()


def main() -> int:
    root = tk.Tk()
    SalsaBeatCoachApp(root)
    root.mainloop()
    return 0
