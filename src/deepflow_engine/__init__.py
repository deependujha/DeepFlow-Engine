# credits: https://github.com/deependujha

from deepflow_engine.core.engine import DeepFlowEngine
from deepflow_engine.core.game import DeepFlowGame
from deepflow_engine.core.event import Event
from deepflow_engine.core.pipeline import run_pipeline
from deepflow_engine.publisher import BasePublisher, TelegramPublisher


def main() -> None:
    print("Hello from DeepFlow-Engine!")


__all__ = [
    "DeepFlowEngine",
    "DeepFlowGame",
    "Event",
    "BasePublisher",
    "TelegramPublisher",
    "run_pipeline",
]
