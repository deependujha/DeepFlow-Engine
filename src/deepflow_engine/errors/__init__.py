# credits: https://github.com/deependujha


class BaseError(Exception):
    """Base class for all DeepFlow exceptions."""

    prefix = "DeepFlow"

    def __init__(self, message: str) -> None:
        super().__init__(f"{self.prefix}: {message}")


class DeepFlowEngineError(BaseError):
    """Errors related to engine execution."""

    prefix = "DeepFlow Engine error"


class DeepFlowGameError(BaseError):
    """Errors caused by game logic or misuse of the game API."""

    prefix = "DeepFlow Game error"


class RendererError(BaseError):
    """Errors during frame rendering or video generation."""

    prefix = "DeepFlow Renderer error"


class PublisherError(BaseError):
    """Errors related to publishing (Telegram, Discord, etc.)."""

    prefix = "DeepFlow Publisher error"


__all__ = [
    "BaseError",
    "DeepFlowEngineError",
    "DeepFlowGameError",
    "RendererError",
    "PublisherError",
]
