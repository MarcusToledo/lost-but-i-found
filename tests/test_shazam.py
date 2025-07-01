import asyncio
from pathlib import Path
import sys

import pytest

# Ensure arguments from pytest don't confuse argparse in shazam
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import shazam


def test_limpar_pasta_removes_directory(tmp_path):
    temp_dir = tmp_path / "tempdir"
    temp_dir.mkdir()
    (temp_dir / "dummy.txt").write_text("data")
    assert temp_dir.exists()
    shazam.limpar_pasta(str(temp_dir))
    assert not temp_dir.exists()


def test_processar_videos_records_tracks(monkeypatch, tmp_path):
    videos_dir = tmp_path / "videos"
    videos_dir.mkdir()
    video_file = videos_dir / "sample.mp4"
    video_file.write_text("video")
    output_file = tmp_path / "result.txt"

    def fake_extrair(video_path, audio_path):
        Path(audio_path).write_bytes(b"audio")

    async def fake_reconhecer(audio_path):
        return "Song - Artist"

    monkeypatch.setattr(shazam, "extrair_audio", fake_extrair)
    monkeypatch.setattr(shazam, "reconhecer_musica", fake_reconhecer)
    monkeypatch.setattr(shazam.messagebox, "showerror", lambda *a, **k: None)

    asyncio.run(shazam.processar_videos(str(videos_dir), str(output_file)))

    assert output_file.read_text().strip() == f"{video_file.name}: Song - Artist"
    assert not (videos_dir / "audios_temp").exists()
