from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Finding:
    """A forensic finding produced from evidence."""

    host: str
    category: str
    severity: str
    title: str
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)