# credits: https://github.com/deependujha


class BaseError(Exception):
    """Base class for all DeepFlow exceptions."""

    pass


class PublisherError(BaseError):
    """Base class for all publisher-related exceptions."""

    def __init__(self, message: str) -> None:
        _base_msg = "An error occurred in the publisher: "
        super().__init__(_base_msg + message)


__all__ = ["BaseError", "PublisherError"]
