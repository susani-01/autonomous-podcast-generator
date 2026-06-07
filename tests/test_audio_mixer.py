import pytest
import numpy as np
import soundfile as sf
import os
import tempfile
from pydub import AudioSegment
from podcast_app.audio_mixer import (
    stitch_dialogue,
    overlay_background,
    export_podcast
)


def create_test_wav(path: str, duration_ms: int = 1000):
    sample_rate = 24000
    samples = np.zeros(int(sample_rate * duration_ms / 1000), dtype=np.float32)
    sf.write(path, samples, sample_rate)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def sample_audio_paths(temp_dir):
    paths = []
    for i in range(4):
        path = os.path.join(temp_dir, f"line_{i}.wav")
        create_test_wav(path, duration_ms=500)
        paths.append(path)
    return paths


@pytest.fixture
def sample_script():
    return [
        {"speaker": "HOST1", "text": "Hello everyone."},
        {"speaker": "HOST2", "text": "Hi there Alex."},
        {"speaker": "HOST1", "text": "Great to have you."},
        {"speaker": "HOST2", "text": "Happy to be here."},
    ]


def test_stitch_dialogue_returns_audio(sample_audio_paths, sample_script):
    result = stitch_dialogue(sample_audio_paths, sample_script)
    assert isinstance(result, AudioSegment)


def test_stitch_dialogue_longer_than_individual(sample_audio_paths, sample_script):
    result = stitch_dialogue(sample_audio_paths, sample_script)
    single = AudioSegment.from_wav(sample_audio_paths[0])
    assert len(result) > len(single)


def test_stitch_dialogue_adds_pauses(sample_audio_paths, sample_script):
    result = stitch_dialogue(sample_audio_paths, sample_script)
    assert len(result) > 2000


def test_overlay_no_music_returns_dialogue(sample_audio_paths, sample_script):
    dialogue = stitch_dialogue(sample_audio_paths, sample_script)
    result = overlay_background(dialogue, music_path=None)
    assert len(result) == len(dialogue)


def test_overlay_missing_file_returns_dialogue(sample_audio_paths, sample_script):
    dialogue = stitch_dialogue(sample_audio_paths, sample_script)
    result = overlay_background(dialogue, music_path="nonexistent.mp3")
    assert len(result) == len(dialogue)


def test_export_podcast_creates_file(sample_audio_paths, sample_script):
    dialogue = stitch_dialogue(sample_audio_paths, sample_script)

    os.makedirs("podcast_app/outputs/test_export",exist_ok=True)
    path = export_podcast(dialogue, job_id="test_export")
    assert os.path.exists(path)
    assert path.endswith(".mp3")


def test_export_podcast_nonzero_size(sample_audio_paths, sample_script):
    dialogue = stitch_dialogue(sample_audio_paths, sample_script)

    os.makedirs("podcast_app/outputs/test_size", exist_ok=True)
    path = export_podcast(dialogue, job_id="test_size")

    assert os.path.exists(path)
    assert os.path.getsize(path) > 0
