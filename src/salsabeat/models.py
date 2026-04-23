"""Core dataclasses for the SalsaBeat Coach domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

EventKind = Literal["spoken_cue", "announce_next_sequence", "start_sequence"]


@dataclass(frozen=True, slots=True)
class Sequence:
    """A dance sequence loaded from ``sequences.json``."""

    step: str
    eight_counts: int
    start_position: str
    end_position: str

    def __post_init__(self) -> None:
        if not self.step.strip():
            raise ValueError("Sequence step cannot be empty.")
        if self.eight_counts < 1:
            raise ValueError("Sequence eight_counts must be >= 1.")
        if not self.start_position.strip() or not self.end_position.strip():
            raise ValueError("Sequence positions cannot be empty.")

    @property
    def duration_measures(self) -> int:
        return self.eight_counts * 2


@dataclass(frozen=True, slots=True)
class Cue:
    """A spoken cue such as 'cinco' or 'uno' scheduled in absolute time."""

    name: str
    scheduled_time: float


@dataclass(frozen=True, slots=True)
class TempoSnapshot:
    """A snapshot of the current tap-tempo state."""

    tap_count: int
    measure_duration: float | None
    beat_duration: float | None
    bpm: float | None
    locked: bool


@dataclass(frozen=True, slots=True)
class TapResult:
    """Result of attempting to record a tap."""

    accepted: bool
    ignored_reason: str | None
    snapshot: TempoSnapshot
    final_tap_time: float | None = None


@dataclass(order=True, frozen=True, slots=True)
class ScheduledEvent:
    """A timed action processed by the Tk event loop."""

    scheduled_time: float
    kind: EventKind = field(compare=False)
    clip_name: str | None = field(default=None, compare=False)
    sequence: Sequence | None = field(default=None, compare=False)


@dataclass(slots=True)
class SessionState:
    """Mutable UI-facing state for a single practice run."""

    status: str = "Ready to calibrate."
    tap_count: int = 0
    bpm: float | None = None
    current_step: str = "Waiting for lead-in"
    locked: bool = False
