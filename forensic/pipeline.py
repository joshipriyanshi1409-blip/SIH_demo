from evidence.builder import build_evidence_bundle
from forensic.analyzer import analyze_evidence


def run_forensic_pipeline(
    host: str,
    platform: str,
    results: list[dict],
):
    """
    Convert raw adapter results into normalized evidence
    and analyze that evidence.
    """

    bundle = build_evidence_bundle(
        host=host,
        platform=platform,
        results=results,
    )

    findings = analyze_evidence(bundle)

    return bundle, findings