from typing import List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Correlations:
    """
    Represents correlations between quantities.
    """
    quantities: Optional[List[str]] = None
    correlation_matrix: Optional[List[List[float]]] = None
    method: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Correlations instance from a dictionary."""
        return cls(
            quantities=data.get("quantities"),
            correlation_matrix=data.get("correlation_matrix"),
            method=data.get("method")
        )