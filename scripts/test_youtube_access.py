#!/usr/bin/env python3
"""
Test YouTube subtitle extraction access
Checks if IP blocking has been lifted
"""

import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# Test with youtube-transcript-api directly
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
except ImportError:
    print("ERROR: youtube-transcript-api not installed")
    print("Run: pip install youtube-transcript-api")
    sys.exit(1)

# Test video: 1.5周年 Part 1
TEST_VIDEO_ID = "Dzd3tboRPWI"
TEST_VIDEO_NAME = "1.5周年 LAST KINGDOM Part 1"

def test_youtube_access():
    """Test if YouTube subtitle extraction works"""
    print("=" * 70)
    print("YouTube Access Test")
    print("=" * 70)
    print(f"\nTest Video: {TEST_VIDEO_NAME}")
    print(f"Video ID: {TEST_VIDEO_ID}")
    print(f"URL: https://youtu.be/{TEST_VIDEO_ID}")
    print(f"Test Time: {datetime.now().isoformat()}")
    print()

    try:
        print("Attempting to fetch transcript list...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(TEST_VIDEO_ID)

        print("✓ Successfully accessed YouTube!")
        print("\nAvailable transcripts:")

        available_transcripts = []
        for transcript in transcript_list:
            lang_code = transcript.language_code
            lang_name = transcript.language
            is_generated = transcript.is_generated
            is_translatable = transcript.is_translatable

            print(f"  - {lang_name} ({lang_code})")
            print(f"    Generated: {is_generated}, Translatable: {is_translatable}")

            available_transcripts.append({
                "language": lang_name,
                "language_code": lang_code,
                "is_generated": is_generated,
                "is_translatable": is_translatable
            })

        # Try to fetch Japanese transcript
        print("\nAttempting to fetch Japanese transcript...")
        try:
            transcript = transcript_list.find_transcript(['ja'])
            subtitle_data = transcript.fetch()

            print(f"✓ Successfully fetched Japanese transcript!")
            print(f"  Segments: {len(subtitle_data)}")
            print(f"  Sample (first 3 segments):")
            for i, segment in enumerate(subtitle_data[:3]):
                print(f"    [{segment['start']:.1f}s] {segment['text']}")

            result = {
                "status": "SUCCESS",
                "ip_blocked": False,
                "video_id": TEST_VIDEO_ID,
                "video_name": TEST_VIDEO_NAME,
                "available_transcripts": available_transcripts,
                "japanese_transcript": {
                    "segments": len(subtitle_data),
                    "sample": subtitle_data[:5]
                },
                "test_time": datetime.now(timezone.utc).isoformat(),
                "message": "YouTube access is working! IP block has been lifted."
            }

            return result

        except NoTranscriptFound:
            print("⚠ No Japanese transcript found for this video")
            result = {
                "status": "PARTIAL_SUCCESS",
                "ip_blocked": False,
                "video_id": TEST_VIDEO_ID,
                "available_transcripts": available_transcripts,
                "error": "No Japanese transcript available",
                "test_time": datetime.now(timezone.utc).isoformat(),
                "message": "YouTube access works, but this video has no Japanese subtitles"
            }
            return result

    except VideoUnavailable as e:
        print(f"✗ Video unavailable: {e}")
        result = {
            "status": "FAILED",
            "ip_blocked": False,
            "error_type": "VideoUnavailable",
            "error": str(e),
            "test_time": datetime.now(timezone.utc).isoformat(),
            "message": "Video is not available (may be private/deleted)"
        }
        return result

    except TranscriptsDisabled as e:
        print(f"✗ Transcripts disabled: {e}")
        result = {
            "status": "FAILED",
            "ip_blocked": False,
            "error_type": "TranscriptsDisabled",
            "error": str(e),
            "test_time": datetime.now(timezone.utc).isoformat(),
            "message": "Transcripts are disabled for this video"
        }
        return result

    except Exception as e:
        error_msg = str(e).lower()

        # Check for IP blocking indicators
        is_ip_blocked = any(keyword in error_msg for keyword in [
            'blocked', 'forbidden', '403', 'unavailable',
            'location', 'region', 'country'
        ])

        print(f"✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")

        if is_ip_blocked:
            print("\n⚠ IP BLOCKING DETECTED")
            print("YouTube access is still blocked from this IP address")

        result = {
            "status": "FAILED",
            "ip_blocked": is_ip_blocked,
            "error_type": type(e).__name__,
            "error": str(e),
            "test_time": datetime.now(timezone.utc).isoformat(),
            "message": "IP blocking detected" if is_ip_blocked else f"Unexpected error: {e}"
        }
        return result

def main():
    result = test_youtube_access()

    # Save result to file
    output_path = Path("/mnt/f/nikkerag/temp/youtube_access_test.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print("TEST RESULT")
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"IP Blocked: {result.get('ip_blocked', 'Unknown')}")
    print(f"Message: {result['message']}")
    print(f"\nResult saved to: {output_path}")
    print("=" * 70)

    # Return exit code based on result
    if result['status'] == 'SUCCESS':
        return 0
    elif result.get('ip_blocked'):
        return 2  # IP blocked
    else:
        return 1  # Other error

if __name__ == "__main__":
    sys.exit(main())
