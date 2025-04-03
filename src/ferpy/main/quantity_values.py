from typing import List, Optional
from dataclasses import dataclass
import uuid
import json

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

    def __eq__(self, other): 
        if not isinstance(other, QuantityValues):
            # don't attempt to compare against unrelated types
            return NotImplemented

       # Get all attributes as dictionaries, excluding 'id'
        self_dict = {key: value for key, value in vars(self).items() if key != 'id'}
        other_dict = {key: value for key, value in vars(other).items() if key != 'id'}

        # Compare the dictionaries
        return self_dict == other_dict

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
    
    @classmethod
    def from_json(cls, json_str: str):
        """Creates a QuantityValues instance from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def load_from_file(cls, filepath: str):
        """Loads a QuantityValues instance from a JSON file."""
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        return cls.from_dict(data)


    def set_values(self, quantity_name, values):

        index = self.quantities.index(quantity_name)
    
        # Ensure self.values is extended to the required length
        if len(self.values) <= index:
            self.values.extend([[]] * (index + 1 - len(self.values)))
        
        # Set the values at the desired index
        self.values[index] = values



    def set_su(self, quantity_name, su):

        index = self.quantities.index(quantity_name)
    
        # Ensure self.values is extended to the required length
        if len(self.standard_uncertainties) <= index:
            self.standard_uncertainties.extend(
                [[]] * (index + 1 - len(self.standard_uncertainties))
            )
        
        # Set the values at the desired index
        self.standard_uncertainties[index] = su

    def __str__(self):
        """
        Returns a formatted string representation of the QuantityValues object.
        If there is a single value (or a list with a single value), it returns:
            symbol = (value ± standard_uncertainty) unit
        """
        if not self.symbols or not self.values or not self.units:
            return "QuantityValues: Missing required data"

        # Extract first symbol, value, uncertainty, and unit
        symbol = self.symbols[0] if self.symbols else "?"
        unit = self.units[0] if self.units else "?"

        if len(self.values) == 1 and len(self.values[0]) == 1:
            value = self.values[0][0]
            uncertainty = self.standard_uncertainties[0][0] if self.standard_uncertainties else 0
            return rf"{symbol} = ({value} \pm {uncertainty}) \, {unit}"

        return f"QuantityValues: {self.name or 'Unnamed'}"
