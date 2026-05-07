"""Sequence loading and compatibility rules."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from .models import Sequence


class SequenceLibrary:
    """Loads and selects compatible sequences from ``sequences.json``."""

    def __init__(
        self,
        sequences: list[Sequence],
        *,
        default_position: str = "cerrada",
        rng: random.Random | None = None,
    ) -> None:
        if not sequences:
            raise ValueError("At least one sequence is required.")
        self.sequences = sequences
        self.default_position = default_position
        self._rng = rng or random.Random()

    @classmethod
    def from_path(
        cls,
        path: Path | str,
        *,
        default_position: str = "cerrada",
        rng: random.Random | None = None,
    ) -> "SequenceLibrary":
        sequence_path = Path(path)
        payload = json.loads(sequence_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("sequences.json must contain a JSON array.")

        sequences = [cls._parse_sequence(item) for item in payload]
        return cls(sequences, default_position=default_position, rng=rng)

    @staticmethod
    def _parse_sequence(item: Any) -> Sequence:
        if not isinstance(item, dict):
            raise ValueError("Each sequence entry must be an object.")

        required_keys = {"step", "eight_counts", "start_position", "end_position"}
        missing = required_keys - item.keys()
        if missing:
            raise ValueError(f"Sequence entry missing keys: {sorted(missing)}")

        step = item["step"]
        eight_counts = item["eight_counts"]
        start_position = item["start_position"]
        end_position = item["end_position"]

        if not isinstance(step, str):
            raise ValueError("Sequence step must be a string.")
        if not isinstance(eight_counts, int):
            raise ValueError("Sequence eight_counts must be an integer.")
        if not isinstance(start_position, str) or not isinstance(end_position, str):
            raise ValueError("Sequence positions must be strings.")

        return Sequence(
            step=step,
            eight_counts=eight_counts,
            start_position=start_position,
            end_position=end_position,
        )

    def clip_names(self) -> list[str]:
        return [sequence.step for sequence in self.sequences]

    def compatible_sequences(self, position: str) -> list[Sequence]:
        return [sequence for sequence in self.sequences if sequence.start_position == position]

    def any_position_sequences(self) -> list[Sequence]:
        return [sequence for sequence in self.sequences if sequence.start_position == "any"]

    def choose_initial(self) -> Sequence:
        try:
            return self.choose_next(self.default_position)
        except LookupError:
            return self._rng.choice(self.sequences)

    def choose_next(self, current_position: str) -> Sequence:
        candidates = self.compatible_sequences(current_position)
        if candidates:
            return self._rng.choice(candidates)

        wildcard_candidates = self.any_position_sequences()
        if wildcard_candidates:
            return self._rng.choice(wildcard_candidates)

        if current_position != self.default_position:
            fallback_candidates = self.compatible_sequences(self.default_position)
            if fallback_candidates:
                return self._rng.choice(fallback_candidates)

        raise LookupError(
            f"No sequence starts at position '{current_position}' and no fallback is available."
        )
