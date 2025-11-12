#!/usr/bin/env python3
"""
Generate full documentation from _processing_*.txt files
"""
import sys
import os
import time
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.process_youtube import get_video_id, get_transcript, format_timestamp


def read_processing_file(file_path):
    """Extract info from processing file"""
    info = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
    return info


def get_all_processing_files(output_dir='docs/videos'):
    """Get all processing files"""
    output_dir = Path(output_dir)
    files = sorted(output_dir.glob('_processing_*.txt'))
    return files


def generate_nikke_documentation(video_id, url, chapter_num, transcript_data, output_dir='docs/videos'):
    """
    Generate comprehensive NIKKE documentation
    Note: This is a placeholder - actual generation would require Claude/AI
    """
    # For now, just create a basic structure that can be filled in manually
    # or by Claude in a separate step

    transcript = transcript_data['transcript']
    last_entry = transcript[-1]
    total_seconds = last_entry['start'] + last_entry['duration']
    total_minutes = int(total_seconds // 60)
    total_secs = int(total_seconds % 60)

    # Extract title from first few lines
    title_text = []
    for entry in transcript[:20]:
        text = entry['text'].strip()
        if text and text != '[音楽]' and text != '[音楽]' and len(text) > 5:
            title_text.append(text)
            if len(title_text) >= 3:
                break

    suggested_title = f"NIKKE 第{chapter_num}章"

    # Create basic template
    content = f"""---
title: "{suggested_title}"
video_id: {video_id}
video_url: {url}
chapter: {chapter_num}
duration: "{total_minutes}:{total_secs:02d}"
language: {transcript_data['language']}
transcript_entries: {len(transcript)}
date_processed: "{time.strftime('%Y-%m-%d')}"
status: "needs_content_generation"
---

# {suggested_title}

## 影片資訊

- **影片 ID**: {video_id}
- **影片連結**: [{url}]({url})
- **章節**: 第 {chapter_num} 章
- **時長**: {total_minutes}:{total_secs:02d}
- **語言**: {transcript_data['language']}
- **字幕條目**: {len(transcript)} 條

## 狀態

**此文檔需要內容生成**

完整的字幕已提取（{len(transcript)} 條），但詳細的故事分析、角色介紹、主題探討等內容需要進一步生成。

## 完整字幕

"""

    # Add full transcript
    for i, entry in enumerate(transcript, 1):
        timestamp = format_timestamp(entry['start'])
        content += f"[{timestamp}] {entry['text']}\n"

    # Save to file
    output_path = Path(output_dir) / f"NIKKE_第{chapter_num}章_{video_id}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def main():
    """Main function"""
    print("開始從處理文件生成完整文檔\n")

    output_dir = 'docs/videos'
    processing_files = get_all_processing_files(output_dir)

    print(f"找到 {len(processing_files)} 個處理文件\n")

    results = {
        'success': [],
        'ip_blocked': [],
        'error': []
    }

    for i, file_path in enumerate(processing_files, 1):
        # Extract chapter from filename
        match = re.search(r'_processing_(\d+)_([a-zA-Z0-9_-]+)\.txt', file_path.name)
        if not match:
            continue

        chapter = match.group(1)
        video_id = match.group(2)

        print(f"\n[{i}/{len(processing_files)}] 處理第 {chapter} 章 (ID: {video_id})")

        try:
            # Read processing file
            info = read_processing_file(file_path)
            url = info.get('URL', f'https://youtu.be/{video_id}')

            # Try to get full transcript
            print(f"  嘗試獲取完整字幕...")
            transcript_data = get_transcript(video_id)

            print(f"  ✓ 成功獲取 {len(transcript_data['transcript'])} 條字幕")

            # Generate documentation
            output_path = generate_nikke_documentation(
                video_id, url, chapter, transcript_data, output_dir
            )

            print(f"  ✓ 文檔已生成: {output_path.name}")
            results['success'].append((chapter, video_id, output_path.name))

            # Delay to avoid IP block
            if i < len(processing_files):
                print(f"  等待 10 秒...")
                time.sleep(10)

        except Exception as e:
            error_msg = str(e)
            if "blocking requests from your IP" in error_msg:
                print(f"  ✗ IP 封鎖")
                results['ip_blocked'].append((chapter, video_id))
                print(f"\n因 IP 封鎖而停止處理")
                print(f"已處理: {len(results['success'])} 個")
                print(f"剩餘: {len(processing_files) - i} 個")
                break
            else:
                print(f"  ✗ 錯誤: {error_msg[:100]}")
                results['error'].append((chapter, video_id, error_msg))

    # Print summary
    print(f"\n\n{'='*60}")
    print("處理結果統計")
    print(f"{'='*60}")
    print(f"成功生成: {len(results['success'])} 個")
    print(f"IP 封鎖: {len(results['ip_blocked'])} 個")
    print(f"其他錯誤: {len(results['error'])} 個")

    if results['success']:
        print(f"\n✓ 成功生成的文檔:")
        for chapter, video_id, filename in results['success']:
            print(f"  第 {chapter} 章: {filename}")

    if results['ip_blocked']:
        print(f"\n✗ IP 封鎖無法處理:")
        for chapter, video_id in results['ip_blocked']:
            print(f"  第 {chapter} 章 (ID: {video_id})")

    if results['error']:
        print(f"\n✗ 其他錯誤:")
        for chapter, video_id, error in results['error'][:5]:
            print(f"  第 {chapter} 章: {error[:80]}")

    print(f"\n生成的文檔保存在: {output_dir}/")
    print(f"注意: 生成的文檔包含完整字幕，但需要進一步的內容分析")


if __name__ == "__main__":
    main()
