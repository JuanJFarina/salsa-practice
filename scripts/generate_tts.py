"""Generate cached `.wav` clips for SalsaBeat Coach."""

from __future__ import annotations

import argparse
from pathlib import Path

from salsabeat.audio import required_clip_names
from salsabeat.sequences import SequenceLibrary
from salsabeat.tts_cache import sync_tts_cache

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
    report = sync_tts_cache(DEFAULT_AUDIO_DIR, clip_names, force=args.force)
    for clip_name in report.generated_clips:
        print(f"Generated clip: {clip_name}")
    for file_name in report.deleted_files:
        print(f"Deleted stale clip: {file_name}")
    print(f"Synced cached clips in {DEFAULT_AUDIO_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
