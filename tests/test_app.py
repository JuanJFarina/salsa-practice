import tkinter as tk

from salsabeat.app import SalsaBeatCoachApp
from salsabeat.models import ScheduledEvent
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


def test_reset_session_restores_ready_state(monkeypatch) -> None:
    sync_calls = 0
    stop_calls = 0

    def fake_sync_tts_cache(audio_dir, clip_names):
        nonlocal sync_calls
        sync_calls += 1
        return TtsCacheSyncReport(
            required_clips=tuple(clip_names),
            generated_clips=(),
            deleted_files=(),
        )

    def fake_preload(self, clip_names) -> None:
        return None

    def fake_stop_all(self) -> None:
        nonlocal stop_calls
        stop_calls += 1

    monkeypatch.setattr("salsabeat.app.sync_tts_cache", fake_sync_tts_cache)
    monkeypatch.setattr("salsabeat.app.AudioPlayer.preload", fake_preload)
    monkeypatch.setattr("salsabeat.app.AudioPlayer.stop_all", fake_stop_all)

    root = tk.Tk()
    root.withdraw()
    try:
        app = SalsaBeatCoachApp(root)
        app.tap_button.state(["disabled"])
        app.tap_progress_var.set("Tap 16/16")
        app.bpm_var.set("Estimated BPM: 200.0")
        app.current_step_var.set("Current Step: Básico")
        app.status_var.set("Dance now: Básico")
        app.measure_duration = 1.5
        app.pending_events.append(
            ScheduledEvent(scheduled_time=1.0, kind="spoken_cue", clip_name="uno")
        )

        app.reset_session()

        assert sync_calls == 2
        assert stop_calls == 1
        assert app.tap_tracker.taps == ()
        assert app.tap_tracker.locked is False
        assert app.pending_events == []
        assert app.measure_duration is None
        assert app.current_sequence is None
        assert app.tap_progress_var.get() == "Tap 0/16"
        assert app.bpm_var.get() == "Estimated BPM: --"
        assert app.current_step_var.get() == "Current Step: waiting for session start"
        assert app.status_var.get() == "Ready: tap 16 times on salsa counts 1 and 5."
        assert "disabled" not in app.tap_button.state()
    finally:
        root.destroy()
