#!/usr/bin/env python3
"""
Convert VTT subtitle files to JSON transcript format
Handles YouTube VTT subtitles with timing markers
"""

import json
import re
from pathlib import Path
from datetime import timedelta

def parse_vtt_timestamp(timestamp_str):
    """Convert VTT timestamp (HH:MM:SS.mmm) to seconds"""
    parts = timestamp_str.strip().split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def clean_vtt_text(text):
    """Remove VTT timing markers and clean text"""
    # Remove inline timing markers like <00:00:14.440>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    # Remove <c> tags
    text = re.sub(r'</?c>', '', text)
    # Clean whitespace
    text = ' '.join(text.split())
    return text.strip()

def parse_vtt_file(vtt_path):
    """Parse VTT file and extract transcript segments"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into blocks
    blocks = content.split('\n\n')

    transcript = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        # Look for timestamp line
        timestamp_line = None
        text_lines = []

        for line in lines:
            if '-->' in line:
                timestamp_line = line
            elif line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:'):
                text_lines.append(line)

        if not timestamp_line or not text_lines:
            continue

        # Parse timestamps
        match = re.match(r'([\d:\.]+)\s*-->\s*([\d:\.]+)', timestamp_line)
        if not match:
            continue

        start_time = parse_vtt_timestamp(match.group(1))
        end_time = parse_vtt_timestamp(match.group(2))
        duration = end_time - start_time

        # Clean and combine text
        text = ' '.join(text_lines)
        text = clean_vtt_text(text)

        if text:
            transcript.append({
                "text": text,
                "start": start_time,
                "duration": duration
            })

    return transcript

def get_video_metadata(video_id):
    """Get video metadata based on video ID"""
    # Map video IDs to event names
    video_map = {
        "Dzd3tboRPWI": {
            "title": "【NIKKE】1.5周年 LAST KINGDOM Part I",
            "event": "1.5eventI"
        },
        "iylYYFpP8GY": {
            "title": "【NIKKE】1.5周年 LAST KINGDOM Part II",
            "event": "1.5eventII"
        },
        "3JvQgROQA2I": {
            "title": "【NIKKE】2.5周年 Part I",
            "event": "2.5eventI"
        },
        "4onDZs7yJ6E": {
            "title": "【NIKKE】2.5周年 Part II",
            "event": "2.5eventII"
        }
    }

    return video_map.get(video_id, {
        "title": f"Unknown video {video_id}",
        "event": f"unknown_{video_id}"
    })

def format_duration(seconds):
    """Convert seconds to HH:MM:SS format"""
    td = timedelta(seconds=int(seconds))
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def convert_vtt_to_json(vtt_path, output_path=None):
    """Convert VTT file to JSON transcript format"""
    vtt_path = Path(vtt_path)

    # Extract video ID from filename
    # Handle both "0.5eventEx_Dzd3tboRPWI.ja.vtt" and "test_Dzd3tboRPWI.ja.vtt"
    filename = vtt_path.stem  # Remove .vtt extension
    if filename.endswith('.ja'):
        filename = filename[:-3]  # Remove .ja

    # Extract video ID (11 characters at the end)
    video_id = filename[-11:]

    # Get metadata
    metadata = get_video_metadata(video_id)

    # Parse VTT
    print(f"Parsing {vtt_path.name}...")
    transcript = parse_vtt_file(vtt_path)

    # Calculate duration from last segment
    duration_seconds = 0
    if transcript:
        last_segment = transcript[-1]
        duration_seconds = last_segment["start"] + last_segment["duration"]

    # Build JSON structure
    result = {
        "video_id": video_id,
        "url": f"https://youtu.be/{video_id}",
        "title": metadata["title"],
        "duration": format_duration(duration_seconds),
        "language": "ja",
        "transcript": transcript
    }

    # Determine output path
    if output_path is None:
        output_path = vtt_path.parent / f"{metadata['event']}_transcript.json"

    # Save JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✓ Converted to {output_path.name}")
    print(f"  Segments: {len(transcript)}")
    print(f"  Duration: {result['duration']}")
    print(f"  Event: {metadata['event']}")
    print()

    return result

def main():
    """Process all VTT files in temp directory"""
    temp_dir = Path("/mnt/f/nikkerag/temp")

    # Find all VTT files with video IDs
    vtt_files = [
        temp_dir / "0.5eventEx_Dzd3tboRPWI.ja.vtt",  # 1.5周年 Part I
        temp_dir / "0.5eventEx_iylYYFpP8GY.ja.vtt",  # 1.5周年 Part II
        temp_dir / "0.5eventEx_3JvQgROQA2I.ja.vtt",  # 2.5周年 Part I
        temp_dir / "0.5eventEx_4onDZs7yJ6E.ja.vtt",  # 2.5周年 Part II
    ]

    print("=" * 70)
    print("VTT to JSON Converter")
    print("=" * 70)
    print()

    results = []
    for vtt_file in vtt_files:
        if vtt_file.exists():
            try:
                result = convert_vtt_to_json(vtt_file)
                results.append(result)
            except Exception as e:
                print(f"✗ Error processing {vtt_file.name}: {e}")
                print()
        else:
            print(f"⚠ File not found: {vtt_file.name}")
            print()

    print("=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    print(f"Successfully converted: {len(results)}/4 files")
    for result in results:
        print(f"  ✓ {result['title']}")
    print()

if __name__ == "__main__":
    main()
