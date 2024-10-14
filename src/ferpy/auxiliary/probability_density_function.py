from typing import List
from dataclasses import dataclass, asdict

@dataclass
class ProbabilityDensityFunction:
    """
    Represents a probability density function.
    """
    name: str
    parameters: List[str]
    values: List[float]

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a ProbabilityDensityFunction instance from a dictionary."""
        return cls(
            name=data["name"],
            parameters=data["parameters"],
            values=data["values"]
        )