# credits: https://github.com/deependujha

from abc import ABC, abstractmethod
from dataclasses import dataclass
from deepflow_engine.errors import PublisherError


@dataclass
class VideoMetadata:
    description: str
    tags: list[str]


class BasePublisher(ABC):
    def __init__(self) -> None:
        pass

    def parse_metadata(self, metadata: VideoMetadata) -> str:
        components = [f"Description: {metadata.description}"]
        if metadata.tags:
            components.append(f"Tags: {', '.join(metadata.tags)}")
        return "\n".join(components)

    @abstractmethod
    def _publish(self, filename: str, msg: str) -> None:
        pass

    def publish(self, filename: str, metadata: VideoMetadata) -> None:
        try:
            parsed_metadata = self.parse_metadata(metadata)
            self._publish(filename, parsed_metadata)
        except Exception as e:
            raise PublisherError(str(e)) from e
