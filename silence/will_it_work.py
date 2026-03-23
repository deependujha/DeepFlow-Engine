# credits: https://github.com/deependujha
from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip
import json
import os

# 1. Load and Sort Frames (Crucial for macOS file systems)
frame_dir = "frames"
files = [
    os.path.join(frame_dir, f) for f in os.listdir(frame_dir) if f.endswith(".png")
]
files.sort()  # Ensure frame_0001.png is first
clip = ImageSequenceClip(files, fps=60)

# 2. Load collisions
with open("collisions_log.json") as f:
    collisions = json.load(f)

# 3. Create Audio Instances
crash_source = AudioFileClip("crash_fixed.wav")
audio_instances = []

# If your crash.wav is 4s, it might be overlapping.
# Let's ensure they are added as independent layers.
for entry in collisions:
    start_time = entry["time"]
    # Create a clean copy with the specific start time
    audio_instances.append(crash_source.copy().with_start(start_time))

# 4. The Fix: Composite with a Background "Silence"
# Sometimes CompositeAudioClip fails if it doesn't have a base duration
final_audio = CompositeAudioClip(audio_instances)
final_audio.duration = clip.duration

# 5. Combine
final = clip.with_audio(final_audio)

# 6. Optimized Export for macOS/Shorts
final.write_videofile(
    "deepflow_reel.mp4",
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",  # Forces a separate audio render
    remove_temp=True,
    fps=60,
    logger=None,  # Cleans up terminal output
)

print("Check deepflow_reel.mp4 now. If it's still silent, check step 2 below.")
