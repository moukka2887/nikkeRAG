#!/usr/bin/env python3
"""
Whisper ASR Batch Processor for NIKKE Anniversary Videos
Extracts Japanese speech from local video files using OpenAI Whisper
"""

import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import whisper

# Configuration
VIDEO_DIR = Path("/mnt/f/nikkerag/references/dlYTvideo")
OUTPUT_DIR = Path("/mnt/f/nikkerag/temp")
WHISPER_MODEL = "large-v3-turbo"  # Best balance of speed and accuracy

# Videos to process
VIDEOS = [
    {
        "id": "goddess_fall_1",
        "filename": "【勝利女神：妮姬NIKKE】三週年GODDESS FALL Story I 完整劇情 (2K) - 傲真翔也【戴永翔】 (360p, h264).mp4",
        "event_name": "3.0周年活动 GODDESS FALL Part 1",
        "estimated_duration_min": 25
    },
    {
        "id": "goddess_fall_2",
        "filename": "【勝利女神：妮姬NIKKE】三週年GODDESS FALL Story II 完整劇情 (2K) - 傲真翔也【戴永翔】 (360p, h264).mp4",
        "event_name": "3.0周年活动 GODDESS FALL Part 2",
        "estimated_duration_min": 25
    },
    {
        "id": "white_memory",
        "filename": "【勝利女神：妮姬】 WHITE MEMORY 全劇情 PC版 - 曉祭 (720p, h264).mp4",
        "event_name": "3.0周年活动 WHITE MEMORY",
        "estimated_duration_min": 21
    }
]


def load_whisper_model(model_name):
    """Load Whisper model with device detection"""
    print(f"\n=== Loading Whisper Model: {model_name} ===")
    start = time.time()

    # Let Whisper auto-detect CUDA/CPU
    model = whisper.load_model(model_name)

    elapsed = time.time() - start
    device = "CUDA" if next(model.parameters()).is_cuda else "CPU"
    print(f"✓ Model loaded in {elapsed:.1f}s (device: {device})")

    return model


def transcribe_video(model, video_path, video_id):
    """Transcribe video audio using Whisper"""
    print(f"\n{'='*70}")
    print(f"Processing: {video_id}")
    print(f"{'='*70}")

    if not video_path.exists():
        print(f"✗ Video not found: {video_path}")
        return None

    file_size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"Video: {file_size_mb:.1f} MB")

    print(f"🎙️ Transcribing with Whisper...")
    start_time = time.time()

    # Whisper transcription with Japanese language hint
    result = model.transcribe(
        str(video_path),
        language="ja",  # Japanese
        task="transcribe",  # Not translate
        verbose=False,
        word_timestamps=True  # Get word-level timestamps
    )

    processing_time = time.time() - start_time
    print(f"✓ Transcription complete in {processing_time/60:.1f} min")

    return result, processing_time


def convert_to_standard_format(whisper_result, video_info, processing_time):
    """Convert Whisper output to standard transcript JSON format"""

    # Extract segments with timestamps
    transcript = []
    for segment in whisper_result["segments"]:
        transcript.append({
            "text": segment["text"].strip(),
            "start": round(segment["start"], 2),
            "duration": round(segment["end"] - segment["start"], 2),
            "confidence": round(segment.get("no_speech_prob", 0.0), 3)  # Whisper confidence
        })

    # Calculate statistics
    total_duration = transcript[-1]["start"] + transcript[-1]["duration"] if transcript else 0
    duration_formatted = f"{int(total_duration) // 60}:{int(total_duration) % 60:02d}"

    avg_confidence = sum(s["confidence"] for s in transcript) / len(transcript) if transcript else 0

    # Build standard JSON structure
    output = {
        "video_id": video_info["id"],
        "source": "local_file",
        "file_path": str(VIDEO_DIR / video_info["filename"]),
        "chapter": None,
        "event_name": video_info["event_name"],
        "language": "ja",
        "duration": duration_formatted,
        "extraction_method": "whisper_asr",
        "extraction_date": datetime.now(timezone.utc).isoformat(),
        "transcript": transcript,
        "metadata": {
            "whisper_model": WHISPER_MODEL,
            "whisper_language": whisper_result.get("language", "ja"),
            "segment_count": len(transcript),
            "average_confidence": round(avg_confidence, 3),
            "processing_time_seconds": int(processing_time),
            "detected_language": whisper_result.get("language", "unknown"),
            "detected_language_probability": round(whisper_result.get("language_probability", 0.0), 3)
        }
    }

    return output


def main():
    print("="*70)
    print("Whisper ASR Batch Processor - NIKKE Anniversary Videos")
    print("="*70)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load Whisper model once
    model = load_whisper_model(WHISPER_MODEL)

    results = []
    total_start = time.time()

    # Process each video
    for video_info in VIDEOS:
        video_path = VIDEO_DIR / video_info["filename"]

        # Transcribe
        result = transcribe_video(model, video_path, video_info["id"])

        if result:
            whisper_result, processing_time = result

            # Convert to standard format
            transcript_json = convert_to_standard_format(
                whisper_result, video_info, processing_time
            )

            # Save to file
            output_path = OUTPUT_DIR / f"{video_info['id']}_transcript.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcript_json, f, ensure_ascii=False, indent=2)

            file_size_kb = output_path.stat().st_size / 1024

            print(f"✓ Saved: {output_path} ({file_size_kb:.1f} KB)")
            print(f"  Segments: {len(transcript_json['transcript'])}")
            print(f"  Language: {transcript_json['metadata']['detected_language']} "
                  f"({transcript_json['metadata']['detected_language_probability']:.2%})")
            print(f"  Duration: {transcript_json['duration']}")

            results.append({
                "video_id": video_info["id"],
                "segments": len(transcript_json['transcript']),
                "language": transcript_json['metadata']['detected_language'],
                "confidence": transcript_json['metadata']['detected_language_probability'],
                "file": str(output_path),
                "processing_time_min": round(processing_time / 60, 1)
            })

    # Summary
    total_time = time.time() - total_start

    print(f"\n{'='*70}")
    print("ASR PROCESSING COMPLETE")
    print(f"{'='*70}")

    print(f"\n✓ Processed {len(results)} videos in {total_time/60:.1f} min")

    for r in results:
        print(f"\n{r['video_id']}:")
        print(f"  - {r['segments']} segments")
        print(f"  - Language: {r['language']} ({r['confidence']:.2%} confidence)")
        print(f"  - Processing: {r['processing_time_min']} min")
        print(f"  - File: {r['file']}")

    print(f"\n✓ Ready for nikke-translation-calibrator agent")


if __name__ == "__main__":
    main()
