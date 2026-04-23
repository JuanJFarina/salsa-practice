from salsabeat.tempo import TapTempoTracker


def test_tracker_locks_after_twelve_measure_spaced_taps() -> None:
    tracker = TapTempoTracker(required_taps=12, min_tap_interval=0.2)

    result = None
    for index in range(12):
        result = tracker.register_tap(timestamp=index * 1.2)

    assert result is not None
    assert result.accepted is True
    assert result.snapshot.locked is True
    assert result.snapshot.tap_count == 12
    assert result.snapshot.measure_duration == 1.2
    assert result.snapshot.beat_duration == 0.3
    assert result.snapshot.bpm == 200.0


def test_tracker_ignores_accidental_double_tap() -> None:
    tracker = TapTempoTracker(required_taps=12, min_tap_interval=0.3)

    tracker.register_tap(timestamp=1.0)
    double_tap = tracker.register_tap(timestamp=1.1)

    assert double_tap.accepted is False
    assert double_tap.ignored_reason == "double_tap"
    assert double_tap.snapshot.tap_count == 1
