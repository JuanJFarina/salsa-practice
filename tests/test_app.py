import tkinter as tk

from salsabeat.app import SalsaBeatCoachApp
from salsabeat.tts_cache import TtsCacheSyncReport


def test_start_session_schedules_correct_startup_phrase(monkeypatch) -> None:
    def fake_sync_tts_cache(audio_dir, clip_names):
        return TtsCacheSyncReport(
            required_clips=tuple(clip_names),
            generated_clips=(),
            deleted_files=(),
        )

    def fake_preload(self, clip_names) -> None:
        return None

    monkeypatch.setattr("salsabeat.app.sync_tts_cache", fake_sync_tts_cache)
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
            15.625,
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
            "uno",
            "cinco",
            "uno",
            first_sequence.step,
        ]
        assert app.current_sequence is None
        assert app.current_step_var.get() == "Current Step: waiting for first step"
    finally:
        root.destroy()
