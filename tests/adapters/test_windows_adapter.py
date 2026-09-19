import platform

import pytest

from compiler.ir.instructions import (
    IRInstruction,
    IROpcode,
)
from adapters.windows.adapter import WindowsAdapter


@pytest.fixture
def adapter():
    if platform.system() != "Windows":
        pytest.skip("Windows adapter tests require Windows")

    return WindowsAdapter()


def test_windows_adapter_initializes(adapter):
    assert isinstance(adapter, WindowsAdapter)

def test_process_instruction(adapter):
    result = adapter.execute(
        IRInstruction(IROpcode.SCAN_PROCESSES)
    )

    assert result["operation"] == "SCAN_PROCESSES"
    assert result["platform"] == "Windows"
    assert result["status"] == "success"
    assert isinstance(result["data"], list)
    assert len(result["data"]) > 0

    
def test_network_instruction(adapter):
    result = adapter.execute(
        IRInstruction(IROpcode.SCAN_NETWORK)
    )

    assert result["operation"] == "SCAN_NETWORK"
    assert result["platform"] == "Windows"
    assert result["status"] == "not_implemented"


def test_dns_instruction(adapter):
    result = adapter.execute(
        IRInstruction(IROpcode.SCAN_DNS)
    )

    assert result["operation"] == "SCAN_DNS"
    assert result["platform"] == "Windows"
    assert result["status"] == "not_implemented"


def test_logs_instruction(adapter):
    result = adapter.execute(
        IRInstruction(IROpcode.SCAN_LOGS)
    )

    assert result["operation"] == "SCAN_LOGS"
    assert result["platform"] == "Windows"
    assert result["status"] == "not_implemented"
    