#!/usr/bin/env python3
"""
Batch process all YouTube videos in YTlist.txt
"""
import sys
import os
import time
import re
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.process_youtube import get_video_id, get_transcript, format_timestamp


def read_ytlist(file_path='YTlist.txt'):
    """Read and parse YTlist.txt"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and 'youtu' in line:
                # Extract chapter number and URL
                parts = line.split()
                if len(parts) >= 2:
                    chapter = parts[0]
                    url = parts[1]
                    urls.append((chapter, url))
    return urls


def check_if_processed(video_id, output_dir='docs/videos'):
    """Check if video has already been processed"""
    output_dir = Path(output_dir)
    for file in output_dir.glob('*.md'):
        content = file.read_text(encoding='utf-8')
        if f'video_id: {video_id}' in content:
            return True, file.name
    return False, None


def process_video(chapter, url, output_dir='docs/videos'):
    """Process a single video"""
    print(f"\n{'='*60}")
    print(f"處理第 {chapter} 章")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        # Extract video ID
        video_id = get_video_id(url)
        print(f"影片 ID: {video_id}")

        # Check if already processed
        is_processed, filename = check_if_processed(video_id, output_dir)
        if is_processed:
            print(f"✓ 已處理過：{filename}")
            return 'skipped', video_id

        # Get transcript
        print("正在提取字幕...")
        transcript_data = get_transcript(video_id)

        # Calculate duration
        last_entry = transcript_data['transcript'][-1]
        total_seconds = last_entry['start'] + last_entry['duration']
        total_minutes = int(total_seconds // 60)
        total_secs = int(total_seconds % 60)

        print(f"✓ 語言: {transcript_data['language']}")
        print(f"✓ 字幕條目數: {len(transcript_data['transcript'])}")
        print(f"✓ 時長: {total_minutes}:{total_secs:02d}")

        # Show preview
        print("\n字幕預覽（前 3 條）:")
        for entry in transcript_data['transcript'][:3]:
            timestamp = format_timestamp(entry['start'])
            text = entry['text'][:50]
            print(f"  [{timestamp}] {text}...")

        # Save basic info for manual processing
        info_file = Path(output_dir) / f'_processing_{chapter}_{video_id}.txt'
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"Chapter: {chapter}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Language: {transcript_data['language']}\n")
            f.write(f"Duration: {total_minutes}:{total_secs:02d}\n")
            f.write(f"Entries: {len(transcript_data['transcript'])}\n")
            f.write(f"\nFirst 10 lines:\n")
            for i, entry in enumerate(transcript_data['transcript'][:10]):
                timestamp = format_timestamp(entry['start'])
                f.write(f"[{timestamp}] {entry['text']}\n")

        print(f"\n✓ 基本信息已保存: {info_file.name}")
        return 'info_saved', video_id

    except Exception as e:
        print(f"\n✗ 錯誤: {str(e)}")
        return 'error', str(e)


def main():
    """Main processing function"""
    print("開始批量處理 YTlist.txt 中的影片")
    print(f"當前時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Read YTlist
    ytlist_path = 'YTlist.txt'
    if not os.path.exists(ytlist_path):
        print(f"錯誤：找不到 {ytlist_path}")
        return

    urls = read_ytlist(ytlist_path)
    print(f"找到 {len(urls)} 個影片\n")

    # Create output directory
    output_dir = 'docs/videos'
    os.makedirs(output_dir, exist_ok=True)

    # Process each video
    results = {
        'skipped': [],
        'info_saved': [],
        'error': []
    }

    for chapter, url in urls:
        status, info = process_video(chapter, url, output_dir)
        results[status].append((chapter, info))

        # Small delay between requests
        time.sleep(1)

    # Print summary
    print(f"\n\n{'='*60}")
    print("處理完成統計")
    print(f"{'='*60}")
    print(f"已跳過（已處理）: {len(results['skipped'])} 個")
    print(f"信息已保存: {len(results['info_saved'])} 個")
    print(f"處理錯誤: {len(results['error'])} 個")

    if results['info_saved']:
        print(f"\n已保存基本信息的影片:")
        for chapter, video_id in results['info_saved']:
            print(f"  第 {chapter} 章: {video_id}")

    if results['error']:
        print(f"\n處理錯誤的影片:")
        for chapter, error in results['error']:
            print(f"  第 {chapter} 章: {error}")

    print(f"\n注意：由於影片數量較多，詳細文檔需要逐一生成")
    print(f"基本信息文件保存在: {output_dir}/_processing_*.txt")


if __name__ == "__main__":
    main()
