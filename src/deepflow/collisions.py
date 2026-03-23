"""
[
  {
    "frame": 143,
    "time": 2.3833333333333333,
    "type": "crash"
  }
]

"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    frame: int
    time: float
    type: str
