# credits: https://github.com/deependujha

from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    # Example:
    #   {
    #     "frame": 143,
    #     "time": 2.3833333333333333,
    #     "type": "crash"
    #   }

    frame: int
    time: float
    type: str
