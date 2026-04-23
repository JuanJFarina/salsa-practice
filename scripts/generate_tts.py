"""Generate cached `.wav` clips for SalsaBeat Coach."""

from __future__ import annotations

import argparse
from pathlib import Path

import pyttsx3

from salsabeat.audio import clip_path_for_name, required_clip_names
from salsabeat.sequences import SequenceLibrary

ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_SEQUENCES_PATH = ROOT_DIR / "sequences.json"
DEFAULT_AUDIO_DIR = ROOT_DIR / "assets" / "audio" / "tts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate clips even if they already exist.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    library = SequenceLibrary.from_path(DEFAULT_SEQUENCES_PATH)
    clip_names = required_clip_names(library.sequences)

    DEFAULT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    engine = pyttsx3.init()
    engine.setProperty("rate", 210)

    for clip_name in clip_names:
        target_path = clip_path_for_name(DEFAULT_AUDIO_DIR, clip_name)
        if target_path.exists() and not args.force:
            print(f"Skipping existing clip: {target_path.name}")
            continue
        print(f"Generating clip: {target_path.name}")
        engine.save_to_file(clip_name, str(target_path))

    engine.runAndWait()
    engine.stop()
    print(f"Generated cached clips in {DEFAULT_AUDIO_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
