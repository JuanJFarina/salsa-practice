from pathlib import Path

from salsabeat.audio import clip_path_for_name, required_clip_names
from salsabeat.models import Sequence
from salsabeat.tts_cache import sync_tts_cache


class DummyEngine:
    def __init__(self) -> None:
        self.saved: list[tuple[str, Path]] = []
        self.rate: int | None = None
        self.stopped = False

    def setProperty(self, name: str, value: int) -> None:
        if name == "rate":
            self.rate = value

    def save_to_file(self, clip_name: str, path: str) -> None:
        self.saved.append((clip_name, Path(path)))

    def runAndWait(self) -> None:
        for clip_name, path in self.saved:
            path.write_text(f"generated:{clip_name}", encoding="utf-8")

    def stop(self) -> None:
        self.stopped = True


def test_required_clip_names_use_spanish_cues() -> None:
    sequences = [
        Sequence(
            step="Básico",
            eight_counts=1,
            start_position="cerrada",
            end_position="cerrada",
        )
    ]

    assert required_clip_names(sequences) == ["uno", "cinco", "Básico"]


def test_sync_tts_cache_generates_missing_and_deletes_stale(monkeypatch, tmp_path) -> None:
    existing_required = clip_path_for_name(tmp_path, "uno")
    existing_required.write_text("keep", encoding="utf-8")
    stale_file = tmp_path / "old.wav"
    stale_file.write_text("stale", encoding="utf-8")

    dummy_engine = DummyEngine()
    monkeypatch.setattr("salsabeat.tts_cache.pyttsx3.init", lambda: dummy_engine)

    report = sync_tts_cache(tmp_path, ["uno", "cinco", "Básico"])

    assert report.required_clips == ("uno", "cinco", "Básico")
    assert report.generated_clips == ("cinco", "Básico")
    assert report.deleted_files == ("old.wav",)
    assert existing_required.read_text(encoding="utf-8") == "keep"
    assert clip_path_for_name(tmp_path, "cinco").exists()
    assert clip_path_for_name(tmp_path, "Básico").exists()
    assert not stale_file.exists()
    assert dummy_engine.rate == 210
    assert dummy_engine.stopped is True
