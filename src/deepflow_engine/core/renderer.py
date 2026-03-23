# credits: https://github.com/deependujha

import json
import re
import subprocess
import tempfile
from pathlib import Path

from deepflow_engine.errors import RendererError
from deepflow_engine.core.event import Event
from deepflow_engine.constants import DEFAULT_FPS


# ----------------------------
# Frame Sorting
# ----------------------------
def get_sorted_base_frames(frames_dir: Path) -> list[Path]:
    pattern = re.compile(r"^frame_(\d+)(?:_pause_(\d+))?\.png$")
    frames = []

    for f in frames_dir.iterdir():
        m = pattern.match(f.name)
        if m:
            frame_num = int(m.group(1))
            pause_num = int(m.group(2)) if m.group(2) is not None else -1
            frames.append((frame_num, pause_num, f))

    frames.sort(key=lambda x: (x[0], x[1]))
    return [f for _, _, f in frames]


# ----------------------------
# Load Events
# ----------------------------
def load_collisions(log_path: Path) -> set[Event]:
    if not log_path.exists():
        raise RendererError(f"{log_path} not found.")

    with open(log_path) as fh:
        data = json.load(fh)

    return {Event(**entry) for entry in data}


# ----------------------------
# Validation
# ----------------------------
def validate_audio_map(audio_map: dict[str, Path]) -> None:
    for event_type, path in audio_map.items():
        if not path.exists():
            raise RendererError(
                f"Audio file for event '{event_type}' not found: {path}"
            )


def validate_event_audio_mapping(
    events: set[Event], audio_map: dict[str, Path]
) -> None:
    missing = {event.name for event in events if event.name not in audio_map.keys()}
    print(f"{missing=}, {audio_map=}, {events=}")

    if missing:
        raise RendererError(
            f"Missing audio mapping for event types: {sorted(missing)}.\n"
            f"Provided mappings: {list(audio_map.keys())}"
        )


# ----------------------------
# Build Frame Sequence
# ----------------------------
def build_frame_sequence(
    base_frames: list[Path],
    collision_frames: set[int],
    pause_extra: int = 10,
) -> list[Path]:
    sequence = []
    frame_pattern = re.compile(r"^frame_(\d+)")

    for frame_path in base_frames:
        m = frame_pattern.match(frame_path.name)
        if not m:
            raise RendererError(f"Invalid frame filename: {frame_path.name}")

        frame_num = int(m.group(1))
        sequence.append(frame_path)

        if frame_num in collision_frames:
            sequence.extend([frame_path] * pause_extra)

    return sequence


# ----------------------------
# Write FFmpeg Concat List
# ----------------------------
def write_concat_list(sequence: list[Path], list_path: Path, FPS: int) -> None:
    duration = 1.0 / FPS

    with open(list_path, "w") as fh:
        for frame_path in sequence:
            fh.write(f"file '{frame_path.resolve()}'\n")
            fh.write(f"duration {duration:.10f}\n")

        fh.write(f"file '{sequence[-1].resolve()}'\n")


# ----------------------------
# FFmpeg Command Builder (Event-driven audio)
# ----------------------------
def build_ffmpeg_cmd(
    concat_list: Path,
    events: set[Event],
    audio_map: dict[str, Path],
    video_duration: float,
    output: Path,
) -> list[str]:
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

    # --- add audio inputs ---
    audio_inputs = []
    for event in events:
        audio_path = audio_map[event.name]
        audio_inputs.append((event, audio_path))

    for _, path in audio_inputs:
        cmd += ["-i", str(path.resolve())]

    # --- video encoding ---
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

    # --- audio ---
    if audio_inputs:
        filter_parts = []
        mix_inputs = []

        for i, (event, _) in enumerate(audio_inputs):
            delay_ms = int(event.time * 1000)
            input_idx = i + 1

            filter_parts.append(f"[{input_idx}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
            mix_inputs.append(f"[a{i}]")

        filter_complex = (
            ";".join(filter_parts) + f";{''.join(mix_inputs)}"
            f"amix=inputs={len(mix_inputs)}:duration=longest:normalize=1,"
            f"apad,atrim=duration={video_duration:.6f}[a]"
        )

        cmd += [
            "-filter_complex",
            filter_complex,
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "44100",
        ]

    cmd.append(str(output))
    return cmd


# ----------------------------
# Main Renderer
# ----------------------------
def video_renderer(
    output_filename: str | Path,
    frames_dir: str | Path,
    audio_map: dict[str, str | Path],
    collisions_log: str | Path | None = None,
    collisions_log_list: list[Event] | None = None,
    FPS: int = DEFAULT_FPS,
) -> Path:
    """Generate video from frames + event timeline + audio mapping."""
    if collisions_log is not None and collisions_log_list is not None:
        raise RendererError("Provide only one of collisions_log or collisions_log_list")
    if collisions_log is None and collisions_log_list is None:
        raise RendererError("Must provide one of collisions_log or collisions_log_list")

    if collisions_log is not None:
        collisions_log = Path(collisions_log)
        collisions_log_list = load_collisions(collisions_log)

    frames_dir = Path(frames_dir)
    output_video = Path(output_filename)
    audio_map = {k: Path(v) for k, v in audio_map.items()}

    if not frames_dir.exists():
        raise RendererError(f"frames directory '{frames_dir}' not found.")

    base_frames = get_sorted_base_frames(frames_dir)
    if not base_frames:
        raise RendererError("no frames found.")

    # --- validation ---
    validate_audio_map(audio_map)
    validate_event_audio_mapping(collisions_log_list, audio_map)

    collision_frame_nums = {event.frame for event in collisions_log_list}

    # --- build timeline ---
    sequence = build_frame_sequence(base_frames, collision_frame_nums)

    if not sequence:
        raise RendererError("empty frame sequence.")

    video_duration = len(sequence) / FPS

    # --- concat file ---
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, prefix="ffmpeg_concat_"
    ) as tmp:
        concat_list = Path(tmp.name)

    try:
        write_concat_list(sequence, concat_list, FPS)

        cmd = build_ffmpeg_cmd(
            concat_list,
            collisions_log_list,
            audio_map,
            video_duration,
            output_video,
        )

        result = subprocess.run(cmd, check=False)

        if result.returncode != 0:
            raise RendererError(f"ffmpeg failed with code {result.returncode}")

        return output_video.resolve()

    finally:
        concat_list.unlink(missing_ok=True)
