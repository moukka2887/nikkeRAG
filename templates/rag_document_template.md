# RAG Document Template

Use this template for generating structured RAG documentation from NIKKE game story transcripts.

---

```markdown
---
title: NIKKE 第XX章 [Chapter Name] - RAG文档
source: [Video filename or YouTube URL]
video_id: [YouTube video ID, e.g., Bd4e60Cf87I]
chapter: [Chapter number, e.g., 14]
chapter_name: [Chapter name in Chinese, e.g., 旅行]
language: [Source language: ja, ko, zh, en]
date_processed: [YYYY-MM-DD]
content_type: story_event
related_docs:
  - [Path to related timeline document]
  - [Path to related character profiles]
confidence: high
validation_status: pending
tags:
  - [Tag 1, e.g., main_story]
  - [Tag 2, e.g., character_development]
  - [Tag 3, e.g., world_building]
---

# NIKKE 第XX章 [Chapter Name] - RAG文档

## 影片概览

**标题**: [Video title in Chinese]
**类型**: [Content type: 主线剧情 | 活动剧情 | 角色剧情]
**时长**: [HH:MM:SS]
**语言**: [Source language with full name]

**主要角色**:
- [Character 1] ([日文名], [English name])
- [Character 2]
- [Character 3]

**主要场景**:
- [Location 1] - [Brief description]
- [Location 2] - [Brief description]

**时间跨度**: [Time period covered, e.g., 一天 | 几个小时 | 数周]

**故事梗概** (200-500 字):
[Comprehensive summary of the chapter's story. Include:
- Main conflict or objective
- Key events in chronological order
- Character motivations and relationships
- Emotional tone and themes
- Resolution or cliffhanger]

---

## 章节时间轴

按照故事进展顺序，将章节分为 3-8 个主要段落。每段 3-8 分钟。

### 段落 1: [Segment Title] ([Timestamp Range, e.g., 00:00 - 05:23])

**场景**: [Location/setting]

**关键事件**:
- [Event 1 with brief description]
- [Event 2 with brief description]
- [Event 3 with brief description]

**核心剧情**:
[Detailed narrative description of what happens in this segment. Include character actions, dialogue themes, and plot progression. 100-200 words.]

**关键对话**:
- `[00:02:15]` **[Character]**: "[Dialogue in original language]" ([Chinese translation])
- `[00:03:42]` **[Character]**: "[Dialogue]" ([Translation])

---

### 段落 2: [Segment Title] ([Timestamp Range])

**场景**: [Location/setting]

**关键事件**:
- [Event 1]
- [Event 2]

**核心剧情**:
[Narrative description]

**关键对话**:
- `[00:07:30]` **[Character]**: "[Dialogue]" ([Translation])

---

[Continue for 3-8 segments total]

---

## 角色档案

### 主要角色 (10-20 个)

#### [Character Name 1] ([日文名], [English])

**定位/职业**: [Role, e.g., Nikke战士 | 指挥官 | 科学家]

**性格特征**:
- [Trait 1: e.g., 冷静沉着]
- [Trait 2: e.g., 责任心强]
- [Trait 3: e.g., 保护欲强]

**在本章中的表现**:
[How character behaves, develops, or is revealed in this chapter. Include personality traits, motivations, conflicts. 50-100 words.]

**关键台词**:
- "[Memorable quote 1 in original]" ([Translation]) - `[Timestamp]`
- "[Memorable quote 2]" ([Translation]) - `[Timestamp]`

**关系网络**:
- **与 [Character 2]**: [Relationship type and quality, e.g., 战友关系，互相信任]
- **与 [Character 3]**: [Relationship description]

---

#### [Character Name 2]

[Same structure as above]

---

[Continue for 10-20 characters]

---

## 核心概念

### 世界观术语

#### [Term 1, e.g., Rapture (ラプチャー)]
**定义**: [What it is]
**在本章中的体现**: [How it appears or is relevant in this chapter]

#### [Term 2, e.g., Ark (アーク)]
**定义**: [What it is]
**在本章中的体现**: [Relevance to chapter]

---

### 技术概念

#### [Technical Term 1]
**说明**: [Explanation]
**关键细节**: [Important details revealed in this chapter]

---

### 组织机构

#### [Organization 1, e.g., Tetra Line]
**性质**: [What kind of organization]
**成员**: [Key members mentioned]
**在本章中的角色**: [What role they play]

---

## 主题分析

### 主题 1: [Theme, e.g., 人性与机械]
[Analysis of how this theme is explored in the chapter. Include specific examples from dialogue or events. 100-150 words.]

### 主题 2: [Theme, e.g., 牺牲与责任]
[Theme analysis]

### 主题 3: [Theme]
[Theme analysis]

[Continue for 5-6 major themes]

---

## 未解之谜

1. **[Mystery 1]**: [Description of unanswered question or plot thread]
2. **[Mystery 2]**: [Description]
3. **[Mystery 3]**: [Description]
4. **[Mystery 4]**: [Description]
5. **[Mystery 5]**: [Description]

[Include 5-7 mysteries or unresolved plot points]

---

## 叙事手法

### 视角
[Narrative perspective used: 第一人称 | 第三人称 | 多视角]

### 节奏
[Pacing: 快节奏 | 缓慢推进 | 张弛有度]

### 情感基调
[Emotional tone: 紧张悬疑 | 温情治愈 | 激烈战斗 | 沉重压抑]

### 特殊手法
- [Technique 1, e.g., 闪回 | 伏笔 | 对比 | 象征]
- [Technique 2]

---

## 情感高潮

### 高潮时刻 1: [Title] (`[Timestamp]`)
**场景**: [Location and participants]
**描述**: [What makes this moment emotionally powerful]
**影响**: [Impact on story and characters]

### 高潮时刻 2: [Title] (`[Timestamp]`)
[Same structure]

[Include 2-4 emotional peaks]

---

## 与其他章节的联系

### 前情提要
- 第XX章: [Connection to previous chapter]
- 第XX章: [Another relevant connection]

### 后续影响
- 预计影响第XX章: [How this chapter sets up future events]
- 伏笔: [Foreshadowing for future chapters]

---

## 搜索关键词

[60-100 keywords optimized for RAG retrieval, comma-separated]

**角色名**: [Character 1], [Character 2], [Character 3], ...

**地点**: [Location 1], [Location 2], ...

**组织**: [Organization 1], [Organization 2], ...

**术语**: [Term 1], [Term 2], [Term 3], ...

**事件**: [Event 1], [Event 2], [Event 3], ...

**主题**: [Theme 1], [Theme 2], [Theme 3], ...

**情感**: [Emotion 1], [Emotion 2], ...

**物品**: [Item 1], [Item 2], ...

**技术**: [Tech 1], [Tech 2], ...

---

## 备注

[Any additional notes, corrections, or observations that don't fit above categories]

---

**生成信息**:
- 生成时间: [YYYY-MM-DD HH:MM:SS]
- 转录来源: [Path to transcript file]
- 生成工具: rag-doc-generator agent v[version]
- 质量评分: [自动评估分数, if available]
```

