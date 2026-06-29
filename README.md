# PRA Template

PRA Template is a small public template for Project-native Research Artifacts.
It organizes research metadata as a graph of:

```text
Problem / Hypothesis / Observation
```

`Experiment` and `Run` remain provenance entities that explain how observations
were designed and produced. Existing project code, results, papers, and logs stay
where they are; PRA records stable IDs, summaries, source locators, edges, and
artifact references.

## Contents

```text
template/          Empty PRA project skeleton
schemas/           JSON Schema references for core record shapes
scripts/           Static validation tools
skills/            Codex skill drafts for compiling and reviewing PRA records
docs/              Design notes and conventions
```

## Quick Start

Copy `template/` into a project, then add YAML records under the entity
directories:

```bash
cp -R template my-project-pra
python scripts/pra_validate.py my-project-pra
```

Install the only runtime dependency for the validator, or run it with `uv`:

```bash
python -m pip install pyyaml
uv run --with PyYAML python scripts/pra_validate.py my-project-pra
```

## Core Directories

```text
problems/
hypotheses/
observations/
experiments/
runs/
edges/
  papers/
  project/
  curated/
traces/
sources/
  papers/
  datasets/
  codebases/
staging/
sessions/
```

## License

MIT.
