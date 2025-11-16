# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a specialized RAG (Retrieval-Augmented Generation) documentation system for NIKKE: Goddess of Victory game story content. The system processes YouTube video gameplay recordings (Japanese/Korean) with automated subtitle extraction, applies systematic error corrections, and generates structured documentation optimized for AI retrieval.

**Primary Use Case**: Converting 42+ chapters of NIKKE main story gameplay videos into searchable, structured Markdown documentation for AI assistant reference.

## Core Architecture

### Multi-Agent Workflow Pipeline

The system uses a coordinated multi-agent pipeline managed by Claude Code:

```
1. video-transcription-mcp → Extracts subtitles from YouTube videos
2. nikke-translation-calibrator → Corrects systematic subtitle errors
3. rag-doc-generator → Creates structured RAG documents
4. story-consistency-validator → Cross-validates information integrity
```

**Agent coordination**: Each agent operates autonomously with state persistence and handoff protocols. See `.claude/agents/*.md` for detailed specifications.

### Critical Files and Their Roles

**Terminology Standards** (Read-only references):
- `NIKKE_TERMINOLOGY.md` - Canonical character names, locations, technical terms (50+ entries)
- `docs/validation/YOUTUBE_SUBTITLE_CORRECTIONS.md` - Known subtitle error patterns (18 documented patterns)

**Protected Files** (Never modify programmatically):
- `docs/timeline/NIKKE_完整故事时间线.md` - Master timeline (immutable)
- `docs/timeline/MAIN_STORY_TIME_FLOW_ANALYSIS.md` - Timeline analysis (immutable)
- Any file marked with `<!-- PROTECTED: DO NOT MODIFY -->`

**Templates**:
- `templates/rag_document_template.md` - Structure for RAG documents

**Output Locations**:
- `docs/videos/` - RAG documents and original transcripts
- `docs/characters/` - Character profile files
- `docs/worldbuilding/` - Worldbuilding documentation
- `docs/calibration_reports/` - Subtitle error correction reports
- `temp/` - Intermediate processing files and agent state

**Development References**:
- `dev-references/` - Development reference materials (videos, AI prompts, NIKKE wiki PDF)
- `dev-references/dlYTvideo/` - Downloaded YouTube videos (ignored by git, 1GB+)

## Development Commands

### MCP Server Configuration

This project requires MCP servers for YouTube video processing. Configuration in `.claude/mcp.json`:

```bash
# YouTube transcript extraction (requires uvx)
uvx mcp-youtube-transcript

# Alternative: yt-dlp server (more reliable for some regions)
npx -y @kevinwatt/yt-dlp-mcp
```

### Python Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - anthropic>=0.18.0
# - youtube-transcript-api>=0.6.0
# - requests>=2.31.0

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Available Processing Scripts

```bash
# Test YouTube access and MCP connectivity
python scripts/test_youtube_access.py

# Batch extract transcripts from multiple videos
python scripts/batch_extract_all.py

# Batch generate RAG documents from existing transcripts
python scripts/batch_generate_rag.py

# Convert VTT subtitle files to JSON format
python scripts/convert_vtt_to_json.py "input.vtt"

# Extract video with yt-dlp fallback
python scripts/extract_with_ytdlp.py "VIDEO_URL"

# Batch process with Whisper ASR (for videos without subtitles)
python scripts/whisper_asr_batch.py
```

## Key Design Patterns

### v3.0 RAG Methodology (Current Standard)

The system uses **v3.0 RAG Generation Methodology** (see `docs/methodology/RAG_GENERATION_METHODOLOGY.md`):

**Core improvements over v2.0**:
1. **Speaker Inference System** - Extracts protagonist from video titles + first-person dialogue analysis
2. **Semantic Chunking** - Uses scene markers ([音楽], dialogue gaps) instead of time-based splitting
3. **Three-Layer Architecture** - Global narrative + detailed timeline + entity index
4. **Automatic Quality Validation** - Title-character consistency checks, time coverage validation

**Key problem solved**: In 2.5 anniversary videos, Siren (protagonist) speaks from minute 5 but name mentioned only once at end. v2.0 incorrectly identified Uni (mentioned 78 times) as protagonist. v3.0 correctly identifies Siren through title analysis + first-person pronoun detection.

### Information Prioritization Protocol

**NEW content always supersedes LEGACY** when conflicts occur:

```markdown
## Current Canonical Information (as of 2025-11-16, Ch14)
**Personality**: [New information from latest source]

### [LEGACY] Previous Characterizations
**Personality** (2025-10-15, Ch11): [Old information]
- Superseded by Ch14 character development
```

All updates must include:
- Source chapter/date
- Reason for superseding
- [LEGACY] annotation for historical data

### Protected File Integrity

**Never directly modify protected timeline files**. When conflicts detected:

