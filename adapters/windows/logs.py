import json
import subprocess


def collect_logs(limit: int = 100) -> list[dict]:
    """Collect recent Windows event-log records."""

    if limit <= 0:
        raise ValueError("limit must be greater than zero")

    script = f"""
Get-WinEvent -LogName System -MaxEvents {limit} |
Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message |
ConvertTo-Json -Compress
"""

    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = completed.stdout.strip()

    if not output:
        return []

    parsed = json.loads(output)

    if isinstance(parsed, dict):
        parsed = [parsed]

    return parsed