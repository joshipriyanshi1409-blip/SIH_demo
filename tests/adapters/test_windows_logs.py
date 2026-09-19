import platform

import pytest

from adapters.windows.logs import collect_logs


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows event-log collection requires Windows",
)
def test_collect_logs_returns_list():
    logs = collect_logs(limit=5)

    assert isinstance(logs, list)


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows event-log collection requires Windows",
)
def test_collect_logs_returns_structured_records():
    logs = collect_logs(limit=5)

    if not logs:
        pytest.skip("No System event records returned")

    record = logs[0]

    assert isinstance(record, dict)
    assert "TimeCreated" in record
    assert "Id" in record
    assert "ProviderName" in record


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows event-log collection requires Windows",
)
def test_collect_logs_respects_limit():
    logs = collect_logs(limit=5)

    assert len(logs) <= 5
    