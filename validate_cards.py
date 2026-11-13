#!/usr/bin/env python3
"""Validate the evidence-card format with Python's standard library.

This checks record structure only. It performs no network requests and cannot
establish whether a product claim, page or recorded observation is true.
"""

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


KEYS = {
    "schema_version", "project", "reference_url", "recorded_on", "illustrative",
    "source_summary", "checked_at", "observations", "unverified", "next_check",
}
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})")


def timestamp(value):
    if not isinstance(value, str) or not TIMESTAMP.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.utcoffset() is not None
    except ValueError:
        return False


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(card):
    """Return errors for this fixed format; this is not a general schema engine."""
    if not isinstance(card, dict):
        return ["card must be a JSON object"]
    errors = []
    missing = KEYS - card.keys()
    extra = card.keys() - KEYS
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("unexpected fields: " + ", ".join(sorted(extra)))
    if type(card.get("schema_version")) is not int or card["schema_version"] != 1:
        errors.append("schema_version must be the integer 1")
    for key in ("project", "source_summary", "next_check"):
        if not nonempty(card.get(key)):
            errors.append(key + " must be nonempty text")
    url = card.get("reference_url")
    try:
        parsed = urlsplit(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in url):
            errors.append("reference_url must be an HTTPS URL without credentials or whitespace")
    except ValueError:
        errors.append("reference_url is malformed")
    day = card.get("recorded_on")
    try:
        if not isinstance(day, str) or date.fromisoformat(day).isoformat() != day:
            errors.append("recorded_on must be YYYY-MM-DD")
    except ValueError:
        errors.append("recorded_on must be a valid calendar date")
    illustrative = card.get("illustrative")
    if type(illustrative) is not bool:
        errors.append("illustrative must be a boolean")
    checked = card.get("checked_at")
    if checked is not None and not timestamp(checked):
        errors.append("checked_at must be null or a timestamp with timezone")
    observations = card.get("observations")
    if not isinstance(observations, list):
        errors.append("observations must be an array")
    else:
        for index, observation in enumerate(observations):
            label = "observations[" + str(index) + "]"
            if not isinstance(observation, dict) or set(observation) != {"observed_at", "method", "result"}:
                errors.append(label + " must contain observed_at, method and result only")
                continue
            if not timestamp(observation["observed_at"]):
                errors.append(label + ".observed_at must include a timezone")
            if not nonempty(observation["method"]) or not nonempty(observation["result"]):
                errors.append(label + " method and result must be nonempty text")
        if observations and checked is None:
            errors.append("observations require a checked_at timestamp")
    questions = card.get("unverified")
    if not isinstance(questions, list) or not questions or not all(nonempty(q) for q in questions):
        errors.append("unverified must contain at least one nonempty limitation")
    if illustrative is True and (checked is not None or observations != []):
        errors.append("illustrative cards must leave checked_at null and observations empty")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cards", nargs="+", type=Path, help="JSON card files to check")
    args = parser.parse_args()
    failed = False
    for path in args.cards:
        try:
            errors = validate(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, ValueError) as error:
            errors = [str(error)]
        if errors:
            failed = True
            print(str(path) + ": INVALID\n  " + "\n  ".join(errors))
        else:
            print(str(path) + ": structure OK (product behavior not verified)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
