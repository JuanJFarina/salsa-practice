import tkinter as tk

from salsabeat.app import SalsaBeatCoachApp
from salsabeat.audio import AudioPreflight


def test_start_session_schedules_correct_startup_phrase(monkeypatch) -> None:
    def fake_preflight(self, clip_names):
        return AudioPreflight(required_clips=tuple(clip_names), missing_clips=())

    def fake_preload(self, clip_names) -> None:
        return None

    monkeypatch.setattr("salsabeat.app.AudioPlayer.preflight", fake_preflight)
    monkeypatch.setattr("salsabeat.app.AudioPlayer.preload", fake_preload)

    root = tk.Tk()
    root.withdraw()
    try:
        app = SalsaBeatCoachApp(root)
        app._start_session(final_tap_time=10.0, measure_duration=1.5)

        scheduled_events = sorted(app.pending_events)
        assert [event.scheduled_time for event in scheduled_events] == [
            11.5,
            13.0,
            14.5,
            16.0,
            17.5,
        ]
        assert [event.kind for event in scheduled_events] == [
            "spoken_cue",
            "spoken_cue",
            "spoken_cue",
            "announce_next_sequence",
            "start_sequence",
        ]
        first_sequence = scheduled_events[4].sequence
        assert first_sequence is not None
        assert [event.clip_name for event in scheduled_events[:4]] == [
            "one",
            "five",
            "one",
            first_sequence.step,
        ]
        assert app.current_sequence is None
        assert app.current_step_var.get() == "Current Step: waiting for first step"
    finally:
        root.destroy()
