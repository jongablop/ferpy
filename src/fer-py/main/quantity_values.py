from typing import List, Optional
from dataclasses import dataclass
import uuid

from ..auxiliary.changelog_entry import ChangelogEntry
from ..auxiliary.coverage import Coverage
from ..auxiliary.probability_density_function import ProbabilityDensityFunction

@dataclass
class QuantityValues:
    """
    Represents the values, uncertainties, and associated data for a physical quantity.
    """
    id: str = None
    name: str = None
    description: Optional[str] = None
    changelog: Optional[List[ChangelogEntry]] = None
    quantities: List[str] = None
    symbols: Optional[List[str]] = None
    units: List[str] = None
    values: List[List[float]] = None
    standard_uncertainties: List[List[float]] = None
    coverages: Optional[List[Coverage]] = None
    probability_density_functions: Optional[List[ProbabilityDensityFunction]] = None
    correlation_indices: Optional[List[int]] = None

    def __post_init__(self):
        """Generates a UUID for the id field if it's not provided."""
        if self.id is None:
            self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "changelog": [entry.to_dict() for entry in self.changelog] if self.changelog else None,
            "quantities": self.quantities,
            "symbols": self.symbols,
            "units": self.units,
            "values": self.values,
            "standard_uncertainties": self.standard_uncertainties,
            "coverages": [cov.to_dict() for cov in self.coverages] if self.coverages else None,
            "probability_density_functions": [
                pdf.to_dict() for pdf in self.probability_density_functions
            ] if self.probability_density_functions else None,
            "correlation_indices": self.correlation_indices,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a QuantityValues instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            changelog=[ChangelogEntry.from_dict(entry) for entry in data.get("changelog", [])],
            quantities=data["quantities"],
            symbols=data.get("symbols"),
            units=data["units"],
            values=data["values"],
            standard_uncertainties=data["standard_uncertainties"],
            coverages=[Coverage.from_dict(cov) for cov in data.get("coverages", [])],
            probability_density_functions=[
                ProbabilityDensityFunction.from_dict(pdf) for pdf in data.get("probability_density_functions", [])
            ],
            correlation_indices=data.get("correlation_indices")
        )
