from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    EOF = auto()

    IDENTIFIER = auto()

    INVESTIGATE = auto()
    CHECK = auto()
    PROCESSES = auto()
    NETWORK = auto()
    DNS = auto()
    LOGS = auto()

    LBRACE = auto()
    RBRACE = auto()

    UNKNOWN = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    line: int
    column: int