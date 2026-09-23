from evidence.models import EvidenceBundle
from forensic.findings import Finding


def analyze_evidence(bundle: EvidenceBundle) -> list[Finding]:
    """Analyze normalized evidence and produce forensic findings."""

    findings: list[Finding] = []

    for record in bundle.records:
        if record.operation == "SCAN_PROCESSES":
            findings.extend(
                _analyze_processes(
                    bundle.host,
                    record.data,
                )
            )

        elif record.operation == "SCAN_NETWORK":
            findings.extend(
                _analyze_network(
                    bundle.host,
                    record.data,
                )
            )

        elif record.operation == "SCAN_DNS":
            findings.extend(
                _analyze_dns(
                    bundle.host,
                    record.data,
                )
            )

        elif record.operation == "SCAN_LOGS":
            findings.extend(
                _analyze_logs(
                    bundle.host,
                    record.data,
                )
            )

    return findings


def _analyze_processes(
    host: str,
    data: dict,
) -> list[Finding]:
    records = data.get("records", [])

    findings = []

    for process in records:
        name = str(process.get("name", "")).lower()

        if name in {
            "powershell.exe",
            "cmd.exe",
        }:
            findings.append(
                Finding(
                    host=host,
                    category="PROCESS",
                    severity="INFO",
                    title="Command Shell Process Observed",
                    description=(
                        f"{process.get('name')} was observed "
                        "during the investigation."
                    ),
                    evidence=process,
                )
            )

    return findings


def _analyze_network(
    host: str,
    data: dict,
) -> list[Finding]:
    records = data.get("records", [])

    findings = []

    for connection in records:
        state = str(
            connection.get("state", "")
        ).upper()

        if state == "LISTENING":
            findings.append(
                Finding(
                    host=host,
                    category="NETWORK",
                    severity="INFO",
                    title="Listening Network Service Observed",
                    description=(
                        "A listening network endpoint was observed "
                        "during the investigation."
                    ),
                    evidence=connection,
                )
            )

    return findings


def _analyze_dns(
    host: str,
    data: dict,
) -> list[Finding]:
    return []


def _analyze_logs(
    host: str,
    data: dict,
) -> list[Finding]:
    return []