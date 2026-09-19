import subprocess


def collect_network() -> list[dict]:
    """Collect active Windows network connections."""

    command = [
        "netstat",
        "-ano",
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    connections = []

    for line in completed.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) < 4:
            continue

        protocol = parts[0]

        if protocol not in {"TCP", "UDP"}:
            continue

        if protocol == "TCP" and len(parts) >= 5:
            connections.append(
                {
                    "protocol": protocol,
                    "local_address": parts[1],
                    "remote_address": parts[2],
                    "state": parts[3],
                    "pid": parts[4],
                }
            )

        elif protocol == "UDP" and len(parts) >= 4:
            connections.append(
                {
                    "protocol": protocol,
                    "local_address": parts[1],
                    "remote_address": "*:*",
                    "state": "NONE",
                    "pid": parts[3],
                }
            )

    return connections