#!/usr/bin/env python3
"""
Generate a single infographic image via Google Gemini API (gemini-3.1-flash-image-preview).
Usage: python generate_image.py "<prompt>" <output_path> [aspect_ratio] [resolution]

aspect_ratio options: "1:1","16:9","4:3","3:4","9:16" (default: "16:9")
resolution options: "512","1K","2K","4K" (default: "2K")
"""
import sys
from google import genai
from google.genai import types

def generate_image(prompt: str, output_path: str, aspect_ratio: str = "16:9", resolution: str = "2K"):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            ),
        )
    )

    for part in response.parts:
        if image := part.as_image():
            image.save(output_path)
            print(f"SAVED:{output_path}")
            return

    # Print any text response for debugging
    for part in response.parts:
        if part.text:
            print(f"TEXT:{part.text}", file=sys.stderr)

    print("ERROR: No image returned in response", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_image.py '<prompt>' <output_path> [aspect_ratio] [resolution]", file=sys.stderr)
        sys.exit(1)
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    aspect_ratio = sys.argv[3] if len(sys.argv) > 3 else "16:9"
    resolution = sys.argv[4] if len(sys.argv) > 4 else "2K"
    generate_image(prompt, output_path, aspect_ratio, resolution)
