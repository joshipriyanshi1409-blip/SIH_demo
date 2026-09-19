import platform

import pytest

from adapters.windows.network import collect_network


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows network collection requires Windows",
)
def test_collect_network_returns_list():
    connections = collect_network()

    assert isinstance(connections, list)


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows network collection requires Windows",
)
def test_network_records_have_expected_fields():
    connections = collect_network()

    if not connections:
        pytest.skip("No active network connections found")

    connection = connections[0]

    assert "protocol" in connection
    assert "local_address" in connection
    assert "remote_address" in connection
    assert "state" in connection
    assert "pid" in connection


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows network collection requires Windows",
)
def test_network_protocols_are_supported():
    connections = collect_network()

    for connection in connections:
        assert connection["protocol"] in {"TCP", "UDP"}