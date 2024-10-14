from typing import List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ChangelogEntry:
    """
    Represents an entry in the changelog.
    """
    timestamp: datetime
    description: str
    user: Optional[str] = None

    def to_dict(self):
        """Converts the ChangelogEntry instance to a dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "user": self.user,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a ChangelogEntry instance from a dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            description=data["description"],
            user=data.get("user")
        )