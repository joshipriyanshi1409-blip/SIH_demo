from fastapi import FastAPI

from adapters.windows import WindowsAdapter
from api.models import InvestigationRequest, InvestigationResponse
from compiler.executor import Executor
from compiler.ir.instructions import IRInstruction, IROpcode
from forensic.pipeline import run_forensic_pipeline


app = FastAPI(
    title="JOCKY Forensics API",
    version="0.1.0",
)


CHECK_TO_OPCODE = {
    "PROCESSES": IROpcode.SCAN_PROCESSES,
    "NETWORK": IROpcode.SCAN_NETWORK,
    "DNS": IROpcode.SCAN_DNS,
    "LOGS": IROpcode.SCAN_LOGS,
}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "JOCKY",
    }


@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)
def investigate(request: InvestigationRequest):
    adapter = WindowsAdapter()
    executor = Executor(adapter)

    results = []

    for check in request.checks:
        check_name = check.upper()

        if check_name not in CHECK_TO_OPCODE:
            continue

        instruction = IRInstruction(
            CHECK_TO_OPCODE[check_name]
        )

        result = executor.execute_instruction(
            instruction
        )

        results.append(result)

    bundle, findings = run_forensic_pipeline(
        host=request.host,
        platform="Windows",
        results=results,
    )

    return InvestigationResponse(
        host=bundle.host,
        platform=bundle.platform,
        evidence_records=len(bundle.records),
        findings=[
            {
                "host": finding.host,
                "category": finding.category,
                "severity": finding.severity,
                "title": finding.title,
                "description": finding.description,
                "evidence": finding.evidence,
            }
            for finding in findings
        ],
    )