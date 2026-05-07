from dataclasses import dataclass
from typing import Literal

from .positions import Positions


@dataclass
class Step:
    name: str
    start_position: list[Positions]
    end_position: list[Positions]
    eight_counts: Literal[1, 2, 3, 4] = 1
