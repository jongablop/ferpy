from typing import List, Optional
from dataclasses import dataclass
import uuid

from ..auxiliary.correlations import Correlations

from .measurement import Measurement
from .quantity_values import QuantityValues

@dataclass
class Source:
    """
    Represents the source of a measurement or experimental result.
    """
    id: str = None
    name: str = None
    description: Optional[str] = None
    model: Optional[str] = None
    influence_quantities: Optional[List[QuantityValues]] = None
    input_quantities: Optional[List[Measurement]] = None
    correlations: Optional[Correlations] = None

    def __post_init__(self):
        """Generates a UUID for the id field if it's not provided."""
        if self.id is None:
            self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "influence_quantities": [
                iq.to_dict() for iq in self.influence_quantities
            ] if self.influence_quantities else None,
            "input_quantities": [iq.to_dict() for iq in self.input_quantities],
            "correlations": self.correlations.to_dict() if self.correlations else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Source instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            model=data.get("model"),
            influence_quantities=[QuantityValues.from_dict(iq) for iq in data.get("influence_quantities", [])],
            input_quantities=[Measurement.from_dict(iq) for iq in data["input_quantities"]],
            correlations=Correlations.from_dict(data["correlations"]) if data.get("correlations") else None
        )