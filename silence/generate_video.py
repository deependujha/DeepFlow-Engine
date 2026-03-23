# credits: https://github.com/deependujha
import json
import subprocess


def create_deepflow_video(frame_pattern, json_log_path, audio_file, output_name):
    with open(json_log_path, "r") as f:
        collisions = json.load(f)

    # Base command
    cmd = ["ffmpeg", "-y", "-framerate", "60", "-i", frame_pattern]

    # Add the crash sound as an input for every collision
    for _ in collisions:
        cmd.extend(["-i", audio_file])

    filter_parts = []
    if collisions:
        for i, entry in enumerate(collisions):
            # Convert seconds to milliseconds
            delay_ms = int(entry["time"] * 1000)
            # [i+1:a] refers to the (i+1)-th input file
            # We delay both left and right channels: delay_ms|delay_ms
            filter_parts.append(f"[{i + 1}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

        # Mix all delayed streams
        mix_labels = "".join([f"[a{i}]" for i in range(len(collisions))])
        filter_complex = (
            ";".join(filter_parts)
            + f";{mix_labels}amix=inputs={len(collisions)}:dropout_transition=99999,aresample=async=1[outa]"
        )

        cmd.extend(["-filter_complex", filter_complex])
        cmd.extend(["-map", "0:v"])  # Map the video from frames
        cmd.extend(["-map", "[outa]"])  # Map the result of our audio filter
        cmd.extend(
            ["-ar", "44100"]
        )  # Set audio sample rate to 44.1kHz for better compatibility
    else:
        # If no collisions, just map the video (will be silent)
        cmd.extend(["-map", "0:v"])

    cmd.extend(
        [
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",  # Explicitly set audio codec to AAC
            "-shortest",
            output_name,
        ]
    )

    print("Running ffmpeg command:")
    print(" ".join(cmd))
    subprocess.run(cmd)


create_deepflow_video(
    "frames/frame_%04d.png",
    "collisions_log.json",
    "crash_fixed.wav",
    "deepflow_reel.mp4",
)
