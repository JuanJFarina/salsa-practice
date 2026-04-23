"""Tap-based tempo capture for SalsaBeat Coach."""

from __future__ import annotations

import time
from collections.abc import Callable

from .models import TapResult, TempoSnapshot


class TapTempoTracker:
    """Collects measure-spaced taps and derives tempo from their average spacing."""

    def __init__(
        self,
        *,
        required_taps: int = 12,
        min_tap_interval: float = 0.35,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        if required_taps < 2:
            raise ValueError("required_taps must be >= 2.")
        if min_tap_interval <= 0:
            raise ValueError("min_tap_interval must be > 0.")
        self.required_taps = required_taps
        self.min_tap_interval = min_tap_interval
        self._clock = clock
        self._taps: list[float] = []
        self._locked = False

    @property
    def taps(self) -> tuple[float, ...]:
        return tuple(self._taps)

    @property
    def locked(self) -> bool:
        return self._locked

    def reset(self) -> None:
        self._taps.clear()
        self._locked = False

    def snapshot(self) -> TempoSnapshot:
        measure_duration: float | None = None
        beat_duration: float | None = None
        bpm: float | None = None

        if len(self._taps) >= 2:
            intervals = [
                later - earlier
                for earlier, later in zip(self._taps, self._taps[1:], strict=False)
            ]
            measure_duration = sum(intervals) / len(intervals)
            beat_duration = measure_duration / 4
            bpm = 60 / beat_duration

        return TempoSnapshot(
            tap_count=len(self._taps),
            measure_duration=measure_duration,
            beat_duration=beat_duration,
            bpm=bpm,
            locked=self._locked,
        )

    def register_tap(self, timestamp: float | None = None) -> TapResult:
        if self._locked:
            return TapResult(
                accepted=False,
                ignored_reason="session_locked",
                snapshot=self.snapshot(),
            )

        tap_time = self._clock() if timestamp is None else timestamp

        if self._taps and (tap_time - self._taps[-1]) < self.min_tap_interval:
            return TapResult(
                accepted=False,
                ignored_reason="double_tap",
                snapshot=self.snapshot(),
            )

        self._taps.append(tap_time)

        if len(self._taps) >= self.required_taps:
            self._locked = True

        return TapResult(
            accepted=True,
            ignored_reason=None,
            snapshot=self.snapshot(),
            final_tap_time=tap_time,
        )
