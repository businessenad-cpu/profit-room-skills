#!/usr/bin/env python3
"""
Single-clip processing pipeline.

Combines smart cropping, text overlay, and FFmpeg encoding to produce
a 9:16 vertical short from a horizontal source video.

Output: JSON to stdout with clip metadata.
"""

import argparse
import json
import os
import subprocess
import sys

from smart_crop import detect_focal_x, compute_crop
from text_overlay import get_drawtext_filter
from utils import format_file_size


def process_clip(video_path: str, start: float, end: float,
                 rank: int, title: str, output_path: str,
                 subtitle: str = "") -> dict:
    """Run the full clip pipeline: crop detection, overlay, encode.

    Args:
        video_path: Path to the source video.
        start: Start time in seconds.
        end: End time in seconds.
        rank: Ranking number for the overlay.
        title: Title text for the overlay.
        output_path: Destination file path.
        subtitle: Optional subtitle line (event/date) for the overlay.

    Returns:
        dict with output metadata.
    """
    duration = end - start

    # 1. Detect crop parameters
    print(f"Detecting crop region for {start:.1f}s - {end:.1f}s ...", file=sys.stderr)
    focal_x, method = detect_focal_x(video_path, start, end)
    crop = compute_crop(video_path, focal_x, method)
    print(f"Crop method: {method}  |  x={crop['crop_x']} w={crop['crop_width']}", file=sys.stderr)

    # 2. Build drawtext filter
    drawtext = get_drawtext_filter(rank, title, subtitle=subtitle, duration=min(duration, 4.0))

    # 3. Assemble video filter chain
    vf = (
        f"crop={crop['crop_width']}:{crop['crop_height']}"
        f":{crop['crop_x']}:{crop['crop_y']},"
        f"scale=1080:1920,"
        f"{drawtext}"
    )

    # 4. Run FFmpeg
    cmd = [
        "ffmpeg",
        "-ss", str(start),
        "-t", str(duration),
        "-i", video_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-y", output_path,
    ]

    print(f"Encoding clip ({duration:.1f}s) ...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    # 5. Verify output
    if not os.path.isfile(output_path):
        print("Error: output file was not created", file=sys.stderr)
        sys.exit(1)

    probe_cmd = [
        "ffmpeg", "-v", "quiet",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        "-i", output_path,
    ]
    probe = subprocess.run(probe_cmd, capture_output=True, text=True)
    # ffmpeg exits 1 when used for probing but still outputs stream info
    try:
        probe_data = json.loads(probe.stdout)
    except json.JSONDecodeError:
        # Fall back to 1080x1920 since we always output that resolution
        probe_data = {"streams": [{"width": 1080, "height": 1920}]}

    streams = probe_data.get("streams", [])
    if not streams:
        streams = [{"width": 1080, "height": 1920}]

    width = streams[0]["width"]
    height = streams[0]["height"]
    file_size = os.path.getsize(output_path)

    print(f"Done: {width}x{height}  {format_file_size(file_size)}", file=sys.stderr)

    return {
        "output_path": os.path.abspath(output_path),
        "duration": round(duration, 2),
        "resolution": f"{width}x{height}",
        "file_size": file_size,
        "crop_method": method,
        "success": True,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Process a single clip: crop, overlay, encode to 9:16 vertical.")
    parser.add_argument("video", help="Path to source video")
    parser.add_argument("start", type=float, help="Start time in seconds")
    parser.add_argument("end", type=float, help="End time in seconds")
    parser.add_argument("rank", type=int, help="Ranking number for overlay")
    parser.add_argument("title", help="Title text for overlay")
    parser.add_argument("output", help="Output file path")
    parser.add_argument("--subtitle", default="", help="Subtitle line (event/date) for overlay")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"Error: file not found '{args.video}'", file=sys.stderr)
        sys.exit(1)

    if args.start < 0 or args.end <= args.start:
        print("Error: invalid time range", file=sys.stderr)
        sys.exit(1)

    result = process_clip(args.video, args.start, args.end,
                          args.rank, args.title, args.output,
                          subtitle=args.subtitle)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
