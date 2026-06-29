# Versioning

PRA Template has two version layers:

```text
Template version: the version of this public template repository.
Project schema version: the PRA schema version a concrete research project uses.
```

Concrete PRA projects should record their schema version in `pra.yaml`:

```yaml
schema: pra-template
schema_version: "0.1.0"
template_commit: ""
project:
  id: ""
  alias: ""
  context: ""
```

`template_commit` is optional but useful when a project is created from an
unreleased commit.

## Semantic Versioning

Use semantic versioning for the template and schema surface.

Patch versions are for compatible fixes:

```text
0.1.0 -> 0.1.1
```

Examples:

- Documentation corrections.
- Validator bug fixes.
- More precise error messages.
- Skill wording updates that do not change schema rules.

Minor versions are for backward-compatible schema additions:

```text
0.1.0 -> 0.2.0
```

Examples:

- New optional fields.
- New optional source locator fields.
- New relation labels that do not invalidate old relations.
- New directories that existing projects do not need immediately.

Major versions are for breaking changes:

```text
0.x -> 1.0
1.x -> 2.0
```

Examples:

- Renaming required fields.
- Moving required directories.
- Changing ID format.
- Removing or changing relation semantics.
- Changing source locator structure in a non-compatible way.

## Project Data Policy

Git records edit history. PRA status fields and curated edges record research
meaning.

Do not delete old nodes just because a hypothesis was rejected or a node was
merged. Prefer:

```yaml
status: retired
notes: >
  Superseded by H00042.
```

or a curated edge:

```yaml
from: H00017
to: H00042
relation: same_as
confidence: high
```

## Migration Scripts

Do not add migration scripts before there is a real migration. When a breaking
schema change is introduced, add a targeted script under `scripts/`, for example:

```text
scripts/migrate_0_1_to_0_2.py
```

Migration scripts should:

- Take a PRA project path as input.
- Preserve source files when possible.
- Print a summary of changed files.
- Be paired with a changelog entry describing the schema change.
