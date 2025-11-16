#!/usr/bin/env python3
"""批量生成所有章节的RAG文档"""

import json
import os
import anthropic
from pathlib import Path

# 设置API
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# RAG生成系统提示词
SYSTEM_PROMPT = """你是NIKKE游戏故事的专业分析师。你的任务是将日语游戏转录分析并生成结构化的中文RAG（Retrieval-Augmented Generation）文档。

**输出格式要求**:

1. **YAML Frontmatter** (包含video_id, video_url, chapter, chapter_name, language, date_processed, tags, timeline等)
2. **影片概览** (标题、类型、主要角色、主要场景、时间跨度、故事梗概)
3. **章节时间轴** (按3-8分钟分段，每段包含: 场景、关键事件、核心剧情、关键对话)
4. **角色档案** (10-20个角色，包含: 角色名、定位/职业、性格特征、关键台词、关系网络)
5. **核心概念** (世界观术语、技术概念、组织机构等)
6. **主题分析** (5-6个主要主题)
7. **未解之谜** (5-7个剧情悬念)
8. **搜索关键词** (60-100个RAG优化关键词)

**分析要求**:
- 保留日语原文关键对话（附中文翻译）
- 深入分析角色心理和动机
- 识别伏笔和剧情线索
- 标注时间戳关键场景
- 使用中文输出，但保留专有名词的日语或英语原文

参考已完成章节的格式和风格。"""

def load_transcript(chapter_num):
    """加载转录文件"""
    json_file = f"/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_transcript.json"
    txt_file = f"/mnt/f/nikkerag/temp/Chapter_{chapter_num:02d}_transcript.txt"

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(txt_file, 'r', encoding='utf-8') as f:
            transcript_text = f.read()

        return data, transcript_text
    except Exception as e:
        print(f"  ❌ 加载失败: {e}")
        return None, None

def generate_rag_document(chapter_num, metadata, transcript_text):
    """使用Claude API生成RAG文档"""
    try:
        user_prompt = f"""请分析NIKKE第{chapter_num:02d}章的游戏转录，生成完整的RAG文档。

**章节元数据**:
- 视频ID: {metadata['video_id']}
- URL: {metadata['url']}
- 章节: {chapter_num}
- 语言: {metadata['language']}
- 来源: {metadata.get('source', 'dual-mcp')}

**完整转录**:
```
{transcript_text[:30000]}
```

请按照系统提示中的格式要求，生成完整、详细的RAG分析文档。"""

        print(f"    调用Claude API...")
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        rag_content = message.content[0].text
        return rag_content

    except Exception as e:
        print(f"    ❌ API调用失败: {e}")
        return None

def save_documents(chapter_num, rag_content, transcript_text):
    """保存RAG文档和原文记录"""
    # 从RAG内容提取章节名
    chapter_name = f"第{chapter_num:02d}章"
    if "chapter_name:" in rag_content:
        import re
        match = re.search(r'chapter_name:\s*(.+)', rag_content)
        if match:
            chapter_name = match.group(1).strip()

    # 保存RAG文档
    rag_file = f"/mnt/f/nikkerag/docs/videos/NIKKE 第{chapter_num:02d}章 {chapter_name} - RAG文档.md"
    with open(rag_file, 'w', encoding='utf-8') as f:
        f.write(rag_content)

    # 保存原文记录
    raw_file = f"/mnt/f/nikkerag/docs/videos/NIKKE 第{chapter_num:02d}章 {chapter_name} - 原文记录.md"
    with open(raw_file, 'w', encoding='utf-8') as f:
        f.write(f"# NIKKE 第{chapter_num:02d}章 {chapter_name} - 原文记录\n\n")
        f.write(transcript_text)

    return rag_file, raw_file

# 主处理循环
chapters = range(11, 42)  # 11-41
successful = 0
failed = []

print(f"开始批量生成 {len(list(chapters))} 个章节的RAG文档...")
print("="*60)

for chapter_num in chapters:
    print(f"\n第{chapter_num:02d}章:")

    # 加载转录
    print(f"  [1/3] 加载转录...")
    metadata, transcript_text = load_transcript(chapter_num)
    if not metadata or not transcript_text:
        failed.append(chapter_num)
        continue

    # 生成RAG文档
    print(f"  [2/3] 生成RAG文档 (约30-60秒)...")
    rag_content = generate_rag_document(chapter_num, metadata, transcript_text)
    if not rag_content:
        failed.append(chapter_num)
        continue

    # 保存文档
    print(f"  [3/3] 保存文档...")
    try:
        rag_file, raw_file = save_documents(chapter_num, rag_content, transcript_text)
        print(f"  ✅ 成功生成:")
        print(f"      - {Path(rag_file).name}")
        print(f"      - {Path(raw_file).name}")
        successful += 1
    except Exception as e:
        print(f"  ❌ 保存失败: {e}")
        failed.append(chapter_num)

print(f"\n\n{'='*60}")
print(f"RAG文档生成完成!")
print(f"成功: {successful}/{len(list(chapters))}")
if failed:
    print(f"失败章节: {', '.join(map(str, failed))}")
print(f"{'='*60}")
