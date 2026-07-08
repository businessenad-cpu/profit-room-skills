#!/usr/bin/env python3
"""
Validate and normalize Claude's ranked item JSON output.

Accepts a JSON file containing an array of ranked items with timestamps,
validates fields, normalizes timestamps to seconds, checks for overlaps
and duration bounds, and outputs validated JSON to stdout.
"""

import argparse
import json
import sys

from utils import time_to_seconds


def parse_timestamp(value):
    """Convert a timestamp value (string or number) to seconds."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return time_to_seconds(value)
    raise ValueError(f"Invalid timestamp type: {type(value)}")


def validate_item(item, index):
    """Validate a single ranked item and return normalized form plus warnings."""
    warnings = []

    # Validate rank
    rank = item.get("rank")
    if rank is None:
        raise ValueError(f"Item at index {index}: missing 'rank'")
    if not isinstance(rank, int):
        try:
            rank = int(rank)
        except (ValueError, TypeError):
            raise ValueError(f"Item at index {index}: 'rank' must be an integer, got {rank!r}")

    # Validate title
    title = item.get("title", "")
    if not title:
        warnings.append(f"Item {index}: missing or empty title")
        title = f"Untitled Item {rank}"

    # Parse timestamps
    try:
        start_seconds = parse_timestamp(item["start_time"])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Item at index {index} (rank {rank}): invalid start_time - {e}")

    try:
        end_seconds = parse_timestamp(item["end_time"])
    except (KeyError, ValueError) as e:
        raise ValueError(f"Item at index {index} (rank {rank}): invalid end_time - {e}")

    if end_seconds <= start_seconds:
        raise ValueError(
            f"Item at index {index} (rank {rank}): end_time ({end_seconds}s) "
            f"must be after start_time ({start_seconds}s)"
        )

    duration = round(end_seconds - start_seconds, 3)

    # Duration bounds warnings
    if duration < 10:
        warnings.append(f"Rank {rank}: duration is very short ({duration}s < 10s)")
    if duration > 300:
        warnings.append(f"Rank {rank}: duration is very long ({duration}s > 300s)")

    description = item.get("description", "")
    overlay_text = f"#{rank} - {title}"

    return {
        "rank": rank,
        "title": title,
        "start_seconds": round(start_seconds, 3),
        "end_seconds": round(end_seconds, 3),
        "duration": duration,
        "description": description,
        "overlay_text": overlay_text,
        "warnings": warnings,
    }


def check_overlaps(items):
    """Check for overlaps between consecutive items sorted by start_time."""
    warnings = []
    sorted_by_start = sorted(items, key=lambda x: x["start_seconds"])

    for i in range(len(sorted_by_start) - 1):
        a = sorted_by_start[i]
        b = sorted_by_start[i + 1]
        if a["end_seconds"] > b["start_seconds"]:
            overlap = round(a["end_seconds"] - b["start_seconds"], 3)
            warnings.append(
                f"Item {a['rank']} and {b['rank']} overlap by {overlap} seconds"
            )

    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate and normalize ranked item JSON from Claude's analysis."
    )
    parser.add_argument("json_file", help="Path to JSON file containing ranked items array")
    parser.add_argument("--output", help="Write validated JSON to this file instead of stdout")
    args = parser.parse_args()

    # Read input
    try:
        with open(args.json_file, "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {args.json_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {args.json_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Accept either a bare array or an object with an "items" key
    if isinstance(raw_data, list):
        raw_items = raw_data
    elif isinstance(raw_data, dict) and "items" in raw_data:
        raw_items = raw_data["items"]
    else:
        print("Error: expected a JSON array or an object with an 'items' key", file=sys.stderr)
        sys.exit(1)

    if not raw_items:
        print("Error: no items found in input", file=sys.stderr)
        sys.exit(1)

    # Validate each item
    validated = []
    global_warnings = []
    fatal = False

    for i, item in enumerate(raw_items):
        try:
            result = validate_item(item, i)
            validated.append(result)
        except ValueError as e:
            print(f"Warning: skipping item - {e}", file=sys.stderr)
            global_warnings.append(str(e))

    if not validated:
        print("Error: no valid items after validation", file=sys.stderr)
        sys.exit(1)

    # Sort by rank ascending
    validated.sort(key=lambda x: x["rank"])

    # Check overlaps
    overlap_warnings = check_overlaps(validated)
    global_warnings.extend(overlap_warnings)

    # Build output
    total_duration = round(sum(item["duration"] for item in validated), 3)

    output = {
        "items": validated,
        "total_items": len(validated),
        "total_duration": total_duration,
        "warnings": global_warnings,
    }

    json_output = json.dumps(output, indent=2, ensure_ascii=False)

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(json_output + "\n")
        print(f"Validated {len(validated)} items -> {args.output}", file=sys.stderr)
    else:
        print(json_output)

    # Print summary to stderr
    if global_warnings:
        print(f"\n{len(global_warnings)} warning(s):", file=sys.stderr)
        for w in global_warnings:
            print(f"  - {w}", file=sys.stderr)

    print(
        f"\nSummary: {len(validated)} items, {total_duration}s total duration",
        file=sys.stderr,
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
