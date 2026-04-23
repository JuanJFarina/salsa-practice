from salsabeat.models import Sequence
from salsabeat.timeline import (
    build_lead_in,
    initial_sequence_announcement_time,
    initial_sequence_start_time,
    sequence_announcement_time,
    sequence_end_time,
)


def test_lead_in_starts_one_measure_after_final_tap() -> None:
    lead_in = build_lead_in(final_tap_time=10.0, measure_duration=1.5)

    assert [cue.name for cue in lead_in] == ["uno", "cinco", "uno"]
    assert [cue.scheduled_time for cue in lead_in] == [11.5, 13.0, 14.5]


def test_initial_sequence_announcement_happens_on_count_five_before_start() -> None:
    assert initial_sequence_announcement_time(final_tap_time=10.0, measure_duration=1.5) == 16.0


def test_initial_sequence_starts_after_lead_in() -> None:
    assert initial_sequence_start_time(final_tap_time=10.0, measure_duration=1.5) == 17.5


def test_sequence_timing_uses_final_cycle_count_five() -> None:
    sequence = Sequence(
        step="Setenta",
        eight_counts=2,
        start_position="closed",
        end_position="closed",
    )

    assert sequence_announcement_time(100.0, 1.0, sequence) == 103.0
    assert sequence_end_time(100.0, 1.0, sequence) == 104.0
