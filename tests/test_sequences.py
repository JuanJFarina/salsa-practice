import json
import random

import pytest

from salsabeat.sequences import SequenceLibrary


def test_sequence_library_prefers_exact_position_match(tmp_path) -> None:
    payload = [
        {
            "step": "Basic Step",
            "eight_counts": 1,
            "start_position": "neutral",
            "end_position": "neutral",
        },
        {
            "step": "Cross Body Lead",
            "eight_counts": 1,
            "start_position": "closed",
            "end_position": "open",
        },
        {
            "step": "Shine Break",
            "eight_counts": 1,
            "start_position": "any",
            "end_position": "neutral",
        },
    ]
    path = tmp_path / "sequences.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    library = SequenceLibrary.from_path(path, rng=random.Random(0))

    assert library.choose_next("closed").step == "Cross Body Lead"


def test_sequence_library_uses_any_fallback_when_no_exact_match(tmp_path) -> None:
    payload = [
        {
            "step": "Basic Step",
            "eight_counts": 1,
            "start_position": "neutral",
            "end_position": "neutral",
        },
        {
            "step": "Shine Break",
            "eight_counts": 1,
            "start_position": "any",
            "end_position": "neutral",
        },
    ]
    path = tmp_path / "sequences.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    library = SequenceLibrary.from_path(path, rng=random.Random(0))

    assert library.choose_next("open").step == "Shine Break"


def test_sequence_library_can_choose_initial_without_neutral_start(tmp_path) -> None:
    payload = [
        {
            "step": "Básico",
            "eight_counts": 1,
            "start_position": "cerrada",
            "end_position": "cerrada",
        },
        {
            "step": "Dile que no",
            "eight_counts": 1,
            "start_position": "cerrada",
            "end_position": "abierta",
        },
    ]
    path = tmp_path / "sequences.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    library = SequenceLibrary.from_path(path, rng=random.Random(0))

    assert library.choose_initial().step == "Dile que no"


def test_sequence_library_validates_required_fields(tmp_path) -> None:
    payload = [{"step": "Broken"}]
    path = tmp_path / "sequences.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="missing keys"):
        SequenceLibrary.from_path(path)