1. Create separate conflict report: `docs/TIMELINE_CONFLICTS_Ch{N}.md`
2. Document both versions with sources
3. Recommend resolution with evidence
4. User manually updates protected files after verification

### Systematic Error Correction

YouTube subtitle errors follow patterns documented in `docs/validation/YOUTUBE_SUBTITLE_CORRECTIONS.md`:

**Critical auto-corrections** (95%+ confidence):
- `福祉霊感` → `指揮官` (Commander mojibake, 18+ instances per chapter)
- `ラビ` → `ラピ` (Rapi character name, 5-12 per chapter)
- `アニース` → `アニス` (Anis character name)

**Context-dependent corrections** (requires review):
- `マリア` vs `マリアン` (Two different characters - operations coordinator vs special character)
- `副司令官` vs `指揮官` (Vice Commander vs Commander - depends on addressee)

### Agent State Management

Batch operations (3+ chapters) persist state to enable interruption recovery:

```json
{
  "session_id": "20251116_023045",
  "agent": "rag-doc-generator",
  "current_state": "EXECUTING",
  "progress": {"completed_items": 4, "total_items": 10},
  "results": [...]
}
```

State files: `temp/{agent}_state_{session_id}.json`

## Agent Invocation Guidelines

### When Processing New Video Content

**Sequential workflow** (do not skip steps):

```
1. User provides YouTube URL
2. Invoke video-transcription-mcp agent
   - Extracts subtitle with timestamps
   - Validates encoding (UTF-8)
   - Saves to temp/Chapter_{N}_transcript.json

3. Invoke nikke-translation-calibrator agent
   - Applies YOUTUBE_SUBTITLE_CORRECTIONS.md patterns
   - Flags ambiguous cases
   - Generates correction report

4. Invoke rag-doc-generator agent (use v3.0 methodology)
   - Follows templates/rag_document_template.md
   - Extracts 10-20 character profiles
   - Generates 60-100 search keywords
   - Creates 3-8 timeline segments
   - Applies speaker inference from video title

5. Invoke story-consistency-validator agent
   - Cross-references with existing docs
   - Detects gaps and conflicts
   - Updates character profiles
   - Preserves protected files
```

### Agent Communication Standards

All agents follow concise reporting (< 5 lines):

```markdown
✅ Good:
Calibrated Chapter 14 transcript.
- 18 critical errors auto-corrected
- 3 cases flagged for review
- Error rate: 6.4%
- Report: docs/calibration_reports/Ch14_correction_report.md

❌ Too verbose:
I've completed the calibration process for Chapter 14. During this process, I identified and automatically corrected 18 critical errors...
```

## File Naming Conventions

```bash
# RAG documents (Chinese chapter names)
docs/videos/NIKKE 第{N}章 {ChapterName} - RAG文档.md
docs/videos/NIKKE 第{N}章 {ChapterName} - 原文記錄.md

# Anniversary events
docs/videos/NIKKE {N}周年 Part {I|II} - RAG文档.md

# Character profiles (English canonical names)
docs/characters/{CharacterName}_profile.md
# Examples: Rapi_profile.md, Scarlet_profile.md

# Worldbuilding (lowercase with underscores)
docs/worldbuilding/{topic}.md
# Examples: ark_locations.md, three_manufacturers.md

# Conflict reports
docs/TIMELINE_CONFLICTS_Ch{N}.md
docs/GAP_ANALYSIS_Ch{N}.md

# Agent state files
temp/{agent}_state_{session_id}.json

# Correction reports
docs/calibration_reports/Ch{N}_correction_report.md
```

## Quality Standards

### RAG Document Requirements (v3.0)

Every generated RAG document must pass:

- [ ] 10-20 character profiles with personality traits
- [ ] 3-8 timeline segments (semantic chunking based on scenes)
- [ ] 60-100 search keywords across 9 categories
- [ ] Valid YAML frontmatter with methodology_version: v3.0.0
- [ ] No placeholder text ([TODO], [需要补充])
- [ ] Timestamps in HH:MM:SS format, chronological
- [ ] File size > 50KB (comprehensive content indicator)
- [ ] All character names match NIKKE_TERMINOLOGY.md
- [ ] Speaker inference validation (title-character consistency check)
- [ ] Time coverage > 95% (for protagonist identification)

### Error Correction Validation

Calibration operations must:

- [ ] Create backup before any modifications
- [ ] Log all auto-corrections with line numbers
- [ ] Flag context-dependent cases (< 95% confidence)
- [ ] Maintain error rate tracking (typical 4-8%)
- [ ] Generate comprehensive correction report

### Story Consistency Checks

Validation operations must:

- [ ] Prioritize NEW information over LEGACY
- [ ] Preserve legacy data with [LEGACY] annotations
- [ ] Never modify protected timeline files
- [ ] Create conflict reports for timeline discrepancies
- [ ] Document all gaps (Critical/Important/Minor)

