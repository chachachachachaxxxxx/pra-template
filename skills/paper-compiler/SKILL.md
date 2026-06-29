---
name: paper-compiler
description: Compile external papers, paper notes, benchmark papers, or related-work excerpts into PRA records. Use when Codex needs to extract Problem, Hypothesis, Observation, Experiment, Run, source, edge, and trace metadata from a paper or literature review material.
---

# Paper Compiler

## Workflow

Read the target paper material and the project PRA conventions. If available,
read `docs/pra-schema.md` from the PRA template or project root.

Create paper-derived records without treating paper claims as verified project
truth:

1. Create or update `sources/papers/<paper-id>.yaml`.
2. Extract stable `Problem`, `Hypothesis`, and `Observation` records.
3. Mark paper-reported observations as `status: reported_by_source`.
4. Put paper argument edges in `edges/papers/<paper-id>.yaml`.
5. Create a paper-local trace in `traces/` when the paper has a readable story.
6. Leave uncertain, ambiguous, or too-granular items in `staging/`.

## Extraction Rules

- Convert paper claims into `Hypothesis`, not a separate claim type.
- Convert evidence, result tables, reported metric findings, figures, and failure
  observations into `Observation`.
- Convert evaluation designs into `Experiment`.
- Convert concrete reported executions into `Run` only when run/protocol metadata
  matters.
- Use source locators whenever possible: section, page, table, figure, appendix,
  URL, commit, or artifact path.
- Do not force similar nodes to merge. Use curated edges later.

## Benchmark Papers

For benchmark papers, identify whether the paper evaluates methods with a
benchmark, or validates a benchmark itself.

For benchmark validation, typical hypotheses include metric validity, human
agreement, ranking stability, coverage, diagnosticity, and leakage absence.
Validation results become observations.

## Output Discipline

Keep records small and traceable. Prefer one durable statement per PHO node.
Do not copy long paper passages. Summarize and cite source locators.
