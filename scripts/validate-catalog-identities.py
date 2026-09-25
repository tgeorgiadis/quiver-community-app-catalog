#!/usr/bin/env python3
"""Verify optional catalog IDs are production-shaped and unique."""
import json
import re
import sys
from pathlib import Path


def validate(files):
    seen = set()
    checked = 0
    for path in files:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for entry in data.get("apps", []):
            if "catalogId" not in entry:
                continue  # No backfill requirement.
            identity = entry["catalogId"]
            if not isinstance(identity, str) or not re.fullmatch(r"qcat_[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}", identity):
                raise ValueError("Invalid or non-production catalogId")
            if identity in seen:
                raise ValueError("Duplicate catalogId across catalog lists")
            seen.add(identity)
            checked += 1
    return checked


if __name__ == "__main__":
    try:
        count = validate(sys.argv[1:])
        print(f"Verified {count} catalog identities")
    except Exception as error:
        print(f"Catalog identity validation failed: {error}", file=sys.stderr)
        sys.exit(1)
