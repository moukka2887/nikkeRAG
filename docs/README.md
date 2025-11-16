# NIKKE RAG 文档系统

这是 NIKKE: Goddess of Victory 游戏剧情的 RAG (Retrieval-Augmented Generation) 文档系统。

## 📁 目录结构

### methodology/ - 方法论文档
RAG 生成的核心方法论和改进提案

- **RAG_GENERATION_METHODOLOGY.md** - RAG 文档生成的完整方法论（v3.0）
- **improvement_proposals.md** - 基于 GraphRAG 论文的改进方案
- **v3.0_UPGRADE_SUMMARY.md** - v3.0 版本升级总结

### timeline/ - 时间线分析
NIKKE 主线故事的时间线梳理和分析

- **NIKKE_完整故事时间线.md** - 完整故事时间线（受保护文件）
- **MAIN_STORY_TIME_FLOW_ANALYSIS.md** - 主线剧情时间流分析
- **MAIN_STORY_TIME_ESTIMATION_BY_EVENTS.md** - 基于事件的时间估算
- **TIMELINE_TIME_MARKERS_ANALYSIS.md** - 时间标记分析
- **TIMELINE_CONFLICTS_GODDESS_FALL.md** - 女神降临篇时间线冲突

### validation/ - 验证和质量控制
字幕校准和质量验证相关文档

- **SUBTITLE_VALIDATION_PLAN.md** - 字幕验证计划
- **SUBTITLE_SCAN_REPORT_20251111.md** - 字幕扫描报告
- **VALIDATION_CHECKLIST.md** - 验证检查清单
- **VALIDATION_REPORT_GODDESS_FALL_20251115.md** - 女神降临验证报告
- **VERIFICATION_NOTES.md** - 验证笔记
- **YOUTUBE_SUBTITLE_CORRECTIONS.md** - YouTube 字幕已知错误模式（18 个）

### calibration_reports/ - 校准报告
字幕错误校准的详细报告（16 个文件）

包含各章节和活动的字幕校准报告，记录自动纠正的错误和需要人工审核的案例。

### characters/ - 角色档案
角色的详细档案和性格分析（13 个文件）

- Rapi, Anis, Neon, Commander, Crown, Dorothy, Isabel 等主要角色
- 按章节整理的角色群像档案

### videos/ - 视频 RAG 文档
YouTube 视频转录和 RAG 文档（109 个文件）

**主线故事**：第 1-42 章（部分）
- 每章包含 RAG 文档和原文记录两个文件

**周年活动**：
- 0.5 周年：永恆樂園的回憶 OVER ZONE
- 1.5 周年：LAST KINGDOM (Part I & II)
- 2.5 周年：小美人魚 (Part I & II)

**特殊活动**：
- 女神降临系列
- Old Tales 系列

### worldbuilding/ - 世界观设定
NIKKE 世界的设定和背景资料

### references/ - 参考文献
理论和技术参考文献

- **graph_RAG.pdf** - Microsoft Research 的 GraphRAG 论文

## 🔧 核心方法论

本系统采用 **v3.0 RAG 生成方法论**，整合以下改进：

1. **说话人推断系统** - 从视频标题提取主角 + LLM 分析对话
2. **语义分块优化** - 基于场景标记的智能分段
3. **增强 RAG 检索** - 结构化元数据和独立角色索引
4. **自动质量验证** - 标题-角色一致性检查

## 📊 文件统计

- RAG 文档和原文记录：109 个
- 角色档案：13 个
- 校准报告：16 个
- 时间线分析：5 个
- 验证文档：6 个
- 方法论文档：3 个

## 🚀 快速导航

**查看 RAG 生成方法**：
→ `methodology/RAG_GENERATION_METHODOLOGY.md`

**查看已知字幕错误**：
→ `validation/YOUTUBE_SUBTITLE_CORRECTIONS.md`

**查看完整时间线**：
→ `timeline/NIKKE_完整故事时间线.md`

**查看最新改进提案**：
→ `methodology/improvement_proposals.md`

## ⚠️ 受保护文件

以下文件标记为受保护，不应通过自动化流程修改：
- `timeline/NIKKE_完整故事时间线.md`
- `timeline/MAIN_STORY_TIME_FLOW_ANALYSIS.md`

如发现冲突，请创建单独的冲突报告而非直接修改。

## 📝 版本历史

- **v3.0** (2025-11-16): 整合 GraphRAG 改进方案，添加说话人推断
- **v2.0** (2025-11-15): 引入字幕校准和质量验证
- **v1.0** (2025-10-30): 初始 RAG 文档系统

---

生成时间：2025-11-16
系统版本：v3.0
