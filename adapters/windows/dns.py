import subprocess


def collect_dns() -> list[dict]:
    """Collect cached DNS resolver information from Windows."""

    command = [
        "ipconfig",
        "/displaydns",
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    entries = []

    current_entry = {}

    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()

        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = {}
            continue

        if line.startswith("Record Name"):
            if current_entry:
                entries.append(current_entry)
                current_entry = {}

            current_entry["record_name"] = line.split(":", 1)[1].strip()

        elif line.startswith("Record Type"):
            current_entry["record_type"] = line.split(":", 1)[1].strip()

        elif line.startswith("Time To Live"):
            current_entry["ttl"] = line.split(":", 1)[1].strip()

        elif line.startswith("Data Length"):
            current_entry["data_length"] = line.split(":", 1)[1].strip()

        elif line.startswith("Section"):
            current_entry["section"] = line.split(":", 1)[1].strip()

        elif line.startswith("A (Host) Record"):
            current_entry["a_record"] = line.split(":", 1)[1].strip()

        elif line.startswith("AAAA Record"):
            current_entry["aaaa_record"] = line.split(":", 1)[1].strip()

        elif line.startswith("CNAME Record"):
            current_entry["cname_record"] = line.split(":", 1)[1].strip()

        elif line.startswith("PTR Record"):
            current_entry["ptr_record"] = line.split(":", 1)[1].strip()

        elif line.startswith("SRV Record"):
            current_entry["srv_record"] = line.split(":", 1)[1].strip()

    if current_entry:
        entries.append(current_entry)

    return entries
