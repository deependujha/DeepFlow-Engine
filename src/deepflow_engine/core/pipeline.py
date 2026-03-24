# credits: https://github.com/deependujha

from pathlib import Path

from deepflow_engine.core.engine import DeepFlowEngine
from deepflow_engine.core.renderer import video_renderer
from deepflow_engine.publisher.telegram import TelegramPublisher
from deepflow_engine.publisher.base import VideoMetadata


def run_pipeline(
    engine: DeepFlowEngine,
    *,
    output_video: str | Path = "deepflow_output.mp4",
    audio_map: dict[str, str | Path] | None = None,
    publish: bool = False,
) -> Path | None:
    """Run game and optionally generate video.

    - Runs the engine
    - If headless → renders video from frames + audio
    - Prints and returns output path

    Args:
        engine: Configured DeepFlowEngine instance
        output_video: Output video path
        audio_map: Optional override audio mapping

    Returns:
        Path to generated video (headless) or None (interactive)
    """
    if publish:
        # when running pipeline with publish=True, first ensure, that the TelegramPublisher is properly configured
        # with necessary credentials (e.g., bot token, chat ID) to avoid runtime errors during publishing.
        publisher = TelegramPublisher()

    engine.run()

    # Interactive → nothing to render
    if engine.interactive and engine.frames_dir is None:
        return None

    # Headless → generate video
    collisions_log = engine.collision_log
    audio_map = audio_map or engine.game.get_audio_map()
    print(f"{audio_map=}")

    if not collisions_log:
        print("DeepFlow: No audio events logged. Generating silent video.")

    output_path = Path(output_video)

    assert engine.frames_dir is not None, (
        "Frames directory must be set in headless mode."
    )

    video_renderer(
        output_filename=output_path,
        frames_dir=engine.frames_dir,
        collisions_log_list=collisions_log,
        audio_map=audio_map or {},
        FPS=engine.fps,
    )

    print(f"DeepFlow: Video generated at → {output_path.resolve()}")

    if publish:
        publisher.publish(
            output_path.resolve(),
            VideoMetadata("sample video", ["tag1", "tag2"]),
        )
    return output_path.resolve()
