from dataclasses import dataclass, field
from typing import Literal

from .positions import Positions


@dataclass
class Step:
    name: str
    """Step name which will be generated through TTS"""

    start_position: list[Positions]
    """Specific starting positions, as narrow as possible, can never be a parent class"""

    end_position: list[Positions]
    """Ending positions, as broad as possible, ideally using parent classes"""

    eight_counts: Literal[1, 2, 3, 4] = 1
    """A value of '1' corresponds to a full '1-2-3, 5-6-7' count"""
