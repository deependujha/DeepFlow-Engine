# credits: https://github.com/deependujha
#!/usr/bin/env python3
"""
Generate a video from frames/ directory at 60 fps.
On collision frames (from collisions_log.json), pause for 10 extra frames.
Overlay game-over.mp3 starting at the first collision timestamp.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


FRAMES_DIR = Path("frames")
COLLISIONS_LOG = Path("collisions_log.json")
AUDIO_FILE = Path("game-over.mp3")
OUTPUT_VIDEO = Path("output.mp4")
FPS = 60


def get_sorted_base_frames(frames_dir: Path) -> list[Path]:
    pattern = re.compile(r"^frame_(\d+)\.png$")
    frames = []
    for f in frames_dir.iterdir():
        m = pattern.match(f.name)
        if m:
            frames.append((int(m.group(1)), f))
    frames.sort(key=lambda x: x[0])
    return [f for _, f in frames]


def load_collisions(log_path: Path) -> set[int]:
    if not log_path.exists():
        print(f"Warning: {log_path} not found, no pauses will be inserted.")
        return set()
    with open(log_path) as fh:
        data = json.load(fh)
    return {entry["frame"] for entry in data}


def build_frame_sequence(
    base_frames: list[Path], collision_frames: set[int], pause_extra: int = 10
) -> list[Path]:
    sequence = []
    for frame_path in base_frames:
        m = re.match(r"^frame_(\d+)\.png$", frame_path.name)
        frame_num = int(m.group(1))
        sequence.append(frame_path)
        if frame_num in collision_frames:
            sequence.extend([frame_path] * pause_extra)
    return sequence


def write_concat_list(sequence: list[Path], list_path: Path) -> None:
    duration = 1.0 / FPS
    with open(list_path, "w") as fh:
        for frame_path in sequence:
            abs_path = frame_path.resolve()
            fh.write(f"file '{abs_path}'\n")
            fh.write(f"duration {duration:.10f}\n")
        fh.write(f"file '{sequence[-1].resolve()}'\n")


def collision_start_seconds(collisions_log: Path) -> float | None:
    if not collisions_log.exists():
        return None
    with open(collisions_log) as fh:
        data = json.load(fh)
    if not data:
        return None
    return min(entry["time"] for entry in data)


def get_video_duration(sequence: list[Path]) -> float:
    return len(sequence) / FPS


def build_ffmpeg_cmd(
    concat_list: Path,
    audio_path: Path,
    audio_delay: float,
    video_duration: float,
    output: Path,
) -> list[str]:
    has_audio = audio_path.exists()

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
    ]

    if has_audio:
        cmd += ["-i", str(audio_path.resolve())]

    cmd += [
        "-fps_mode",
        "passthrough",
        "-pix_fmt",
        "yuv420p",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "slow",
    ]

    if has_audio:
        delay_ms = int(audio_delay * 1000)
        # adelay: pad silence before audio
        # apad:   pad silence after audio to match video duration exactly
        # atrim:  hard-cut at video duration so no overshoot
        cmd += [
            "-filter_complex",
            f"[1:a]adelay={delay_ms}|{delay_ms},apad,atrim=duration={video_duration:.6f}[a]",
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
        ]
    else:
        print("Warning: game-over.mp3 not found — generating video without audio.")

    cmd.append(str(output))
    return cmd


def main() -> None:
    if not FRAMES_DIR.exists():
        sys.exit(f"Error: frames directory '{FRAMES_DIR}' not found.")

    base_frames = get_sorted_base_frames(FRAMES_DIR)
    if not base_frames:
        sys.exit("Error: no base frames found in frames/ directory.")

    print(f"Found {len(base_frames)} base frames.")

    collision_frame_nums = load_collisions(COLLISIONS_LOG)
    print(f"Collision frames: {collision_frame_nums or 'none'}")

    sequence = build_frame_sequence(base_frames, collision_frame_nums, pause_extra=10)
    print(
        f"Total frame sequence length: {len(sequence)} frames  "
        f"({len(sequence) / FPS:.2f}s at {FPS} fps)"
    )

    audio_delay = collision_start_seconds(COLLISIONS_LOG) or 0.0
    print(f"Audio (game-over.mp3) will start at t={audio_delay:.4f}s")

    video_duration = get_video_duration(sequence)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, prefix="ffmpeg_concat_"
    ) as tmp:
        concat_list = Path(tmp.name)

    try:
        write_concat_list(sequence, concat_list)
        cmd = build_ffmpeg_cmd(
            concat_list, AUDIO_FILE, audio_delay, video_duration, output=OUTPUT_VIDEO
        )

        print("\nRunning ffmpeg …")
        print(" ".join(cmd))
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            sys.exit(f"ffmpeg exited with code {result.returncode}")
        print(f"\nDone → {OUTPUT_VIDEO.resolve()}")
    finally:
        concat_list.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
