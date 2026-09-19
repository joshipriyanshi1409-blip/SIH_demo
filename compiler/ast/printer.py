from compiler.ast.nodes import InvestigationNode


def print_ast(node: InvestigationNode) -> str:
    lines = [
        "INVESTIGATE",
        f"└── {node.host}",
    ]

    for index, check in enumerate(node.checks):
        is_last = index == len(node.checks) - 1
        branch = "└──" if is_last else "├──"

        lines.append(
            f"    {branch} CHECK_{check.check_type.value}"
        )

    return "\n".join(lines)
