import platform

from compiler.ir.instructions import IRInstruction, IROpcode

from adapters.windows.dns import collect_dns
from adapters.windows.logs import collect_logs
from adapters.windows.network import collect_network
from adapters.windows.processes import collect_processes


class WindowsAdapter:
    """Windows implementation of JOCKY forensic operations."""

    def __init__(self):
        if platform.system() != "Windows":
            raise RuntimeError(
                "WindowsAdapter can only run on Windows."
            )

    def execute(self, instruction: IRInstruction) -> dict:
        if instruction.opcode == IROpcode.SCAN_PROCESSES:
            return self.scan_processes()

        if instruction.opcode == IROpcode.SCAN_NETWORK:
            return self.scan_network()

        if instruction.opcode == IROpcode.SCAN_DNS:
            return self.scan_dns()

        if instruction.opcode == IROpcode.SCAN_LOGS:
            return self.scan_logs()

        raise ValueError(
            f"Unsupported IR opcode: {instruction.opcode}"
        )

    def scan_processes(self) -> dict:
        processes = collect_processes()

        return {
            "operation": "SCAN_PROCESSES",
            "platform": "Windows",
            "status": "success",
            "data": processes,
        }

    def scan_network(self) -> dict:
        connections = collect_network()

        return {
            "operation": "SCAN_NETWORK",
            "platform": "Windows",
            "status": "success",
            "data": connections,
        }

    def scan_dns(self) -> dict:
        entries = collect_dns()

        return {
            "operation": "SCAN_DNS",
            "platform": "Windows",
            "status": "success",
            "data": entries,
        }

    def scan_logs(self) -> dict:
        logs = collect_logs()

        return {
            "operation": "SCAN_LOGS",
            "platform": "Windows",
            "status": "success",
            "data": logs,
        }