# PRA Schema Notes

PRA is a research metadata layer. It records structured summaries and references
without moving canonical source files, experiments, logs, or paper assets.

## Main Graph

Only three node types are first-class research graph nodes:

```text
Problem
Hypothesis
Observation
```

`Experiment` and `Run` are provenance entities. They can be linked by edges, but
the default readable trace should foreground PHO.

## Common Entity Fields

All `Problem`, `Hypothesis`, `Observation`, `Experiment`, and `Run` records use:

```yaml
id: P00001
type: problem
alias: "Short display name"
statement: >
  Stable statement of the node.
context: >
  Background, scope, caveats, and explanation.
status: active
confidence: null
sources:
  - id: paper-example
    locator: "Section 3 / Table 2"
    note: "Precise source note."
notes: ""
```

`sources` are provenance locators, not graph edges. They may be simple strings or
objects with `id`, `locator`, and `note`.

## Entity Status

Recommended status values:

```text
problem: open / active / partially_answered / answered / closed / deferred
hypothesis: proposed / active / supported / weakened / rejected / accepted_for_paper / retired
observation: reported_by_source / observed_by_us / reproduced_by_us / partially_reproduced / contradicted_by_us / invalid / superseded
experiment: planned / running / complete / abandoned
run: planned / running / complete / failed / invalid
```

## Edges

Edges are stored separately from nodes:

```yaml
edges:
  - from: O00001
    to: P00001
    relation: raises
    context: >
      Why this relation exists.
    confidence: medium
    sources:
      - id: paper-example
        locator: "Section 3"
```

Use `edges/papers/` for paper-local argument edges, `edges/project/` for project
research edges, and `edges/curated/` for manually merged equivalence or high
confidence views.

## Trace Views

Traces are views over entities and edge sets:

```yaml
id: trace-example
alias: "Example trace"
edge_sets:
  - edges/papers/paper-example.yaml
nodes:
  include:
    - P00001
    - H00001
    - O00001
  exclude: []
layout:
  mode: layered
```

The underlying graph may contain cycles. Do not force DAG assumptions.

## Staging

Staging is the inbox for immature material. Promote staging items only when they
have a stable statement, a source, and a target type.

```yaml
id: S00001
type: staging_item
alias: ""
raw: >
  Rough note, quote, chat fragment, table observation, or idea.
candidate_types:
  - observation
sources:
  - id: paper-example
    locator: "Table 2"
status: inbox
promoted_to: []
notes: ""
```
