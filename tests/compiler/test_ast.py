from compiler.ast import build_ast
from compiler.ast.nodes import (
    CheckNode,
    CheckType,
    InvestigationNode,
)
from compiler.ast.printer import print_ast
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def build_from_source(source: str) -> InvestigationNode:
    tokens = Lexer(source).tokenize()
    parsed = Parser(tokens).parse()
    return build_ast(parsed)


def test_build_single_check_ast():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
}"""

    ast = build_from_source(source)

    assert isinstance(ast, InvestigationNode)
    assert ast.host == "HOST01"
    assert ast.checks == (
        CheckNode(CheckType.DNS),
    )


def test_build_full_ast():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
}"""

    ast = build_from_source(source)

    assert ast.host == "HOST01"

    assert ast.checks == (
        CheckNode(CheckType.PROCESSES),
        CheckNode(CheckType.NETWORK),
        CheckNode(CheckType.DNS),
        CheckNode(CheckType.LOGS),
    )


def test_ast_preserves_check_order():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
    CHECK PROCESSES
}"""

    ast = build_from_source(source)

    assert ast.checks[0].check_type == CheckType.DNS
    assert ast.checks[1].check_type == CheckType.PROCESSES


def test_ast_printer():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
}"""

    ast = build_from_source(source)

    output = print_ast(ast)

    expected = """INVESTIGATE
└── HOST01
    ├── CHECK_PROCESSES
    ├── CHECK_NETWORK
    ├── CHECK_DNS
    └── CHECK_LOGS"""

    assert output == expected