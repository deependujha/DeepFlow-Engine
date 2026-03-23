# credits: https://github.com/deependujha

import os
from pathlib import Path
import json
import pygame
from dataclasses import asdict

from deepflow_engine.errors import DeepFlowEngineError, DeepFlowGameError
from deepflow_engine.core.game import DeepFlowGame
from deepflow_engine.core.event import Event
from deepflow_engine.constants import (
    DEFAULT_FPS,
    DEFAULT_GAME_HEIGHT,
    DEFAULT_GAME_WIDTH,
)


class DeepFlowEngine:
    """Core engine that runs a DeepFlow game.

    Responsibilities:
    - Initialize pygame
    - Manage game loop
    - Provide rendering surface (canvas)
    - Handle audio (play or log)
    - Save frames in headless mode
    """

    def __init__(
        self,
        game: DeepFlowGame,
        *,
        frames_dir: str | Path | None = None,
        height: int = DEFAULT_GAME_HEIGHT,
        width: int = DEFAULT_GAME_WIDTH,
        fps: int = DEFAULT_FPS,
        video_length_seconds: int | None = None,
        total_frames: int | None = None,
        interactive: bool = False,
        game_caption: str = "DeepFlow Engine",
        collision_filename: str = "collisions_log.json",
    ):
        self.game = game
        self.game._engine = self

        self.height = height
        self.width = width
        self.fps = fps
        self.game_caption = game_caption

        self.video_length_seconds = video_length_seconds
        self.total_frames = total_frames
        self.interactive = interactive

        self.frames_dir = Path(frames_dir) if frames_dir is not None else None

        self.collision_log: list[dict] = []
        self.collision_filename = collision_filename
        self.curr_frame: int | None = None

        self._canvas: pygame.Surface | None = None
        self._clock: pygame.time.Clock | None = None
        self._error_occurred = False

        self._post_init()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _post_init(self) -> None:
        if not self.interactive:
            self._use_headless_mode()

            if self.frames_dir is None:
                raise DeepFlowEngineError(
                    "frames_dir must be specified in headless mode"
                )

            if self.total_frames is None and self.video_length_seconds is None:
                raise DeepFlowEngineError(
                    "Specify either total_frames or video_length_seconds"
                )

            if self.total_frames is not None and self.video_length_seconds is not None:
                raise DeepFlowEngineError(
                    "Specify only one of total_frames or video_length_seconds"
                )

            if self.video_length_seconds is not None:
                self.total_frames = int(self.fps * self.video_length_seconds)

            if not self.frames_dir.exists():
                self.frames_dir.mkdir(parents=True, exist_ok=True)

        pygame.init()
        self._clock = pygame.time.Clock()

    def _use_headless_mode(self) -> None:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    # ------------------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        self.game.start()
        self.loop()
        self.exit()

    def loop(self) -> None:
        print("DeepFlow: Starting game loop...")
        assert self._clock is not None

        if self.interactive:
            while self.game.running:
                self._handle_system_events()
                self._tick()
                self._step()
        else:
            for frame in range(self.total_frames):
                print(f"{frame=}")
                self.curr_frame = frame
                self._tick()
                self._step()

    def _tick(self) -> None:
        """Update delta time."""
        dt = self._clock.tick(self.fps) / 1000.0
        self.game.dt = dt

    def _step(self) -> None:
        """Single frame execution."""
        self.game.update()
        self.game.render(self.canvas)

        if self.interactive:
            pygame.display.update()
        else:
            self.save_frame()

    def _handle_system_events(self) -> None:
        """Handle OS-level events (window close, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    @property
    def canvas(self) -> pygame.Surface:
        if self._canvas is None:
            if self.interactive:
                self._canvas = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption(self.game_caption)
            else:
                self._canvas = pygame.Surface((self.width, self.height))
        return self._canvas

    def save_frame(self) -> None:
        if self.frames_dir is None:
            raise DeepFlowEngineError("frames_dir must be set to save frames")

        if self.curr_frame is None:
            raise DeepFlowEngineError("curr_frame must be set before saving frame")

        file_name = self.frames_dir / f"frame_{self.curr_frame:04d}.png"
        pygame.image.save(self.canvas, file_name)

    def write_log(self):
        collisions = [asdict(entry) for entry in self.collision_log]
        json_data = json.dumps(collisions, indent=4)
        with open(self.collision_filename, "w") as f:
            f.write(json_data)

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------

    def _emit_event(self, event_name: str) -> None:
        if self.interactive:
            audio_map = self.game._get_cached_audio_map()

            if event_name not in audio_map:
                raise DeepFlowGameError(f"No audio mapping found for '{event_name}'")
            pygame.mixer.Sound(audio_map[event_name]).play()
        else:
            if self.curr_frame is None:
                raise DeepFlowEngineError("curr_frame must be set for event logging")

            self.collision_log.append(
                Event(
                    frame=self.curr_frame,
                    time=self.curr_frame / self.fps,
                    name=event_name,
                )
            )

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def exit(self) -> None:
        self.write_log()
        self.game.exit()
        pygame.quit()
