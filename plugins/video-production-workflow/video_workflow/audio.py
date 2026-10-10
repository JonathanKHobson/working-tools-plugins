from __future__ import annotations

import json
import math
import tempfile
import wave
from pathlib import Path
from typing import Any

import numpy as np

from .utils import require_tool, run


def _extract_wav(source: Path, destination: Path, sample_rate: int = 22050) -> None:
    require_tool("ffmpeg")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(source), "-vn", "-ac", "1", "-ar", str(sample_rate), "-c:a", "pcm_s16le", str(destination)
    ])


def _read_pcm(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        width = handle.getsampwidth()
        channels = handle.getnchannels()
        frames = handle.readframes(handle.getnframes())
    if width != 2:
        raise ValueError("Fallback audio reader expects 16-bit PCM")
    samples = np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    return samples, rate


def _fallback_beats(samples: np.ndarray, rate: int) -> tuple[float, list[float], list[dict[str, float]]]:
    hop = max(1, int(rate * 0.02))
    frame = max(hop, int(rate * 0.08))
    envelope = []
    times = []
    for start in range(0, max(1, len(samples) - frame), hop):
        chunk = samples[start : start + frame]
        envelope.append(float(np.sqrt(np.mean(chunk * chunk) + 1e-12)))
        times.append(start / rate)
    env = np.asarray(envelope)
    if len(env) < 4 or np.allclose(env, 0):
        return 0.0, [], []
    novelty = np.maximum(0.0, np.diff(env, prepend=env[0]))
    threshold = float(np.median(novelty) + 1.5 * np.std(novelty))
    peaks: list[int] = []
    min_gap = max(1, int(0.22 / (hop / rate)))
    for index in range(1, len(novelty) - 1):
        if novelty[index] > threshold and novelty[index] >= novelty[index - 1] and novelty[index] >= novelty[index + 1]:
            if not peaks or index - peaks[-1] >= min_gap:
                peaks.append(index)
    beat_times = [times[index] for index in peaks]
    if len(beat_times) >= 3:
        intervals = np.diff(beat_times)
        median = float(np.median(intervals[(intervals >= 0.25) & (intervals <= 2.0)])) if np.any((intervals >= 0.25) & (intervals <= 2.0)) else 0.0
        tempo = 60.0 / median if median else 0.0
        while 0 < tempo < 70:
            tempo *= 2
        while tempo > 180:
            tempo /= 2
    else:
        tempo = 0.0
    energy = [{"time_s": round(times[i], 4), "rms": round(float(env[i]), 6)} for i in range(len(env))]
    return tempo, beat_times, energy


def analyze_music(path: str | Path, *, use_librosa: bool = True) -> dict[str, Any]:
    source = Path(path)
    with tempfile.TemporaryDirectory(prefix="video-workflow-audio-") as temp:
        wav_path = Path(temp) / "analysis.wav"
        _extract_wav(source, wav_path)
        samples, rate = _read_pcm(wav_path)
        duration = len(samples) / rate
        if use_librosa:
            try:
                import librosa

                y, sr = librosa.load(str(wav_path), sr=None, mono=True)
                onset = librosa.onset.onset_strength(y=y, sr=sr)
                tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset, sr=sr, units="frames")
                beat_times = librosa.frames_to_time(beat_frames, sr=sr).astype(float).tolist()
                rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
                energy_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
                tempo_value = float(np.asarray(tempo).reshape(-1)[0]) if np.asarray(tempo).size else 0.0
                energy = [{"time_s": round(float(t), 4), "rms": round(float(v), 6)} for t, v in zip(energy_times, rms)]
                method = "librosa"
            except Exception:
                tempo_value, beat_times, energy = _fallback_beats(samples, rate)
                method = "energy-fallback"
        else:
            tempo_value, beat_times, energy = _fallback_beats(samples, rate)
            method = "energy-fallback"
    # Coarse sections based on energy quartiles; editorial hints, not musicological truth.
    section_count = max(1, min(8, math.ceil(duration / 15.0)))
    section_duration = duration / section_count if section_count else duration
    sections = []
    for index in range(section_count):
        start, end = index * section_duration, min(duration, (index + 1) * section_duration)
        values = [point["rms"] for point in energy if start <= point["time_s"] < end]
        sections.append({"start_s": round(start, 3), "end_s": round(end, 3), "mean_energy": round(float(np.mean(values)) if values else 0.0, 6)})
    return {
        "path": str(source.resolve()),
        "duration_s": round(duration, 4),
        "sample_rate": rate,
        "tempo_bpm": round(tempo_value, 3),
        "beats_s": [round(float(value), 4) for value in beat_times],
        "energy": energy,
        "sections": sections,
        "method": method,
        "interpretation_warning": "Beat and section estimates are editorial cues; confirm against listening and waveform review.",
    }


def save_music_analysis(result: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
