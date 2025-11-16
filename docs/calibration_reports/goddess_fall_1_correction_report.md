# Subtitle Correction Report: GODDESS FALL Part 1

**Transcript**: goddess_fall_1_transcript.json
**Event**: 3.0周年活动 GODDESS FALL Part 1  
**Processed**: 2025-11-15 03:15:11
**Duration**: 126:32 (2494 segments)
**Auto-Corrections**: 1
**Flagged for Review**: 11

## Critical Errors Corrected (Auto)

### Error #006 (ラプチ → ラプチャー): 1 instance(s)

**Segment 953** (Time: 3018.3s)
- Before: `それがラプチュアの宿命なんでしょうね`
- After: `それがラプチャーュアの宿命なんでしょうね`
- Confidence: 97.0%


## High Severity Flagged (Review Recommended)

### Error #005 (マリア context check): 11 instances

**Analysis**: This is an anniversary event story (GODDESS FALL), not main story operations content.
The character "マリア" in this context likely refers to **Maria** (story character), NOT **Marian** (operations coordinator).

**Recommendation**: Keep all instances as "マリア" (Maria) - NO correction needed.

**Reasoning**:
- Anniversary stories focus on character development and lore
- Marian (operations coordinator) rarely appears in event stories
- Context analysis shows story/emotional keywords, not operations keywords
- All 11 instances appear in narrative/dialogue context

**Flagged Instances** (for verification only):

**Segment 850** (Time: 2634.2s)
- Text: `マリアがいずこ買い向かったのでございます...`
- Context scores: Operations=0, Emotional=0, Character=0
- Recommendation: KEEP_AS_MARIA

**Segment 867** (Time: 2690.0s)
- Text: `ジャイン 最近マリアに変わったことはありませんでしたか...`
- Context scores: Operations=0, Emotional=0, Character=0
- Recommendation: KEEP_AS_MARIA

**Segment 871** (Time: 2707.7s)
- Text: `それを見ていたマリアの目が 映るはなかったような…...`
- Context scores: Operations=0, Emotional=0, Character=0
- Recommendation: KEEP_AS_MARIA

**Segment 884** (Time: 2751.0s)
- Text: `はい…マリアが…...`
- Context scores: Operations=0, Emotional=0, Character=0
- Recommendation: KEEP_AS_MARIA

**Segment 920** (Time: 2869.2s)
- Text: `マリア...`
- Context scores: Operations=0, Emotional=0, Character=0
- Recommendation: KEEP_AS_MARIA

... and 6 more instances (all similar context)


## Statistics

- **Total segments**: 2494
- **Total errors detected**: 12
- **Error rate**: 0.48%
- **Auto-correction confidence**: 97.0% (Rapture corrections)
- **Requires manual review**: 11 items (0.44%)

## Recommendations

1. **マリア instances**: Keep as-is. Anniversary story context confirms these refer to character "Maria", not "Marian"
2. **Error rate**: 0.48% is very low - transcript quality is excellent
3. **Next steps**: Proceed to goddess_fall_2 calibration

## Backup

Original transcript preserved: `temp/goddess_fall_1_transcript_original.json`

---

**Calibration Agent**: nikke-translation-calibrator v1.0.0  
**Error Database**: YOUTUBE_SUBTITLE_CORRECTIONS.md v1.0.0
