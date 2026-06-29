---
name: graph-curator
description: Curate PRA graph duplicates and near-duplicates by proposing same_as, close_to, broader_than, narrower_than, related_to, or conflicts_with edges. Use when multiple papers or project sessions create similar Problem, Hypothesis, or Observation records that need canonicalization.
---

# Graph Curator

## Workflow

Compare candidate PHO nodes without over-merging.

1. Read the candidate records and their source locators.
2. Preserve paper-local wording when it captures a meaningful distinction.
3. Use curated edges for equivalence, similarity, hierarchy, or conflict.
4. Write curation edges to `edges/curated/*.yaml`.
5. Only mark nodes as merged or canonical when the user explicitly wants that
   stronger policy.

## Curation Relations

Use these relation labels:

```text
same_as
close_to
broader_than
narrower_than
related_to
conflicts_with
```

Prefer `close_to` when two nodes are similar but emphasize different mechanisms,
scope, dataset, benchmark, or interpretation.

## Output Discipline

Each proposed curation edge should include:

- `from`
- `to`
- `relation`
- `context`
- `confidence`
- `sources`

Do not create a separate `mappings/` directory. Use curated edges as the mapping
layer.
