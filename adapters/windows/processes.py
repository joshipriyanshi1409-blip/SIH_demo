import subprocess


def collect_processes() -> list[dict]:
    """Collect running Windows process information."""

    command = [
        "tasklist",
        "/FO",
        "CSV",
        "/NH",
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    processes = []

    for line in completed.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = [
            field.strip().strip('"')
            for field in line.split('","')
        ]

        if len(parts) < 5:
            continue

        processes.append(
            {
                "name": parts[0],
                "pid": parts[1],
                "session_name": parts[2],
                "session_number": parts[3],
                "memory_usage": parts[4],
            }
        )

    return processes