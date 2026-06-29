---
name: rigor-reviewer
description: Review a PRA project for research-logic rigor, PHO type errors, unsupported or overconfident hypotheses, weak source locators, overstrong edges, stale staging, and provenance gaps. Use when Codex needs an agentic audit beyond static schema validation.
---

# Rigor Reviewer

## Workflow

Run static validation first when a validator is available. Then perform a
semantic review of the records and graph.

Prioritize findings that could change research conclusions:

1. Observations that contain interpretation instead of recorded fact.
2. Hypotheses that are not testable or cannot be supported/refuted.
3. Problems that are actually claims or observations.
4. Paper-reported observations treated as reproduced-by-us.
5. Edges whose relation is too strong for the evidence.
6. High confidence without source locators or supporting observations.
7. Accepted-for-paper hypotheses without adequate observations.
8. Runs that produce observations but lack command/config/artifact provenance.

## Review Output

Lead with issues ordered by severity. For each issue, include record IDs,
file paths, and the reason the current encoding is risky.

Use concise recommendations:

- retype node
- weaken relation
- lower confidence
- add source locator
- split observation from hypothesis
- move rough item back to staging
- add missing provenance edge

Do not rewrite the whole project unless explicitly asked.
