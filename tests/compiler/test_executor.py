from compiler.executor import Executor
from compiler.ir.instructions import (
    IRInstruction,
    IROpcode,
)


class FakeAdapter:
    def __init__(self):
        self.executed = []

    def execute(self, instruction):
        self.executed.append(instruction)
        return {
            "status": "success",
            "opcode": instruction.opcode.value,
        }


def test_executor_sends_instruction_to_adapter():
    adapter = FakeAdapter()
    executor = Executor(adapter)

    instruction = IRInstruction(IROpcode.SCAN_PROCESSES)

    result = executor.execute_instruction(instruction)

    assert adapter.executed == [instruction]
    assert result == {
        "status": "success",
        "opcode": "SCAN_PROCESSES",
    }


def test_executor_supports_network_instruction():
    adapter = FakeAdapter()
    executor = Executor(adapter)

    instruction = IRInstruction(IROpcode.SCAN_NETWORK)

    result = executor.execute_instruction(instruction)

    assert adapter.executed == [instruction]
    assert result["opcode"] == "SCAN_NETWORK"


def test_executor_supports_dns_instruction():
    adapter = FakeAdapter()
    executor = Executor(adapter)

    instruction = IRInstruction(IROpcode.SCAN_DNS)

    result = executor.execute_instruction(instruction)

    assert adapter.executed == [instruction]
    assert result["opcode"] == "SCAN_DNS"


def test_executor_supports_log_instruction():
    adapter = FakeAdapter()
    executor = Executor(adapter)

    instruction = IRInstruction(IROpcode.SCAN_LOGS)

    result = executor.execute_instruction(instruction)

    assert adapter.executed == [instruction]
    assert result["opcode"] == "SCAN_LOGS"
    