---

## Template Usage Guidelines

### Required Sections (Must Include)
- YAML Frontmatter with all required fields
- 影片概览 (Story Overview)
- 章节时间轴 (Timeline with 3-8 segments)
- 角色档案 (Character Profiles, 10-20 characters)
- 核心概念 (Core Concepts)
- 搜索关键词 (Search Keywords, 60-100 keywords)

### Optional Sections (Include if Relevant)
- 主题分析 (Theme Analysis)
- 未解之谜 (Mysteries)
- 叙事手法 (Narrative Techniques)
- 情感高潮 (Emotional Peaks)
- 与其他章节的联系 (Connections)
- 备注 (Notes)

### Quality Checks
- [ ] YAML frontmatter is valid
- [ ] All required fields populated
- [ ] Chapter number matches filename
- [ ] Timestamps in chronological order
- [ ] 60-100 search keywords included
- [ ] Character names consistent with NIKKE_TERMINOLOGY.md
- [ ] No placeholder text remaining (no [TODO], [需要补充])
- [ ] Chinese translation quality verified
- [ ] Markdown syntax valid

### Common Pitfalls to Avoid
- ❌ Generic placeholders left in final document
- ❌ Character names inconsistent with standard terminology
- ❌ Insufficient detail in timeline segments (< 100 words)
- ❌ Too few or too many character profiles (aim for 10-20)
- ❌ Missing timestamps for key dialogue
- ❌ Keywords insufficient for RAG optimization (< 60)
- ❌ YAML frontmatter syntax errors

### Customization Notes
- Adjust segment count (3-8) based on chapter length
- Character profile count (10-20) flexible based on chapter cast
- Theme analysis depth varies by chapter complexity
- Keyword count (60-100) should cover all major elements

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
