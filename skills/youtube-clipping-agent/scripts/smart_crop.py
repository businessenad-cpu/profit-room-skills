#!/usr/bin/env python3
"""
Smart 9:16 crop detection for horizontal video.

Uses OpenCV Haar cascade face detection to find a focal point,
then computes a vertical (9:16) crop window centered on detected faces.
Falls back to center crop when no faces are found.

Output: JSON to stdout with crop parameters.
"""

import argparse
import json
import math
import sys
from typing import Optional, Tuple

import cv2


def detect_focal_x(video_path: str, start_seconds: float, end_seconds: float,
                   sample_interval: float = 2.0) -> Tuple[Optional[float], str]:
    """
    Sample frames from the video and detect faces to find a weighted
    average horizontal focal point.

    Returns:
        (focal_x, detection_method) where focal_x is None if no faces found.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: cannot open video '{video_path}'", file=sys.stderr)
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("Error: cannot determine video FPS", file=sys.stderr)
        sys.exit(1)

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        print("Error: failed to load Haar cascade", file=sys.stderr)
        sys.exit(1)

    total_weight = 0.0
    weighted_x_sum = 0.0
    t = start_seconds

    while t <= end_seconds:
        frame_number = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            t += sample_interval
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            center_x = x + w / 2.0
            area = w * h
            weighted_x_sum += center_x * area
            total_weight += area

        t += sample_interval

    cap.release()

    if total_weight > 0:
        return weighted_x_sum / total_weight, "face_detection"
    return None, "center_fallback"


def compute_crop(video_path: str, focal_x: Optional[float],
                 detection_method: str) -> dict:
    """Compute 9:16 crop rectangle given a focal x position."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: cannot open video '{video_path}'", file=sys.stderr)
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    if width <= 0 or height <= 0:
        print("Error: cannot determine video dimensions", file=sys.stderr)
        sys.exit(1)

    crop_h = height
    crop_w = math.floor(height * 9 / 16)
    crop_w &= ~1  # ensure even

    if focal_x is None:
        focal_x = width / 2.0

    crop_x = int(focal_x - crop_w // 2)
    crop_x = max(0, min(crop_x, width - crop_w))
    crop_y = 0

    return {
        "crop_x": crop_x,
        "crop_y": crop_y,
        "crop_width": crop_w,
        "crop_height": crop_h,
        "detection_method": detection_method,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Detect focal point and compute 9:16 crop for a video.")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("start_seconds", type=float,
                        help="Start time in seconds")
    parser.add_argument("end_seconds", type=float,
                        help="End time in seconds")
    parser.add_argument("--sample-interval", type=float, default=2.0,
                        help="Seconds between sampled frames (default: 2)")
    args = parser.parse_args()

    import os
    if not os.path.isfile(args.video_path):
        print(f"Error: file not found '{args.video_path}'", file=sys.stderr)
        sys.exit(1)

    if args.start_seconds < 0 or args.end_seconds <= args.start_seconds:
        print("Error: invalid time range", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing video: {args.video_path}", file=sys.stderr)
    print(f"Time range: {args.start_seconds}s - {args.end_seconds}s", file=sys.stderr)

    focal_x, method = detect_focal_x(
        args.video_path, args.start_seconds, args.end_seconds,
        args.sample_interval)

    print(f"Detection method: {method}", file=sys.stderr)

    result = compute_crop(args.video_path, focal_x, method)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
