from typing import List, Optional
from dataclasses import dataclass
import uuid
import json

from ..auxiliary.changelog_entry import ChangelogEntry
from ..auxiliary.correlations import Correlations
from ..auxiliary.state import State

from .quantity_values import QuantityValues

@dataclass
class Measurement:
    """
    Represents a measurement in the experiment.
    """
    id: str = None
    description: Optional[str] = None
    changelog: Optional[List[ChangelogEntry]] = None
    correct: Optional[bool] = None
    state: Optional[List[State]] = None
    results: List[QuantityValues] = None
    correlations: Optional[Correlations] = None
    measurands: Optional[List[str]] = None
    source: Optional["Source"] = None # Use forward reference for Source

    def __post_init__(self):
        """Generates a UUID for the id field if it's not provided."""
        if self.id is None:
            self.id = str(uuid.uuid4())

        # Delay the import of Source until the object is fully initialized
        if isinstance(self.source, dict):
            from .source import Source
            self.source = Source(**self.source)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "changelog": [entry.to_dict() for entry in self.changelog] if self.changelog else None,
            "correct": self.correct,
            "state": [st.to_dict() for st in self.state] if self.state else None,
            "results": [result.to_dict() for result in self.results],
            "correlations": self.correlations.to_dict() if self.correlations else None,
            "measurands": self.measurands,
            "source": self.source.to_dict(),
        }

    def to_json(self):
        """Converts the Measurement instance to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)

    def save_to_file(self, filepath: str):
        """Exports the Measurement instance to a JSON file."""
        with open(filepath, "w") as json_file:
            json_file.write(self.to_json())

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Measurement instance from a dictionary."""
        from .source import Source
        return cls(
            id=data.get("id"),
            description=data.get("description"),
            changelog=[ChangelogEntry.from_dict(entry) for entry in data.get("changelog", [])],
            correct=data.get("correct"),
            state=[State.from_dict(st) for st in data.get("state", [])],
            results=[QuantityValues.from_dict(result) for result in data["results"]],
            correlations=Correlations.from_dict(data["correlations"]) if data.get("correlations") else None,
            measurands=data.get("measurands"),
            source=Source.from_dict(data["source"])
        )

    @classmethod
    def from_json(cls, json_str: str):
        """Creates a Measurement instance from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def load_from_file(cls, filepath: str):
        """Loads a Measurement instance from a JSON file."""
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        return cls.from_dict(data)
