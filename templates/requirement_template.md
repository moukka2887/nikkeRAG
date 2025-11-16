# OpenSpec Requirement Template

Use this template for defining agent requirements in OpenSpec format.

---

```markdown
### Requirement: [Requirement Name]
The agent SHALL/MUST [requirement statement].

#### Scenario: [Scenario Name]
- WHEN [trigger condition or context]
- THEN [expected behavior or action]
- AND [additional condition or verification step]

**Rationale**: [Why this requirement exists]

**Example**:
\`\`\`markdown
[Concrete example of this requirement in action,
showing both the trigger and the expected behavior]
\`\`\`

**Validation**:
- [ ] [How to verify this requirement is met]
- [ ] [Additional validation criteria]

**Related Requirements**:
- [Link to related requirement 1]
- [Link to related requirement 2]
```

---

## Guidelines

### Requirement Statement

**Use SHALL for**:
- Mandatory behaviors
- Core functionality
- Safety-critical operations

**Use MUST for**:
- Critical requirements that cannot be violated
- Security requirements
- Data integrity requirements

**Use SHOULD for**:
- Recommended practices
- Optional enhancements
- Performance optimizations

### Scenario Writing

**Good Scenarios**:
- Specific and testable
- Clear trigger conditions
- Explicit expected outcomes
- Verifiable results

**Bad Scenarios**:
- Vague or ambiguous
- Multiple unrelated conditions
- Unclear expected behavior

### Example Quality

**✅ Good Example**:
```markdown
#### Scenario: File Not Found
- WHEN agent attempts to read transcript file
- AND file does not exist at expected path
- THEN agent SHALL search alternative locations
- THEN agent SHALL log search results
- AND if still not found, report error to user with specific path

Example:
<think>
Transcript file not found at: /mnt/f/nikkerag/temp/Chapter_14_transcript.json
Searching alternative locations:
- /mnt/f/nikkerag/temp/ch14_transcript.json
- /mnt/f/nikkerag/downloads/Chapter_14_transcript.json
Not found in alternatives. Reporting to user.
</think>

Transcript file not found.
Expected path: /mnt/f/nikkerag/temp/Chapter_14_transcript.json
Searched: 2 alternative locations

Recommendation: Run video-transcription-mcp agent first.
```

**❌ Bad Example**:
```markdown
#### Scenario: Handle Missing Files
- WHEN file is missing
- THEN do something appropriate
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
