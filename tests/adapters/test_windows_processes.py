import platform

import pytest

from adapters.windows.processes import collect_processes


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows process collection requires Windows",
)
def test_collect_processes_returns_list():
    processes = collect_processes()

    assert isinstance(processes, list)


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows process collection requires Windows",
)
def test_collected_processes_have_expected_fields():
    processes = collect_processes()

    assert len(processes) > 0

    process = processes[0]

    assert "name" in process
    assert "pid" in process
    assert "session_name" in process
    assert "session_number" in process
    assert "memory_usage" in process


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows process collection requires Windows",
)
def test_process_names_are_strings():
    processes = collect_processes()

    assert len(processes) > 0

    for process in processes[:10]:
        assert isinstance(process["name"], str)
        assert process["name"] != ""
        