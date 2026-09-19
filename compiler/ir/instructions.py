from dataclasses import dataclass
from enum import Enum


class IROpcode(Enum):
    SCAN_PROCESSES = "SCAN_PROCESSES"
    SCAN_NETWORK = "SCAN_NETWORK"
    SCAN_DNS = "SCAN_DNS"
    SCAN_LOGS = "SCAN_LOGS"


@dataclass(frozen=True)
class IRInstruction:
    opcode: IROpcode


@dataclass(frozen=True)
class IRProgram:
    host: str
    instructions: tuple[IRInstruction, ...]