#!/usr/bin/env python3
"""
Safer batch processing with longer delays to avoid IP blocks
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


def check_if_info_extracted(chapter, video_id, output_dir='docs/videos'):
    """Check if basic info has been extracted"""
    output_dir = Path(output_dir)
    info_file = output_dir / f'_processing_{chapter}_{video_id}.txt'
    return info_file.exists()


def check_if_fully_processed(video_id, output_dir='docs/videos'):
    """Check if video has full documentation"""
    output_dir = Path(output_dir)
    for file in output_dir.glob('*.md'):
        if file.name.startswith('_processing'):
            continue
        content = file.read_text(encoding='utf-8')
        if f'video_id: {video_id}' in content:
            return True, file.name
    return False, None


def process_video(chapter, url, output_dir='docs/videos', delay=15):
    """Process a single video with safety measures"""
    print(f"\n{'='*60}")
    print(f"處理第 {chapter} 章")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        # Extract video ID
        video_id = get_video_id(url)
        print(f"影片 ID: {video_id}")

        # Check if fully processed
        is_fully_processed, filename = check_if_fully_processed(video_id, output_dir)
        if is_fully_processed:
            print(f"✓ 已完整處理：{filename}")
            return 'fully_processed', video_id

        # Check if info already extracted
        if check_if_info_extracted(chapter, video_id, output_dir):
            print(f"✓ 基本信息已提取過")
            return 'info_exists', video_id

        # Get transcript
        print("正在提取字幕...")
        print(f"(處理完成後將等待 {delay} 秒以避免 IP 封鎖)")

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

        # Save basic info
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

        # Important: delay after successful request
        print(f"等待 {delay} 秒...")
        time.sleep(delay)

        return 'info_saved', video_id

    except Exception as e:
        error_msg = str(e)
        if "blocking requests from your IP" in error_msg:
            print(f"\n✗ IP 封鎖：YouTube 已封鎖當前 IP")
            print("建議：等待數小時後再試，或使用 VPN/代理")
            return 'ip_blocked', video_id
        else:
            print(f"\n✗ 錯誤: {error_msg[:200]}")
            return 'error', error_msg


def main():
    """Main processing function with safety features"""
    print("開始安全批量處理 YTlist.txt 中的影片")
    print("特點：更長的請求間隔（15秒）以避免 IP 封鎖")
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

    # Ask for processing mode
    print("請選擇處理模式：")
    print("1. 處理所有影片（包括已提取的）")
    print("2. 僅處理未提取的影片（推薦）")
    print("3. 處理前 5 個未提取的影片（測試模式）")

    mode = input("\n選擇 (1/2/3，預設為 2): ").strip() or "2"

    # Filter URLs based on mode
    if mode == "2":
        # Filter out already extracted
        filtered_urls = []
        for chapter, url in urls:
            video_id = get_video_id(url)
            if not check_if_info_extracted(chapter, video_id, output_dir):
                filtered_urls.append((chapter, url))
        urls = filtered_urls
        print(f"\n發現 {len(urls)} 個未處理的影片")
    elif mode == "3":
        # Only first 5 unextracted
        filtered_urls = []
        for chapter, url in urls:
            video_id = get_video_id(url)
            if not check_if_info_extracted(chapter, video_id, output_dir):
                filtered_urls.append((chapter, url))
                if len(filtered_urls) >= 5:
                    break
        urls = filtered_urls
        print(f"\n測試模式：將處理 {len(urls)} 個影片")

    if not urls:
        print("所有影片都已處理！")
        return

    # Confirm before starting
    estimated_time = len(urls) * 15 / 60  # minutes
    print(f"\n預計需要時間：約 {estimated_time:.1f} 分鐘")
    confirm = input("按 Enter 開始，或按 Ctrl+C 取消... ")

    # Process each video
    results = {
        'fully_processed': [],
        'info_exists': [],
        'info_saved': [],
        'ip_blocked': [],
        'error': []
    }

    for i, (chapter, url) in enumerate(urls, 1):
        print(f"\n進度：{i}/{len(urls)}")
        status, info = process_video(chapter, url, output_dir)
        results[status].append((chapter, info))

        # Stop if IP blocked
        if status == 'ip_blocked':
            print("\n\n因 IP 封鎖而停止處理")
            print("建議等待數小時後再繼續")
            break

    # Print summary
    print(f"\n\n{'='*60}")
    print("處理完成統計")
    print(f"{'='*60}")
    print(f"已有完整文檔: {len(results['fully_processed'])} 個")
    print(f"基本信息已存在: {len(results['info_exists'])} 個")
    print(f"新提取信息: {len(results['info_saved'])} 個")
    print(f"IP 封鎖: {len(results['ip_blocked'])} 個")
    print(f"其他錯誤: {len(results['error'])} 個")

    if results['info_saved']:
        print(f"\n新提取的影片:")
        for chapter, video_id in results['info_saved']:
            print(f"  第 {chapter} 章: {video_id}")

    if results['ip_blocked']:
        print(f"\nIP 封鎖的影片（建議稍後重試）:")
        for chapter, video_id in results['ip_blocked']:
            print(f"  第 {chapter} 章: {video_id}")

    if results['error']:
        print(f"\n其他錯誤:")
        for chapter, error in results['error'][:5]:  # Show first 5 errors
            print(f"  第 {chapter} 章: {error[:100]}")

    print(f"\n基本信息文件保存在: {output_dir}/_processing_*.txt")


if __name__ == "__main__":
    main()
