---
name: session-compiler
description: Compile live research discussions, experiment-review sessions, planning notes, or chat transcripts into PRA session notes, staging items, and stable PHO or edge records. Use when Codex needs to keep project research metadata current during ongoing work.
---

# Session Compiler

## Workflow

Capture the session first; promote only stable content.

1. Write a concise `sessions/session-YYYY-MM-DD-<topic>.md` note covering what
   was decided, inspected, deferred, or rejected.
2. Put immature ideas, rough observations, quotes, and unresolved fragments in
   `staging/`.
3. Promote staging items only when they have a stable statement, a source, and a
   target type.
4. Create or update PHO/E/R records only for content that is stable enough to
   reference later.
5. Add edges for relationships that were explicitly decided or strongly implied.

## Promotion Rules

A staging item can be promoted when:

- It has a stable `statement`.
- It has at least one `source`, preferably with a locator.
- Its target type is clear: `Problem`, `Hypothesis`, `Observation`,
  `Experiment`, `Run`, `edge`, or `source`.
- An observation is phrased as a fact, not an interpretation.
- A hypothesis is supportable, weakenable, or refutable by observations.
- A problem states a research gap or question.

After promotion, keep the staging item and set `status: promoted` plus
`promoted_to`.

## Boundaries

`sessions/` records what happened in the work session. `staging/` records the
raw material being processed. Do not mix full discussion logs into formal PHO
records.
