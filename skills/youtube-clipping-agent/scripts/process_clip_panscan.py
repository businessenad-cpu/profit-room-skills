#!/usr/bin/env python3
"""
Pan/scan clip processor.

Instead of a single static crop, samples focal_x at every second using
motion-based detection, smooths the trajectory, and animates the FFmpeg
crop filter to follow the action.

Usage:
    python3 process_clip_panscan.py <video> <start> <end> <rank> "<title>" <output> [--subtitle "<text>"]
"""

import argparse
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from text_overlay import get_drawtext_filter
from utils import format_file_size


# ── Focal-point detection ────────────────────────────────────────────────────

def detect_focal_x_per_second(video_path: str, start: float, end: float) -> list[float]:
    """
    Return a list of focal_x values — one per second from start to end.
    Uses motion (frame-difference) to find the most active horizontal region.
    Falls back to center if a frame can't be read.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = end - start
    n_samples = max(2, math.ceil(duration) + 1)   # keyframe at each integer second
    timestamps = [start + i * (duration / (n_samples - 1)) for i in range(n_samples)]

    def read_frame(t):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ret, frame = cap.read()
        return frame if ret else None

    focal_xs = []
    prev_gray = None

    for t in timestamps:
        frame = read_frame(t)
        if frame is None:
            focal_xs.append(width / 2.0)
            prev_gray = None
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None and prev_gray.shape == gray.shape:
            # Motion map: absolute difference from previous sampled frame
            diff = cv2.absdiff(gray, prev_gray).astype(np.float32)
        else:
            # Fallback: use Laplacian (high-frequency = interesting content)
            diff = cv2.Laplacian(gray, cv2.CV_32F)
            diff = np.abs(diff)

        # Sum motion per column, then find the centroid (weighted average x)
        col_motion = diff.sum(axis=0)   # shape: (width,)
        total = col_motion.sum()
        if total > 0:
            col_indices = np.arange(width, dtype=np.float32)
            focal_x = float(np.dot(col_indices, col_motion) / total)
        else:
            focal_x = width / 2.0

        focal_xs.append(focal_x)
        prev_gray = gray

    cap.release()
    return focal_xs


def focal_to_crop_x(focal_x: float, width: int, crop_w: int) -> int:
    """Convert focal_x to clamped crop_x."""
    x = int(focal_x - crop_w / 2)
    return max(0, min(x, width - crop_w))


def smooth(values: list[float], window: int = 3) -> list[float]:
    """Simple moving-average smoothing."""
    out = []
    for i, v in enumerate(values):
        lo = max(0, i - window // 2)
        hi = min(len(values), i + window // 2 + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


# ── FFmpeg expression builder ────────────────────────────────────────────────

def build_crop_x_expr(crop_xs: list[int], duration: float) -> str:
    """
    Build a piecewise-linear FFmpeg expression for animated crop_x.
    Each pair of keyframes (at integer seconds) interpolates linearly.
    """
    n = len(crop_xs)
    if n == 1:
        return str(crop_xs[0])

    # t intervals: evenly spaced over [0, duration]
    times = [i * duration / (n - 1) for i in range(n)]

    # Build nested if-else: if(lt(t, t1), lerp(x0,x1,t/t1), if(lt(t, t2), ..., xN))
    # FFmpeg doesn't have lerp, so we inline: x0 + (x1-x0) * (t - t0) / (t1 - t0)
    def segment_expr(x0, x1, t0, t1):
        if t1 <= t0 or x0 == x1:
            return str(x0)
        slope = (x1 - x0) / (t1 - t0)
        if slope == 0:
            return str(x0)
        return f"({x0}+({slope:.4f})*(t-({t0:.4f})))"

    # Build from right to left
    expr = str(crop_xs[-1])
    for i in range(n - 2, -1, -1):
        seg = segment_expr(crop_xs[i], crop_xs[i + 1], times[i], times[i + 1])
        expr = f"if(lt(t,{times[i+1]:.4f}),{seg},{expr})"

    return expr


# ── Main processing ──────────────────────────────────────────────────────────

def process_clip_panscan(video_path: str, start: float, end: float,
                         rank: int, title: str, output_path: str,
                         subtitle: str = "") -> dict:
    duration = end - start

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    crop_h = height
    crop_w = (math.floor(height * 9 / 16)) & ~1  # even number

    print(f"Sampling motion for pan/scan ({start:.1f}s - {end:.1f}s) ...", file=sys.stderr)
    focal_xs = detect_focal_x_per_second(video_path, start, end)
    smoothed = smooth(focal_xs, window=3)
    crop_xs = [focal_to_crop_x(fx, width, crop_w) for fx in smoothed]

    print(f"  Keyframe crop_x values: {crop_xs}", file=sys.stderr)

    crop_x_expr = build_crop_x_expr(crop_xs, duration)

    # Build drawtext overlay
    drawtext = get_drawtext_filter(rank, title, subtitle=subtitle, duration=min(duration, 4.0))

    vf = (
        f"crop={crop_w}:{crop_h}:'{crop_x_expr}':0,"
        f"scale=1080:1920,"
        f"{drawtext}"
    )

    print(f"Encoding pan/scan clip ({duration:.1f}s) ...", file=sys.stderr)
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", video_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(result.stderr.decode()[-600:], file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(output_path)
    print(f"Done: 1080x1920  {format_file_size(size)}", file=sys.stderr)

    return {
        "output_path": output_path,
        "duration": duration,
        "resolution": "1080x1920",
        "file_size": size,
        "crop_method": "pan_scan",
        "crop_keyframes": crop_xs,
        "success": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Pan/scan clip processor")
    parser.add_argument("video")
    parser.add_argument("start", type=float)
    parser.add_argument("end", type=float)
    parser.add_argument("rank", type=int)
    parser.add_argument("title")
    parser.add_argument("output")
    parser.add_argument("--subtitle", default="")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"Error: file not found '{args.video}'", file=sys.stderr)
        sys.exit(1)

    result = process_clip_panscan(args.video, args.start, args.end,
                                  args.rank, args.title, args.output,
                                  subtitle=args.subtitle)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
