from typing import List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Coverage:
    """
    Represents coverage data for a measurement.
    """
    intervals: List[List[float]]
    probabilities: List[float]
    degrees_of_freedom: List[int]
    method: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Coverage instance from a dictionary."""
        return cls(
            intervals=data["intervals"],
            probabilities=data["probabilities"],
            degrees_of_freedom=data["degrees_of_freedom"],
            method=data.get("method")
        )