#!/usr/bin/env python3
"""批量提取所有剩余章节的转录"""

import json
import time
from youtube_transcript_api import YouTubeTranscriptApi
import re

# 章节11-41的URL
chapters = {
    11: "https://youtu.be/grMdPk1q3LM",
    12: "https://youtu.be/EvhGalHLUpY",
    13: "https://youtu.be/hPD1vfUaDl4",
    14: "https://youtu.be/Bd4e60Cf87I",
    15: "https://youtu.be/EpQEf3mTEa4",
    16: "https://youtu.be/EFVn-oBA2YQ",
    17: "https://youtu.be/uSPSjlugsLk",
    18: "https://youtu.be/vaWNlQLnbfA",
    19: "https://youtu.be/3yZlh66tRHM",
    20: "https://youtu.be/xNyagXpq6a4",
    21: "https://youtu.be/pltXmzzqBtM",
    22: "https://youtu.be/ZyuJDhTIM_M",
    23: "https://youtu.be/XorqH_pRkuA",
    24: "https://youtu.be/xliJaykqwkA",
    25: "https://youtu.be/siYtVTwCq6M",
    26: "https://youtu.be/y32W12rS9s8",
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

def get_transcript(video_id):
    """获取转录文本 - 使用API 1.2.3的fetch()方法"""
    try:
        api = YouTubeTranscriptApi()

        # 优先顺序：日语 > 韩语 > 中文 > 英语
        for lang_code in ['ja', 'ko', 'zh-Hans', 'zh-Hant', 'zh', 'en']:
            try:
                transcript = api.fetch(video_id, languages=[lang_code])
                return transcript, lang_code
            except:
                continue

        # 如果所有语言都失败，返回None
        return None, None

    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None, None

def format_timestamp(seconds):
    """格式化时间戳为 [HH:MM:SS]"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"

def main():
    successful = 0
    failed = []

    print(f"开始批量提取 {len(chapters)} 个章节的转录...")

    for chapter_num, url in chapters.items():
        print(f"\n处理章节 {chapter_num}...")

        video_id = extract_video_id(url)
        if not video_id:
            print(f"  ❌ 无法提取视频ID: {url}")
            failed.append(chapter_num)
            continue

        transcript_data, lang = get_transcript(video_id)
        if not transcript_data:
            print(f"  ❌ 无法获取转录")
            failed.append(chapter_num)
            continue

        # 转换FetchedTranscript为dict列表
        transcript_list = [
            {
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            }
            for snippet in transcript_data
        ]

        # 保存为JSON格式
        output_file = f"/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_transcript.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'video_id': video_id,
                'url': url,
                'chapter': chapter_num,
                'language': lang,
                'transcript': transcript_list
            }, f, ensure_ascii=False, indent=2)

        # 同时保存为可读文本格式
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

        # 延迟避免触发速率限制
        time.sleep(3)

    print(f"\n\n{'='*60}")
    print(f"批量提取完成!")
    print(f"成功: {successful}/{len(chapters)}")
    if failed:
        print(f"失败章节: {', '.join(map(str, failed))}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
