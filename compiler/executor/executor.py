from typing import Protocol

from compiler.ir.instructions import IRInstruction


class PlatformAdapter(Protocol):
    def execute(self, instruction: IRInstruction) -> object:
        ...


class Executor:
    def __init__(self, adapter: PlatformAdapter):
        self.adapter = adapter

    def execute_instruction(self, instruction: IRInstruction) -> object:
        return self.adapter.execute(instruction)