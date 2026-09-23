from evidence.builder import build_evidence_bundle
from forensic.analyzer import analyze_evidence
from forensic.findings import Finding


def test_finding_can_be_created():
    finding = Finding(
        host="HOST01",
        category="PROCESS",
        severity="INFO",
        title="Test Finding",
        description="Test description",
        evidence={"name": "example.exe"},
    )

    assert finding.host == "HOST01"
    assert finding.category == "PROCESS"
    assert finding.severity == "INFO"


def test_process_analysis_creates_finding():
    results = [
        {
            "operation": "SCAN_PROCESSES",
            "platform": "Windows",
            "status": "success",
            "data": [
                {
                    "name": "powershell.exe",
                    "pid": "1234",
                }
            ],
        }
    ]

    bundle = build_evidence_bundle(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    findings = analyze_evidence(bundle)

    assert len(findings) == 1
    assert findings[0].category == "PROCESS"
    assert findings[0].title == "Command Shell Process Observed"


def test_network_analysis_creates_finding():
    results = [
        {
            "operation": "SCAN_NETWORK",
            "platform": "Windows",
            "status": "success",
            "data": [
                {
                    "protocol": "TCP",
                    "local_address": "0.0.0.0:445",
                    "remote_address": "0.0.0.0:0",
                    "state": "LISTENING",
                    "pid": "4",
                }
            ],
        }
    ]

    bundle = build_evidence_bundle(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    findings = analyze_evidence(bundle)

    assert len(findings) == 1
    assert findings[0].category == "NETWORK"
    assert findings[0].severity == "INFO"


def test_dns_analysis_currently_returns_no_findings():
    results = [
        {
            "operation": "SCAN_DNS",
            "platform": "Windows",
            "status": "success",
            "data": [],
        }
    ]

    bundle = build_evidence_bundle(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    findings = analyze_evidence(bundle)

    assert findings == []


def test_logs_analysis_currently_returns_no_findings():
    results = [
        {
            "operation": "SCAN_LOGS",
            "platform": "Windows",
            "status": "success",
            "data": [],
        }
    ]

    bundle = build_evidence_bundle(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    findings = analyze_evidence(bundle)

    assert findings == []

from forensic.pipeline import run_forensic_pipeline


def test_forensic_pipeline_end_to_end():
    results = [
        {
            "operation": "SCAN_PROCESSES",
            "platform": "Windows",
            "status": "success",
            "data": [
                {
                    "name": "powershell.exe",
                    "pid": "4321",
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
                    "local_address": "0.0.0.0:445",
                    "remote_address": "0.0.0.0:0",
                    "state": "LISTENING",
                    "pid": "4",
                }
            ],
        },
    ]

    bundle, findings = run_forensic_pipeline(
        host="HOST01",
        platform="Windows",
        results=results,
    )

    assert bundle.host == "HOST01"
    assert bundle.platform == "Windows"
    assert len(bundle.records) == 2

    assert len(findings) == 2
    assert findings[0].category == "PROCESS"
    assert findings[1].category == "NETWORK"    