## Common Pitfalls

### Do Not

- **Modify protected files** directly - always create conflict reports
- **Skip calibration step** - raw YouTube subtitles have 6-18% error rate
- **Discard legacy information** - always preserve with [LEGACY] annotation
- **Auto-correct low confidence patterns** - flag for manual review below 95%
- **Create new files unnecessarily** - always prefer editing existing files
- **Batch tool operations sequentially** - use parallel reads when possible
- **Use v2.0 methodology** - always use v3.0 for new RAG documents

### Always

- **Read NIKKE_TERMINOLOGY.md** before character name operations
- **Verify word boundaries** when applying regex corrections (e.g., `ラビ` vs `ラビット`)
- **Include source citations** - every update needs chapter number and date
- **Generate correction reports** - never silently fix errors
- **Validate YAML frontmatter** - invalid YAML breaks document parsing
- **Check protected file list** before any write operation
- **Apply speaker inference** from video titles (v3.0 methodology)
- **Use semantic chunking** based on [音楽] markers and dialogue gaps

## Terminology Notes

### Character Name Disambiguation

- **指揮官** (Commander) - Player character, often corrupted to `福祉霊感` in subtitles
- **副司令官** (Vice Commander) - Anderson's title, NOT the player
- **Marian** (マリアン) - Operations coordinator, often truncated to `マリア`
- **Maria** - Different character introduced Ch14+, also `マリア` but different person
- **Rapi** (ラピ) - Main character, frequently misrecognized as `ラビ`

### Technical Terms

- **Rapture** (ラプチャー) - Enemy faction, often truncated to `ラプチ`
- **Core** (コア) - NIKKE system, sometimes mistranscribed as `核` (nucleus)
- **Corruption** (腐食) - Technical term, sometimes mistranscribed as `腐敗` (decay)
- **Tetra Line** (テトラライン) - Manufacturer, often truncated to `テトララ`

## Documentation Structure

### Three-Tier Documentation System

1. **RAG Documents** (`docs/videos/`) - AI-optimized retrieval format
   - 60-100 keywords for search
   - Timeline segmentation (semantic chunking)
   - Character profiles embedded
   - Worldbuilding concepts extracted
   - Speaker inference from titles

2. **Original Transcripts** (`docs/videos/`) - Complete dialogue record
   - Full timestamp preservation
   - Minimal processing
   - Reference for verification

3. **Supplementary Docs** (`docs/characters/`, `docs/worldbuilding/`)
   - Character profile files (detailed personality, relationships)
   - Worldbuilding concept files (locations, organizations, technology)
   - Cross-referenced with RAG documents

## Workflow State Recovery

If agent interrupted during batch operation:

```bash
# Check for state file
ls temp/*_state_*.json

# Resume by invoking agent with state file reference
# Agent will automatically skip completed items and continue
```

State files contain:
- Progress tracking (completed/failed items)
- Cumulative results
- Checkpoints with timestamps
- Resume instructions

## Directory Structure

```
nikkerag/
├── docs/                          # Main documentation system
│   ├── methodology/               # RAG v3.0 methodology
│   ├── timeline/                  # Story timeline (protected)
│   ├── validation/                # Quality validation
│   ├── references/                # GraphRAG paper
│   ├── calibration_reports/       # Subtitle corrections (16 files)
│   ├── characters/                # Character profiles (13 files)
│   ├── videos/                    # RAG docs (109+ files)
│   └── worldbuilding/             # Worldbuilding docs
├── dev-references/                # Development references (not in git)
│   ├── dlYTvideo/                 # Downloaded videos (1GB+, gitignored)
│   ├── awesome-ai-system-prompts/ # AI prompt references
│   └── NIKKE胜利女神全角色评分榜.pdf
├── scripts/                       # Processing scripts
├── temp/                          # Temporary files (gitignored)
├── templates/                     # Document templates
├── .claude/                       # Claude Code config
│   └── agents/                    # Agent specifications
├── NIKKE_TERMINOLOGY.md           # Terminology standards
└── README.md                      # Project overview
```

## References

**Agent Specifications**: `.claude/agents/*.md` (comprehensive 500-1000 line specs per agent)

**v3.0 Methodology**: `docs/methodology/RAG_GENERATION_METHODOLOGY.md` (complete v3.0 specification)

**Error Database**: `docs/validation/YOUTUBE_SUBTITLE_CORRECTIONS.md` (18 documented patterns with detection regex)

**Terminology Database**: `NIKKE_TERMINOLOGY.md` (50+ canonical terms, common errors)

**Templates**: `templates/rag_document_template.md` (structure for all RAG outputs)

**Protected Files**: Files in `docs/timeline/` marked immutable - check before write operations

**GraphRAG Paper**: `docs/references/graph_RAG.pdf` (Microsoft Research, theoretical foundation for v3.0)
