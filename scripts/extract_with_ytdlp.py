#!/usr/bin/env python3
"""使用yt-dlp提取失败的章节转录"""

import subprocess
import json
import re
import os

# 失败的章节
failed_chapters = {
    25: "https://youtu.be/siYtVTwCq6M",
    27: "https://youtu.be/AJgeaw4EyNI",
    28: "https://youtu.be/GO6Tai5YPag",
    29: "https://youtu.be/4Us6rnpY4OE",
    30: "https://youtu.be/BsNevxS1ubM",
    31: "https://youtu.be/yPdi283EIk4",
    32: "https://youtu.be/K1G6_6Qf6Io",
    33: "https://youtu.be/DylyZwx2fhA",
    34: "https://youtu.be/CQBTyf9JmOo",
    35: "https://youtu.be/hXuGXN0BU6Q",
    36: "https://youtu.be/706pbFRmG-U",
    37: "https://youtu.be/a6TnywuZGHk",
    38: "https://youtu.be/QlRHtXiPc1I",
    39: "https://youtu.be/n1YLOO7pJJU",
    40: "https://youtu.be/NMPi5fzC4IE",
    41: "https://youtu.be/WYnXa9Zbsdk",
}

def extract_video_id(url):
    """从URL提取视频ID"""
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be/([0-9A-Za-z_-]{11})',
        r'embed/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript_ytdlp(video_id, url):
    """使用yt-dlp获取字幕"""
    try:
        # 使用yt-dlp获取字幕列表
        cmd_list = ['yt-dlp', '--list-subs', '--skip-download', url]
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        print(f"  可用字幕: {result.stdout[:200]}...")

        # 尝试下载字幕 (优先: ja > ko > en)
        for lang in ['ja', 'ko', 'en', 'zh-Hans', 'zh']:
            output_template = f'/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_%(ext)s'
            cmd_download = [
                'yt-dlp',
                '--write-auto-sub',
                '--sub-lang', lang,
                '--skip-download',
                '--output', output_template,
                url
            ]

            result = subprocess.run(cmd_download, capture_output=True, text=True)

            # 检查是否成功下载
            for ext in ['vtt', 'srt', 'json3']:
                subtitle_file = f'/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_{lang}.{ext}'
                if os.path.exists(subtitle_file):
                    print(f"  ✅ 成功下载 {lang} 字幕 ({ext})")
                    return subtitle_file, lang

        return None, None

    except Exception as e:
        print(f"  yt-dlp错误: {e}")
        return None, None

def parse_vtt_to_transcript(vtt_file):
    """解析VTT文件为转录格式"""
    transcript = []
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 跳过WEBVTT头和空行
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:') or not line:
            i += 1
            continue

        # 时间戳行格式: 00:00:00.750 --> 00:00:09.560
        if '-->' in line:
            timestamp_match = re.match(r'(\d{2}):(\d{2}):(\d{2}\.\d{3})', line)
            if timestamp_match:
                hours = int(timestamp_match.group(1))
                minutes = int(timestamp_match.group(2))
                seconds = float(timestamp_match.group(3))
                start_time = hours * 3600 + minutes * 60 + seconds

                # 下一行是文本
                i += 1
                if i < len(lines):
                    text = lines[i].strip()
                    if text:
                        transcript.append({
                            'text': text,
                            'start': start_time,
                            'duration': 3.0  # 默认持续时间
                        })
        i += 1

    return transcript

def format_timestamp(seconds):
    """格式化时间戳为 [HH:MM:SS]"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"

successful = 0
still_failed = []

print(f"使用yt-dlp提取 {len(failed_chapters)} 个失败的章节...")

for chapter_num, url in failed_chapters.items():
    print(f"\n处理章节 {chapter_num}...")

    video_id = extract_video_id(url)
    if not video_id:
        print(f"  ❌ 无法提取视频ID")
        still_failed.append(chapter_num)
        continue

    subtitle_file, lang = get_transcript_ytdlp(video_id, url)
    if not subtitle_file:
        print(f"  ❌ 无法下载字幕")
        still_failed.append(chapter_num)
        continue

    # 解析字幕文件
    transcript_list = parse_vtt_to_transcript(subtitle_file)

    if not transcript_list:
        print(f"  ❌ 无法解析字幕")
        still_failed.append(chapter_num)
        continue

    # 保存为JSON
    json_file = f"/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_transcript.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'video_id': video_id,
            'url': url,
            'chapter': chapter_num,
            'language': lang,
            'transcript': transcript_list
        }, f, ensure_ascii=False, indent=2)

    # 保存为可读文本
    text_file = f"/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_transcript.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(f"# NIKKE 第{chapter_num:02d}章 转录\n")
        f.write(f"视频ID: {video_id}\n")
        f.write(f"URL: {url}\n")
        f.write(f"语言: {lang}\n\n")

        for entry in transcript_list:
            timestamp = format_timestamp(entry['start'])
            text = entry['text']
            f.write(f"{timestamp} {text}\n")

    print(f"  ✅ 成功保存 (语言: {lang}, {len(transcript_list)} 条)")
    successful += 1

print(f"\n\n{'='*60}")
print(f"yt-dlp提取完成!")
print(f"成功: {successful}/{len(failed_chapters)}")
if still_failed:
    print(f"仍然失败: {', '.join(map(str, still_failed))}")
print(f"{'='*60}")
