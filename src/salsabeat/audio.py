"""Audio asset helpers and playback for cached SalsaBeat clips."""

from __future__ import annotations

import re
import winsound
from dataclasses import dataclass
from pathlib import Path

from .models import Sequence
from .timeline import LEAD_IN_CUES


class MissingAudioAssetError(FileNotFoundError):
    """Raised when a required cached clip is missing."""


@dataclass(frozen=True, slots=True)
class AudioPreflight:
    required_clips: tuple[str, ...]
    missing_clips: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.missing_clips


def slugify_clip_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.casefold()).strip("_")
    return slug or "clip"


def clip_path_for_name(assets_dir: Path, clip_name: str) -> Path:
    return assets_dir / f"{slugify_clip_name(clip_name)}.wav"


def required_clip_names(sequences: list[Sequence]) -> list[str]:
    ordered = dict.fromkeys([*LEAD_IN_CUES, *(sequence.step for sequence in sequences)])
    return list(ordered)


class AudioPlayer:
    """Validates and plays cached `.wav` clips through Windows ``winsound``."""

    def __init__(self, assets_dir: Path | str) -> None:
        self.assets_dir = Path(assets_dir)

    def preflight(self, clip_names: list[str]) -> AudioPreflight:
        missing = [
            clip_name
            for clip_name in clip_names
            if not clip_path_for_name(self.assets_dir, clip_name).exists()
        ]
        return AudioPreflight(required_clips=tuple(clip_names), missing_clips=tuple(missing))

    def preload(self, clip_names: list[str]) -> None:
        for clip_name in clip_names:
            self._path_for_clip(clip_name)

    def play(self, clip_name: str) -> Path:
        clip_path = self._path_for_clip(clip_name)
        winsound.PlaySound(
            str(clip_path),
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )
        return clip_path

    def stop_all(self) -> None:
        winsound.PlaySound(None, 0)

    def _path_for_clip(self, clip_name: str) -> Path:
        clip_path = clip_path_for_name(self.assets_dir, clip_name)
        if not clip_path.exists():
            raise MissingAudioAssetError(f"Missing audio clip: {clip_path}")
        return clip_path
