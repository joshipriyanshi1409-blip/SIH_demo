from datetime import datetime, timezone

from evidence.models import EvidenceBundle, EvidenceRecord


def build_evidence_bundle(
    host: str,
    platform: str,
    results: list[dict],
) -> EvidenceBundle:
    """Convert adapter results into the common evidence format."""

    records = []

    timestamp = datetime.now(timezone.utc).isoformat()

    for result in results:
        records.append(
            EvidenceRecord(
                host=host,
                source=platform,
                operation=result["operation"],
                timestamp=timestamp,
                data={
                    "status": result["status"],
                    "records": result["data"],
                },
            )
        )

    return EvidenceBundle(
        host=host,
        platform=platform,
        records=tuple(records),
    )