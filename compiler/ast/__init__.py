from compiler.ast.nodes import (
    CheckNode,
    CheckType,
    InvestigationNode,
)


def build_ast(parsed_program: dict) -> InvestigationNode:
    checks = tuple(
        CheckNode(CheckType[check])
        for check in parsed_program["checks"]
    )

    return InvestigationNode(
        host=parsed_program["host"],
        checks=checks,
    )


__all__ = [
    "CheckNode",
    "CheckType",
    "InvestigationNode",
    "build_ast",
]