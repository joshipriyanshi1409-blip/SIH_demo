import platform

import pytest

from adapters.windows.dns import collect_dns


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows DNS collection requires Windows",
)
def test_collect_dns_returns_list():
    entries = collect_dns()

    assert isinstance(entries, list)


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows DNS collection requires Windows",
)
def test_dns_entries_have_structured_fields():
    entries = collect_dns()

    if not entries:
        pytest.skip("No DNS cache entries found")

    entry = entries[0]

    assert isinstance(entry, dict)
    assert "record_name" in entry


@pytest.mark.skipif(
    platform.system() != "Windows",
    reason="Windows DNS collection requires Windows",
)
def test_dns_record_names_are_strings():
    entries = collect_dns()

    for entry in entries:
        assert isinstance(entry["record_name"], str)
        assert entry["record_name"] != ""
        