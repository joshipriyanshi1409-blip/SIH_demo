from evidence.builder import build_evidence_bundle
from evidence.models import EvidenceBundle, EvidenceRecord


def test_evidence_record_can_be_created():
    record = EvidenceRecord(
        host="HOST01",
        source="Windows",
        operation="SCAN_PROCESSES",
        timestamp="2026-01-01T00:00:00+00:00",
        data={
            "status": "success",
            "records": [],
        },
    )

    assert record.host == "HOST01"
    assert record.source == "Windows"
    assert record.operation == "SCAN_PROCESSES"


def test_evidence_bundle_can_be_created():
    record = EvidenceRecord(
        host="HOST01",
        source="Windows",
        operation="SCAN_NETWORK",
        timestamp="2026-01-01T00:00:00+00:00",
        data={
            "status": "success",
            "records": [],
        },
    )

    bundle = EvidenceBundle(
        host="HOST01",
        platform="Windows",
        records=(record,),
    )

    assert bundle.host == "HOST01"
    assert bundle.platform == "Windows"
    assert len(bundle.records) == 1


def test_builder_converts_results():
    results = [
        {
            "operation": "SCAN_PROCESSES",
            "platform": "Windows",
            "status": "success",
            "data": [
                {
                    "name": "example.exe",
                    "pid": "1234",
                }
            ],
        },
        {
            "operation": "SCAN_NETWORK",
            "platform": "Windows",
            "status": "success",
            "data": [
                {
                    "protocol": "TCP",
                    "local_address": "127.0.0.1:5000",
                }
            ],
        },
    ]

    bundle = build_evidence_bundle(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    assert bundle.host == "HOST01"
    assert bundle.platform == "Windows"
    assert len(bundle.records) == 2

    assert bundle.records[0].operation == "SCAN_PROCESSES"
    assert bundle.records[1].operation == "SCAN_NETWORK"
    