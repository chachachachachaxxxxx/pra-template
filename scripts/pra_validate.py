#!/usr/bin/env python3
"""Validate a PRA project directory.

The validator intentionally checks hard structural rules only. It does not try
to judge research truth, whether an observation really supports a hypothesis, or
whether the graph is acyclic.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ENTITY_DIRS = {
    "problems": ("problem", "P"),
    "hypotheses": ("hypothesis", "H"),
    "observations": ("observation", "O"),
    "experiments": ("experiment", "E"),
    "runs": ("run", "R"),
}

COMMON_FIELDS = {
    "id",
    "type",
    "alias",
    "statement",
    "context",
    "status",
    "sources",
}

PHO_RELATIONS = {
    ("problem", "problem"): {"decomposes", "reframes", "relates_to"},
    ("problem", "hypothesis"): {"motivates", "asks_for_explanation"},
    ("problem", "observation"): {"asks_to_check", "asks_for_observation"},
    ("hypothesis", "hypothesis"): {
        "refines",
        "contradicts",
        "generalizes",
        "specializes",
    },
    ("hypothesis", "observation"): {"predicts", "expects", "asks_to_observe"},
    ("hypothesis", "problem"): {"answers", "reframes", "partially_resolves"},
    ("observation", "observation"): {
        "reproduces",
        "contradicts",
        "extends",
        "aggregates",
    },
    ("observation", "hypothesis"): {"suggests", "supports", "refutes", "qualifies"},
    ("observation", "problem"): {"raises", "resolves", "reframes"},
}

PROVENANCE_RELATIONS = {
    ("problem", "experiment"): {"investigates"},
    ("hypothesis", "experiment"): {"tested_by"},
    ("experiment", "run"): {"instantiated_by", "has_run"},
    ("experiment", "observation"): {"produces", "expected_to_produce"},
    ("run", "observation"): {"produces", "records"},
}

CURATION_RELATIONS = {
    "same_as",
    "close_to",
    "broader_than",
    "narrower_than",
    "related_to",
    "conflicts_with",
}

CONFIDENCE_VALUES = {"low", "medium", "high", "unknown"}


class Issue:
    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        self.message = message

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_yaml(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parse error: {exc}") from exc


def yaml_files(root: Path) -> list[Path]:
    return sorted(
        path
        for pattern in ("*.yaml", "*.yml")
        for path in root.rglob(pattern)
        if path.is_file()
    )


def validate_source_list(path: Path, value: Any, issues: list[Issue]) -> None:
    if not isinstance(value, list):
        issues.append(Issue(path, "sources must be a list"))
        return
    for index, item in enumerate(value):
        if isinstance(item, str):
            if not item:
                issues.append(Issue(path, f"sources[{index}] must not be empty"))
            continue
        if not isinstance(item, dict):
            issues.append(Issue(path, f"sources[{index}] must be a string or object"))
            continue
        if not item.get("id"):
            issues.append(Issue(path, f"sources[{index}] object requires id"))


def validate_entity_file(
    path: Path,
    expected_type: str,
    expected_prefix: str,
    entities: dict[str, dict[str, Any]],
    issues: list[Issue],
) -> None:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        issues.append(Issue(path, str(exc)))
        return
    if not isinstance(data, dict):
        issues.append(Issue(path, "entity record must be a mapping"))
        return

    missing = sorted(COMMON_FIELDS - set(data))
    if missing:
        issues.append(Issue(path, f"missing common fields: {', '.join(missing)}"))

    entity_id = data.get("id")
    if not isinstance(entity_id, str) or not re.match(rf"^{expected_prefix}[0-9]{{5}}$", entity_id):
        issues.append(Issue(path, f"id must match {expected_prefix}00000 format"))
        return

    if data.get("type") != expected_type:
        issues.append(Issue(path, f"type must be {expected_type!r}"))

    if entity_id in entities:
        issues.append(Issue(path, f"duplicate id {entity_id}"))
    entities[entity_id] = {"type": expected_type, "path": path, "data": data}

    for field in ("alias", "statement", "context", "status"):
        if field in data and not isinstance(data[field], str):
            issues.append(Issue(path, f"{field} must be a string"))
    if "confidence" in data:
        confidence = data["confidence"]
        if confidence is not None and not isinstance(confidence, (str, int, float)):
            issues.append(Issue(path, "confidence must be string, number, or null"))
    if "sources" in data:
        validate_source_list(path, data["sources"], issues)


def validate_staging_file(
    path: Path,
    entities: dict[str, dict[str, Any]],
    staging_ids: set[str],
    issues: list[Issue],
) -> None:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        issues.append(Issue(path, str(exc)))
        return
    if not isinstance(data, dict):
        issues.append(Issue(path, "staging record must be a mapping"))
        return
    staging_id = data.get("id")
    if not isinstance(staging_id, str) or not re.match(r"^S[0-9]{5}$", staging_id):
        issues.append(Issue(path, "staging id must match S00000 format"))
    elif staging_id in staging_ids:
        issues.append(Issue(path, f"duplicate staging id {staging_id}"))
    else:
        staging_ids.add(staging_id)

    if data.get("type") != "staging_item":
        issues.append(Issue(path, "staging type must be 'staging_item'"))
    for field in ("raw", "candidate_types", "sources", "status", "promoted_to"):
        if field not in data:
            issues.append(Issue(path, f"missing staging field {field}"))
    if "sources" in data:
        validate_source_list(path, data["sources"], issues)
    promoted_to = data.get("promoted_to", [])
    if not isinstance(promoted_to, list):
        issues.append(Issue(path, "promoted_to must be a list"))
    else:
        for target_id in promoted_to:
            if target_id not in entities:
                issues.append(Issue(path, f"promoted_to target {target_id} does not exist"))


def relation_allowed(from_type: str, to_type: str, relation: str) -> bool:
    if relation in PHO_RELATIONS.get((from_type, to_type), set()):
        return True
    if relation in PROVENANCE_RELATIONS.get((from_type, to_type), set()):
        return True
    if relation in CURATION_RELATIONS:
        return True
    return False


def validate_edge_file(
    path: Path,
    entities: dict[str, dict[str, Any]],
    issues: list[Issue],
) -> None:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        issues.append(Issue(path, str(exc)))
        return
    if not isinstance(data, dict):
        issues.append(Issue(path, "edge set must be a mapping"))
        return
    edges = data.get("edges")
    if edges is None:
        issues.append(Issue(path, "edge set requires top-level edges list"))
        return
    if not isinstance(edges, list):
        issues.append(Issue(path, "edges must be a list"))
        return
    for index, edge in enumerate(edges):
        label = f"edges[{index}]"
        if not isinstance(edge, dict):
            issues.append(Issue(path, f"{label} must be a mapping"))
            continue
        from_id = edge.get("from")
        to_id = edge.get("to")
        relation = edge.get("relation")
        if from_id not in entities:
            issues.append(Issue(path, f"{label}.from {from_id!r} does not exist"))
            continue
        if to_id not in entities:
            issues.append(Issue(path, f"{label}.to {to_id!r} does not exist"))
            continue
        if not isinstance(relation, str) or not relation:
            issues.append(Issue(path, f"{label}.relation must be a non-empty string"))
            continue
        from_type = entities[from_id]["type"]
        to_type = entities[to_id]["type"]
        if not relation_allowed(from_type, to_type, relation):
            issues.append(
                Issue(
                    path,
                    f"{label} relation {relation!r} is not allowed for {from_type}->{to_type}",
                )
            )
        confidence = edge.get("confidence")
        if isinstance(confidence, str) and confidence not in CONFIDENCE_VALUES:
            issues.append(Issue(path, f"{label}.confidence should be one of {sorted(CONFIDENCE_VALUES)}"))
        if "sources" in edge:
            validate_source_list(path, edge["sources"], issues)


def validate_trace_file(path: Path, project_root: Path, entities: dict[str, dict[str, Any]], issues: list[Issue]) -> None:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        issues.append(Issue(path, str(exc)))
        return
    if not isinstance(data, dict):
        issues.append(Issue(path, "trace must be a mapping"))
        return
    for field in ("id", "alias", "edge_sets", "nodes"):
        if field not in data:
            issues.append(Issue(path, f"missing trace field {field}"))
    edge_sets = data.get("edge_sets", [])
    if not isinstance(edge_sets, list):
        issues.append(Issue(path, "edge_sets must be a list"))
    else:
        for edge_set in edge_sets:
            edge_path = project_root / str(edge_set)
            if not edge_path.exists():
                issues.append(Issue(path, f"edge_set does not exist: {edge_set}"))
    nodes = data.get("nodes", {})
    if not isinstance(nodes, dict):
        issues.append(Issue(path, "nodes must be a mapping"))
        return
    for key in ("include", "exclude"):
        values = nodes.get(key, [])
        if not isinstance(values, list):
            issues.append(Issue(path, f"nodes.{key} must be a list"))
            continue
        for node_id in values:
            if node_id not in entities:
                issues.append(Issue(path, f"nodes.{key} references missing id {node_id}"))


def validate_project(project_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    entities: dict[str, dict[str, Any]] = {}

    for dirname, (expected_type, expected_prefix) in ENTITY_DIRS.items():
        directory = project_root / dirname
        if not directory.exists():
            issues.append(Issue(directory, "missing entity directory"))
            continue
        for path in yaml_files(directory):
            validate_entity_file(path, expected_type, expected_prefix, entities, issues)

    staging_ids: set[str] = set()
    staging_dir = project_root / "staging"
    if staging_dir.exists():
        for path in yaml_files(staging_dir):
            validate_staging_file(path, entities, staging_ids, issues)
    else:
        issues.append(Issue(staging_dir, "missing staging directory"))

    edges_dir = project_root / "edges"
    if edges_dir.exists():
        for path in yaml_files(edges_dir):
            validate_edge_file(path, entities, issues)
    else:
        issues.append(Issue(edges_dir, "missing edges directory"))

    traces_dir = project_root / "traces"
    if traces_dir.exists():
        for path in yaml_files(traces_dir):
            validate_trace_file(path, project_root, entities, issues)
    else:
        issues.append(Issue(traces_dir, "missing traces directory"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PRA project directory")
    parser.add_argument("project_root", type=Path, help="PRA project directory to validate")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    if not project_root.exists():
        print(f"Project root does not exist: {project_root}", file=sys.stderr)
        return 2
    issues = validate_project(project_root)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1
    print(f"OK: {project_root} is a valid PRA project")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
