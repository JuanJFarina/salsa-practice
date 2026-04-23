"""Timeline helpers for lead-in and sequence scheduling."""

from __future__ import annotations

from .models import Cue, Sequence

LEAD_IN_CUES = ("uno", "cinco", "uno")
FIRST_LEAD_IN_DELAY_MEASURES = 1
INITIAL_SEQUENCE_ANNOUNCEMENT_DELAY_MEASURES = 3
INITIAL_SEQUENCE_ANNOUNCEMENT_DELAY_BEATS = 3
INITIAL_SEQUENCE_START_DELAY_MEASURES = 5


def build_lead_in(final_tap_time: float, measure_duration: float) -> list[Cue]:
    """Build the fixed lead-in after the calibration taps.

    The final calibration tap lands on count ``5``. The lead-in therefore begins one
    measure later on count ``1`` and continues as ``uno, cinco, uno``.
    """

    if measure_duration <= 0:
        raise ValueError("measure_duration must be > 0.")

    return [
        Cue(
            name=cue_name,
            scheduled_time=(
                final_tap_time + (FIRST_LEAD_IN_DELAY_MEASURES + index) * measure_duration
            ),
        )
        for index, cue_name in enumerate(LEAD_IN_CUES)
    ]


def initial_sequence_start_time(final_tap_time: float, measure_duration: float) -> float:
    """Start the first dance sequence on the count 1 after its count 5 announcement."""

    if measure_duration <= 0:
        raise ValueError("measure_duration must be > 0.")
    return final_tap_time + INITIAL_SEQUENCE_START_DELAY_MEASURES * measure_duration


def initial_sequence_announcement_time(final_tap_time: float, measure_duration: float) -> float:
    """Announce the first sequence on beat 4 before the next count 5."""

    if measure_duration <= 0:
        raise ValueError("measure_duration must be > 0.")
    beat_duration = measure_duration / 4
    return (
        final_tap_time
        + INITIAL_SEQUENCE_ANNOUNCEMENT_DELAY_MEASURES * measure_duration
        + INITIAL_SEQUENCE_ANNOUNCEMENT_DELAY_BEATS * beat_duration
    )


def sequence_announcement_time(
    sequence_start_time: float, measure_duration: float, sequence: Sequence
) -> float:
    """Announce the next sequence on beat 4 of the current sequence's final cycle."""

    if measure_duration <= 0:
        raise ValueError("measure_duration must be > 0.")
    beat_duration = measure_duration / 4
    return sequence_start_time + (sequence.duration_measures - 1) * measure_duration - beat_duration


def sequence_end_time(
    sequence_start_time: float, measure_duration: float, sequence: Sequence
) -> float:
    """Return the timestamp where a sequence hands off to the next one."""

    if measure_duration <= 0:
        raise ValueError("measure_duration must be > 0.")
    return sequence_start_time + sequence.duration_measures * measure_duration
