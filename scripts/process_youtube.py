#!/usr/bin/env python3
"""
YouTube Video to RAG Documentation Tool

This script processes YouTube videos and generates structured Markdown documentation
suitable for use as reference material in Claude Code projects.

Usage:
    python scripts/process_youtube.py "https://youtu.be/VIDEO_ID"
"""

import os
import sys
import re
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from anthropic import Anthropic


def get_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    # Handle various YouTube URL formats
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be/([0-9A-Za-z_-]{11})',
        r'embed/([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript(video_id: str, lang: str = 'ja') -> dict:
    """
    Fetch transcript from YouTube video.

    Returns a dict with:
    - video_id: str
    - language: str
    - transcript: list of {text, start, duration}
    """
    try:
        # Create API instance
        api = YouTubeTranscriptApi()

        # Try to get transcript in specified language
        # Priority: specified language, then fallback to common languages
        languages = [lang, 'ja', 'en', 'zh-Hans', 'zh-Hant']

        transcript = api.fetch(video_id, languages=languages, preserve_formatting=False)

        # Convert FetchedTranscript to list of dicts for compatibility
        data = [
            {
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            }
            for snippet in transcript
        ]

        return {
            'video_id': video_id,
            'language': transcript.language_code,
            'transcript': data
        }

    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def analyze_with_claude(transcript_data: dict, api_key: str) -> str:
    """
    Use Claude API to analyze transcript and generate structured Markdown.

    Args:
        transcript_data: Dict containing video_id, language, and transcript
        api_key: Anthropic API key

    Returns:
        Structured Markdown content
    """
    client = Anthropic(api_key=api_key)

    # Format transcript with timestamps for Claude
    formatted_transcript = "\n".join([
        f"[{format_timestamp(entry['start'])}] {entry['text']}"
        for entry in transcript_data['transcript']
    ])

    # Create analysis prompt
    prompt = f"""请分析以下 YouTube 视频转录内容，并生成一份结构化的 Markdown 文档。

视频 ID: {transcript_data['video_id']}
语言: {transcript_data['language']}

转录内容：
{formatted_transcript}

请按照以下格式生成完整的 Markdown 文档：

---
# 文档元数据（Frontmatter）
video_id: {transcript_data['video_id']}
video_url: https://youtu.be/{transcript_data['video_id']}
language: {transcript_data['language']}
date_processed: {datetime.now().strftime('%Y-%m-%d')}
tags: [自动提取相关标签]
---

# 影片概览

**标题**: [从内容推断标题]
**类型**: [类型：游戏、教程、访谈等]
**主要角色**: [列出主要角色]
**主要场景**: [场景1 → 场景2 → 场景3]

**故事梗概**:
[2-3句话总结整个内容]

---

# 章节时间轴

## 第X章：[章节标题] (开始时间 - 结束时间)
**场景**: [场景描述]
**关键事件**: [事件列表]

### 场景描述
[详细描述这一章节发生了什么]

### 对话记录

**[时间戳]** 角色名
> 对话内容（原文）
[中文翻译如果需要]

[重复多个章节...]

---

# 角色档案

## 角色名
- **所属**: [组织/团队]
- **职位/兵种**: [如果适用]
- **性格特征**: [描述]
- **关键行动**:
  - [行动1]
  - [行动2]
- **代表性台词**: "[引用]"

[重复多个角色...]

---

# 关键概念

## 概念名
[解释这个概念，包括在视频中的相关信息]

---

# 搜索关键词
[列出20-30个相关关键词，用逗号分隔]

---

重要要求：
1. 保持时间戳格式为 [MM:SS] 或 [HH:MM:SS]
2. 明确标注每句对话的说话者
3. 将内容合理分章节，每个章节应该是一个完整的场景或主题
4. 提取所有重要角色并创建档案
5. 识别关键概念并解释
6. 确保 Markdown 格式正确，便于阅读和 RAG 检索
7. 如果是日语内容，保留原文并提供中文翻译说明

请生成完整的文档："""

    # Call Claude API
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=16000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def extract_title_from_markdown(content: str) -> str:
    """
    Extract title from generated Markdown content.

    Args:
        content: Markdown content

    Returns:
        Extracted title or None
    """
    # Look for title in the format: **标题**: Title Here
    patterns = [
        r'\*\*标题\*\*:\s*(.+?)(?:\n|$)',
        r'\*\*標題\*\*:\s*(.+?)(?:\n|$)',
        r'\*\*Title\*\*:\s*(.+?)(?:\n|$)',
        r'title:\s*(.+?)(?:\n|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def sanitize_filename(title: str) -> str:
    """
    Sanitize title to create a valid filename.

    Args:
        title: Original title

    Returns:
        Sanitized filename
    """
    # Remove or replace invalid filename characters
    # Keep Chinese, Japanese, English letters, numbers, spaces, hyphens, underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)

    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Trim and limit length
    sanitized = sanitized.strip()[:100]

    return sanitized


def save_markdown(content: str, video_id: str, output_dir: str = "docs/videos") -> str:
    """
    Save generated Markdown to file.

    Args:
        content: Markdown content
        video_id: YouTube video ID
        output_dir: Output directory path

    Returns:
        Path to saved file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Try to extract title from content
    title = extract_title_from_markdown(content)

    if title:
        # Use title as filename
        safe_title = sanitize_filename(title)
        filename = f"{safe_title}.md"
    else:
        # Fallback to video ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{video_id}_{timestamp}.md"

    filepath = os.path.join(output_dir, filename)

    # If file exists, add video ID to make it unique
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{video_id}{ext}"
        filepath = os.path.join(output_dir, filename)

    # Write content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def main():
    """Main execution function."""
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python scripts/process_youtube.py <youtube_url>")
        print("\nExample:")
        print('  python scripts/process_youtube.py "https://youtu.be/D7-vCxdMT_0"')
        sys.exit(1)

    youtube_url = sys.argv[1]

    # Get API key from environment
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nPlease set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    try:
        print(f"Processing video: {youtube_url}")
        print()

        # Step 1: Extract video ID
        print("Step 1: Extracting video ID...")
        video_id = get_video_id(youtube_url)
        print(f"  Video ID: {video_id}")
        print()

        # Step 2: Fetch transcript
        print("Step 2: Fetching transcript...")
        transcript_data = get_transcript(video_id)
        print(f"  Language: {transcript_data['language']}")
        print(f"  Transcript entries: {len(transcript_data['transcript'])}")
        print()

        # Step 3: Analyze with Claude
        print("Step 3: Analyzing content with Claude API...")
        print("  (This may take 30-60 seconds...)")
        markdown_content = analyze_with_claude(transcript_data, api_key)
        print("  Analysis complete!")
        print()

        # Step 4: Save to file
        print("Step 4: Saving Markdown document...")
        output_path = save_markdown(markdown_content, video_id)
        print(f"  Saved to: {output_path}")
        print()

        print("✓ Success! Documentation generated successfully.")
        print(f"\nYou can now use this file as a reference in your Claude Code project.")
        print(f"File location: {output_path}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
