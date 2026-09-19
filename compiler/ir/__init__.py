from compiler.ast.nodes import CheckType, InvestigationNode
from compiler.ir.instructions import (
    IRInstruction,
    IROpcode,
    IRProgram,
)


CHECK_TO_OPCODE = {
    CheckType.PROCESSES: IROpcode.SCAN_PROCESSES,
    CheckType.NETWORK: IROpcode.SCAN_NETWORK,
    CheckType.DNS: IROpcode.SCAN_DNS,
    CheckType.LOGS: IROpcode.SCAN_LOGS,
}


def build_ir(ast: InvestigationNode) -> IRProgram:
    instructions = tuple(
        IRInstruction(
            CHECK_TO_OPCODE[check.check_type]
        )
        for check in ast.checks
    )

    return IRProgram(
        host=ast.host,
        instructions=instructions,
    )


__all__ = [
    "IRInstruction",
    "IROpcode",
    "IRProgram",
    "build_ir",
]