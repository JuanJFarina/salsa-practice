"""Utilities for keeping cached TTS audio in sync with the current sequences."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pyttsx3

from .audio import clip_path_for_name


@dataclass(frozen=True, slots=True)
class TtsCacheSyncReport:
    """Summary of a cache synchronization run."""

    required_clips: tuple[str, ...]
    generated_clips: tuple[str, ...]
    deleted_files: tuple[str, ...]


def sync_tts_cache(
    audio_dir: Path | str,
    clip_names: Iterable[str],
    *,
    force: bool = False,
    speech_rate: int = 210,
) -> TtsCacheSyncReport:
    """Create missing cached clips and remove stale ones."""

    target_dir = Path(audio_dir)
    ordered_clips = tuple(dict.fromkeys(clip_names))
    required_paths = {
        clip_name: clip_path_for_name(target_dir, clip_name) for clip_name in ordered_clips
    }
    required_filenames = {path.name for path in required_paths.values()}

    target_dir.mkdir(parents=True, exist_ok=True)

    deleted_files: list[str] = []
    for existing_file in target_dir.glob("*.wav"):
        if existing_file.name not in required_filenames:
            existing_file.unlink()
            deleted_files.append(existing_file.name)

    generated_clips = list(ordered_clips) if force else [
        clip_name for clip_name, clip_path in required_paths.items() if not clip_path.exists()
    ]

    if generated_clips:
        engine = pyttsx3.init()
        engine.setProperty("rate", speech_rate)
        try:
            for clip_name in generated_clips:
                engine.save_to_file(clip_name, str(required_paths[clip_name]))
            engine.runAndWait()
        finally:
            engine.stop()

    return TtsCacheSyncReport(
        required_clips=ordered_clips,
        generated_clips=tuple(generated_clips),
        deleted_files=tuple(sorted(deleted_files)),
    )
