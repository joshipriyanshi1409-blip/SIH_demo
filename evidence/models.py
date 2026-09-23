from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvidenceRecord:
    """A single piece of forensic evidence."""

    host: str
    source: str
    operation: str
    timestamp: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceBundle:
    """Collection of evidence produced during an investigation."""

    host: str
    platform: str
    records: tuple[EvidenceRecord, ...] = field(default_factory=tuple)
    