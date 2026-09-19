from dataclasses import dataclass
from enum import Enum


class CheckType(Enum):
    PROCESSES = "PROCESSES"
    NETWORK = "NETWORK"
    DNS = "DNS"
    LOGS = "LOGS"


@dataclass(frozen=True)
class CheckNode:
    check_type: CheckType


@dataclass(frozen=True)
class InvestigationNode:
    host: str
    checks: tuple[CheckNode, ...]