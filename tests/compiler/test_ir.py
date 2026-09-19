from compiler.ast import build_ast
from compiler.ir import build_ir
from compiler.ir.instructions import (
    IRInstruction,
    IROpcode,
    IRProgram,
)
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def build_ir_from_source(source: str) -> IRProgram:
    tokens = Lexer(source).tokenize()
    parsed = Parser(tokens).parse()
    ast = build_ast(parsed)
    return build_ir(ast)


def test_build_single_ir_instruction():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
}"""

    ir = build_ir_from_source(source)

    assert isinstance(ir, IRProgram)
    assert ir.host == "HOST01"
    assert ir.instructions == (
        IRInstruction(IROpcode.SCAN_DNS),
    )


def test_build_full_ir_program():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
    CHECK DNS
    CHECK LOGS
}"""

    ir = build_ir_from_source(source)

    assert ir.host == "HOST01"

    assert ir.instructions == (
        IRInstruction(IROpcode.SCAN_PROCESSES),
        IRInstruction(IROpcode.SCAN_NETWORK),
        IRInstruction(IROpcode.SCAN_DNS),
        IRInstruction(IROpcode.SCAN_LOGS),
    )


def test_ir_preserves_check_order():
    source = """INVESTIGATE HOST01 {
    CHECK DNS
    CHECK PROCESSES
}"""

    ir = build_ir_from_source(source)

    assert ir.instructions[0].opcode == IROpcode.SCAN_DNS
    assert ir.instructions[1].opcode == IROpcode.SCAN_PROCESSES


def test_ir_contains_no_platform_specific_commands():
    source = """INVESTIGATE HOST01 {
    CHECK PROCESSES
    CHECK NETWORK
}"""

    ir = build_ir_from_source(source)

    assert ir.instructions[0].opcode == IROpcode.SCAN_PROCESSES
    assert ir.instructions[1].opcode == IROpcode.SCAN_NETWORK

    for instruction in ir.instructions:
        assert isinstance(instruction.opcode, IROpcode)