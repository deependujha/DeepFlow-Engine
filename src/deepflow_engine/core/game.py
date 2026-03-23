# credits: https://github.com/deependujha

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

from deepflow_engine.errors import DeepFlowGameError

if TYPE_CHECKING:
    from deepflow_engine.core.engine import DeepFlowEngine


class DeepFlowGame(ABC):
    """Base class for all DeepFlow games.

    Users should subclass this and implement the required methods.
    The engine controls the main loop; the game defines behavior.

    Key responsibilities:
    - Define game state and logic (`update`)
    - Render onto the provided canvas (`render`)
    - Emit audio events via `play_audio`
    - Control lifecycle using `running`
    """

    def __init__(self) -> None:
        self._engine: "DeepFlowEngine | None" = None

        # Controls the game loop in interactive mode
        self.running: bool = False

        # Delta time (seconds) between frames (set by engine)
        self.dt: float = 0.0

        # Internal cache for audio mapping
        self._audio_map: dict[str, str] | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def start(self) -> None:
        """Initialize game state.

        Called once before the game loop starts.
        Typically used to:
        - initialize sprites
        - reset score/state
        - set `self.running = True` (for interactive mode)
        """
        pass

    @abstractmethod
    def kill_all_sprites(self) -> None:
        """Cleanup all game objects (sprites, resources, etc.)."""
        pass

    def exit(self) -> None:
        """Called when the engine stops the game."""
        self.kill_all_sprites()

    # ------------------------------------------------------------------
    # Game Loop Hooks
    # ------------------------------------------------------------------

    @abstractmethod
    def update(self) -> None:
        """Update game state.

        Called every frame.

        Responsibilities may include:
        - movement and physics
        - collision detection
        - AI / input handling
        - triggering audio via `play_audio`
        """
        pass

    @abstractmethod
    def render(self, canvas: pygame.Surface) -> None:
        """Render the current frame onto the provided canvas.

        Args:
            canvas: The surface to draw on (display or offscreen).
        """
        pass

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------

    @abstractmethod
    def get_audio_map(self) -> dict[str, str]:
        """Return mapping of event name → audio file path.

        Example:
            {"crash": "assets/crash.wav"}
        """
        pass

    def _get_cached_audio_map(self) -> dict[str, str]:
        """Internal helper to cache audio map."""
        if self._audio_map is None:
            self._audio_map = self.get_audio_map()
        return self._audio_map

    def play_audio(self, audio_name: str) -> None:
        """Emit an audio event.

        In interactive mode → plays sound immediately
        In headless mode → logs event for later video rendering

        Args:
            audio_name: Key from `get_audio_map()`
        """
        if self._engine is None:
            raise RuntimeError(
                "Game must be attached to an engine before playing audio"
            )

        audio_map = self._get_cached_audio_map()

        if audio_name not in audio_map:
            raise DeepFlowGameError(f"No audio mapping found for '{audio_name}'")

        self._engine._emit_event(audio_name)
