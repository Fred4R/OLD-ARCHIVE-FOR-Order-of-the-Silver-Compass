#!/usr/bin/env python3
"""Validate Silver Compass repository integrity.

This validator protects repository structure and provenance. It does not decide
fictional canon, infer missing facts, or certify Warhammer rules beyond the
claims already recorded in the repository.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "SHA256SUMS.txt"
MASTER_PATH = ROOT / "Order_of_the_Silver_Compass_MASTER_v4.3.41.txt"
SOURCE_INDEX_PATH = ROOT / "Rules/11e/SOURCE_INDEX.md"

ALLOWED_EVIDENCE_CLASSES = {
    "A1", "A1-REPORTED", "A2", "A3", "A4", "A5", "A6", "A7", "A8"
}
ALLOWED_CANON_STATUSES = {
    "ESTABLISHED_PROJECT_CANON",
    "INTERPRETATION",
    "PROPOSAL",
    "UNRESOLVED",
    "REJECTED",
}
KNOWN_VERIFICATION_STATUSES = {
    "verified_current",
    "partially_verified_current",
    "not_yet_verified",
    "blocked_current_source",
    "not_fully_verified",
    "not_certified",
}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"Cannot read UTF-8 text file {path.relative_to(ROOT)}: {exc}")
        return ""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:
        fail(f"YAML parse failed for {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"YAML root must be a mapping: {path.relative_to(ROOT)}")
        return {}
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return sorted(p for p in result.stdout.decode("utf-8").split("\0") if p)
    except Exception as exc:
        fail(f"Could not enumerate tracked files with git: {exc}")
        return []


def resolve_repo_path(base_file: Path, reference: str) -> Path | None:
    candidate = (base_file.parent / reference).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        fail(f"Path escapes repository: {base_file.relative_to(ROOT)} -> {reference}")
        return None
    if not candidate.exists():
        fail(f"Referenced path does not exist: {base_file.relative_to(ROOT)} -> {reference}")
        return None
    return candidate


def validate_date(value: Any, context: str) -> None:
    if not isinstance(value, str):
        fail(f"{context} must be an ISO date string")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        fail(f"{context} is not a valid ISO date: {value!r}")


def walk(value: Any) -> Iterable[tuple[str | None, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield None, child
            yield from walk(child)


def collect_source_refs(value: Any) -> set[str]:
    refs: set[str] = set()

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if key == "source" and isinstance(child, str) and child.startswith("OFF-"):
                    refs.add(child)
                elif key == "sources" and isinstance(child, list):
                    refs.update(
                        item for item in child
                        if isinstance(item, str) and item.startswith("OFF-")
                    )
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return refs


def contains_current_verification(value: Any) -> bool:
    for key, child in walk(value):
        if key in {"status", "verification_status"} and child in {
            "verified_current", "partially_verified_current"
        }:
            return True
    return False


def validate_manifest() -> None:
    if not MANIFEST_PATH.exists():
        fail("Missing SHA256SUMS.txt")
        return

    manifest: dict[str, str] = {}
    line_re = re.compile(r"^([0-9a-f]{64})  (.+)$")
    for number, line in enumerate(read_text(MANIFEST_PATH).splitlines(), start=1):
        if not line.strip():
            continue
        match = line_re.fullmatch(line)
        if not match:
            fail(f"Malformed SHA256SUMS.txt line {number}: {line!r}")
            continue
        digest, rel = match.groups()
        if rel in manifest:
            fail(f"Duplicate checksum entry for {rel}")
        manifest[rel] = digest

    tracked = set(tracked_files())
    expected = tracked - {"SHA256SUMS.txt"}
    actual = set(manifest)

    for rel in sorted(expected - actual):
        fail(f"Checksum manifest missing tracked file: {rel}")
    for rel in sorted(actual - expected):
        fail(f"Checksum manifest has non-tracked or stale file: {rel}")

    for rel in sorted(expected & actual):
        path = ROOT / rel
        digest = sha256_file(path)
        if digest != manifest[rel]:
            fail(
                f"Checksum mismatch for {rel}: "
                f"manifest={manifest[rel]} actual={digest}"
            )


def validate_master() -> str:
    if not MASTER_PATH.exists():
        fail(f"Missing canonical Compendium: {MASTER_PATH.name}")
        return ""

    text = read_text(MASTER_PATH)
    match = re.search(r"^CANONICAL_FILENAME:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        fail("Compendium does not declare CANONICAL_FILENAME")
    elif match.group(1).strip() != MASTER_PATH.name:
        fail(
            "Compendium canonical filename does not match repository path: "
            f"declared={match.group(1).strip()!r} actual={MASTER_PATH.name!r}"
        )

    if "REVIEW_STATUS: REVISED CANDIDATE — user acceptance not established." not in text:
        fail("Preserved Compendium review-status statement is missing or changed")

    return text


def validate_source_index() -> set[str]:
    if not SOURCE_INDEX_PATH.exists():
        fail("Missing Rules/11e/SOURCE_INDEX.md")
        return set()

    text = read_text(SOURCE_INDEX_PATH)
    ids = re.findall(r"^## (OFF-[A-Z0-9.-]+)$", text, flags=re.MULTILINE)
    if len(ids) != len(set(ids)):
        fail("Rules/11e/SOURCE_INDEX.md contains duplicate OFF-* source IDs")
    return set(ids)


def validate_category_separation(path: Path, data: dict[str, Any]) -> None:
    for key, value in walk(data):
        if key == "status" and isinstance(value, str):
            if value in ALLOWED_EVIDENCE_CLASSES or value == "SOURCE_SNAPSHOT":
                fail(
                    f"{path.relative_to(ROOT)} mixes category {value!r} into generic status; "
                    "use evidence_class or record_type"
                )
            if re.fullmatch(r"A\d(?:-REPORTED)?(?:_.+)?", value):
                fail(
                    f"{path.relative_to(ROOT)} stores evidence-like value {value!r} as status"
                )

        if key == "evidence_class" and value not in ALLOWED_EVIDENCE_CLASSES:
            fail(f"{path.relative_to(ROOT)} has invalid evidence_class {value!r}")

        if key == "canon_status" and value is not None and value not in ALLOWED_CANON_STATUSES:
            fail(f"{path.relative_to(ROOT)} has invalid canon_status {value!r}")

        if key == "verification_status" and isinstance(value, str):
            if value not in KNOWN_VERIFICATION_STATUSES:
                fail(
                    f"{path.relative_to(ROOT)} has unknown verification_status {value!r}"
                )


def validate_rules_files(
    master_text: str,
    source_ids: set[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, tuple[Path, dict[str, Any]]]]:
    project_units = set(re.findall(r"\bUNIT-[A-Z0-9-]+\b", master_text))
    rule_records: dict[str, dict[str, Any]] = {}
    rule_locations: dict[str, tuple[Path, dict[str, Any]]] = {}

    rules_paths = sorted((ROOT / "Rules/11e/units").glob("*.yaml"))
    if not rules_paths:
        fail("No current rules YAML files found under Rules/11e/units")

    for path in rules_paths:
        data = load_yaml(path)
        if not data:
            continue

        validate_category_separation(path, data)

        if data.get("record_type") != "current_rules_crosswalk":
            fail(f"{path.relative_to(ROOT)} must use record_type current_rules_crosswalk")

        authority_ref = data.get("authority_map")
        if not isinstance(authority_ref, str):
            fail(f"{path.relative_to(ROOT)} missing authority_map")
        else:
            resolve_repo_path(path, authority_ref)

        source_index_ref = data.get("source_index")
        if not isinstance(source_index_ref, str):
            fail(f"{path.relative_to(ROOT)} missing source_index")
        else:
            resolved = resolve_repo_path(path, source_index_ref)
            if resolved and resolved != SOURCE_INDEX_PATH:
                fail(f"{path.relative_to(ROOT)} source_index does not resolve to Rules/11e/SOURCE_INDEX.md")

        validate_date(data.get("verification_as_of"), f"{path.relative_to(ROOT)} verification_as_of")

        units = data.get("units")
        if not isinstance(units, dict):
            fail(f"{path.relative_to(ROOT)} missing units mapping")
            continue

        unknown_sources = collect_source_refs(data) - source_ids
        for source in sorted(unknown_sources):
            fail(f"{path.relative_to(ROOT)} references undefined source ID {source}")

        for rule_id, record in units.items():
            if rule_id in rule_records:
                previous = rule_locations[rule_id][0].relative_to(ROOT)
                fail(
                    f"Duplicate rules ID {rule_id} in {path.relative_to(ROOT)} "
                    f"and {previous}"
                )
                continue
            if not isinstance(record, dict):
                fail(f"{path.relative_to(ROOT)} {rule_id} must be a mapping")
                continue

            rule_records[rule_id] = record
            rule_locations[rule_id] = (path, record)

            project_unit_id = record.get("project_unit_id")
            if project_unit_id not in project_units:
                fail(
                    f"{path.relative_to(ROOT)} {rule_id} references missing "
                    f"project unit {project_unit_id!r}"
                )

            occurrences = record.get("roster_occurrences")
            if not isinstance(occurrences, list) or not all(isinstance(x, str) for x in occurrences):
                fail(f"{path.relative_to(ROOT)} {rule_id} has invalid roster_occurrences")

            current_points = record.get("current_points")
            if isinstance(current_points, dict):
                point_status = current_points.get("status")
                if point_status == "verified_current":
                    source = current_points.get("source")
                    if not isinstance(source, str) or source not in source_ids:
                        fail(
                            f"{path.relative_to(ROOT)} {rule_id} has verified current points "
                            "without a defined OFF-* source"
                        )
                elif point_status == "blocked_current_source":
                    source = current_points.get("source")
                    if not isinstance(source, str) or source not in source_ids:
                        fail(
                            f"{path.relative_to(ROOT)} {rule_id} has blocked current points "
                            "without a defined source"
                        )

            if contains_current_verification(record) and not collect_source_refs(record):
                fail(
                    f"{path.relative_to(ROOT)} {rule_id} contains a verified-current "
                    "claim without any OFF-* source reference"
                )

    return rule_records, rule_locations


def validate_armies(
    master_text: str,
    source_ids: set[str],
    rule_records: dict[str, dict[str, Any]],
) -> None:
    project_units = set(re.findall(r"\bUNIT-[A-Z0-9-]+\b", master_text))
    project_characters = set(re.findall(r"\bCHAR-[A-Z0-9-]+\b", master_text))

    force_index: dict[str, tuple[Path, dict[str, Any], set[str]]] = {}
    expected_rule_occurrences: set[tuple[str, str]] = set()

    army_paths = sorted((ROOT / "Armies").glob("**/*.yaml"))
    if not army_paths:
        fail("No army crosswalk YAML files found under Armies")

    for path in army_paths:
        data = load_yaml(path)
        if not data:
            continue

        validate_category_separation(path, data)

        if data.get("record_type") != "roster_crosswalk":
            fail(f"{path.relative_to(ROOT)} must use record_type roster_crosswalk")

        force_id = data.get("force_id")
        if not isinstance(force_id, str):
            fail(f"{path.relative_to(ROOT)} missing force_id")
            continue
        if force_id in force_index:
            fail(f"Duplicate force_id {force_id}")
            continue

        authority_ref = data.get("authority_map")
        if not isinstance(authority_ref, str):
            fail(f"{path.relative_to(ROOT)} missing authority_map")
        else:
            resolve_repo_path(path, authority_ref)

        source_snapshot = data.get("source_snapshot")
        if not isinstance(source_snapshot, dict):
            fail(f"{path.relative_to(ROOT)} missing source_snapshot")
            continue

        if source_snapshot.get("record_type") != "source_snapshot":
            fail(f"{path.relative_to(ROOT)} source_snapshot must use record_type source_snapshot")
        if source_snapshot.get("evidence_class") != "A2":
            fail(f"{path.relative_to(ROOT)} source_snapshot must use evidence_class A2")

        exact_ref = source_snapshot.get("exact_source_file")
        exact_sha = source_snapshot.get("exact_source_sha256")
        exact_path: Path | None = None
        if not isinstance(exact_ref, str):
            fail(f"{path.relative_to(ROOT)} missing exact_source_file")
        else:
            exact_path = resolve_repo_path(path, exact_ref)
        if not isinstance(exact_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", exact_sha):
            fail(f"{path.relative_to(ROOT)} has invalid exact_source_sha256")
        elif exact_path and sha256_file(exact_path) != exact_sha:
            fail(f"{path.relative_to(ROOT)} exact source SHA-256 does not match {exact_ref}")

        embedded = source_snapshot.get("embedded_duplicate")
        if isinstance(embedded, dict) and exact_path:
            embedded_ref = embedded.get("file")
            if isinstance(embedded_ref, str):
                embedded_path = resolve_repo_path(path, embedded_ref)
                if embedded_path:
                    exact_text = read_text(exact_path)
                    embedded_text = read_text(embedded_path)
                    if exact_text not in embedded_text:
                        fail(
                            f"{path.relative_to(ROOT)} exact source payload is not present "
                            f"in embedded duplicate {embedded_ref}"
                        )
            else:
                fail(f"{path.relative_to(ROOT)} embedded_duplicate missing file")

        direct = data.get("direct_user_resupply")
        if isinstance(direct, dict):
            if direct.get("evidence_class") != "A1":
                fail(f"{path.relative_to(ROOT)} direct_user_resupply must use evidence_class A1")
            if "date" in direct:
                validate_date(direct["date"], f"{path.relative_to(ROOT)} direct_user_resupply.date")

        current_rules = data.get("current_rules_status")
        if isinstance(current_rules, dict):
            validate_date(current_rules.get("as_of"), f"{path.relative_to(ROOT)} current_rules_status.as_of")

        formations = data.get("formations")
        if not isinstance(formations, dict):
            fail(f"{path.relative_to(ROOT)} missing formations mapping")
            continue

        formation_ids = set(formations)
        force_index[force_id] = (path, data, formation_ids)

        point_total = 0
        model_total = 0
        occurrence_count = 0

        for formation_id, formation in formations.items():
            if not re.fullmatch(r"F\d+-\d+", str(formation_id)):
                fail(f"{path.relative_to(ROOT)} invalid formation ID {formation_id!r}")
            if not isinstance(formation, dict):
                fail(f"{path.relative_to(ROOT)} formation {formation_id} must be a mapping")
                continue

            formation_points = formation.get("snapshot_points")
            formation_models = formation.get("models")
            if not isinstance(formation_points, int):
                fail(f"{path.relative_to(ROOT)} {formation_id} snapshot_points must be integer")
                formation_points = 0
            if not isinstance(formation_models, int):
                fail(f"{path.relative_to(ROOT)} {formation_id} models must be integer")
                formation_models = 0
            point_total += formation_points
            model_total += formation_models

            units = formation.get("units")
            if not isinstance(units, list) or not units:
                fail(f"{path.relative_to(ROOT)} {formation_id} must contain units")
                continue

            unit_point_values: list[int] = []
            for unit in units:
                if not isinstance(unit, dict):
                    fail(f"{path.relative_to(ROOT)} {formation_id} has non-mapping unit")
                    continue
                occurrence_count += 1

                project_unit_id = unit.get("project_unit_id")
                rule_id = unit.get("rules_id")
                if project_unit_id not in project_units:
                    fail(
                        f"{path.relative_to(ROOT)} {formation_id} references missing "
                        f"project unit {project_unit_id!r}"
                    )
                if rule_id not in rule_records:
                    fail(
                        f"{path.relative_to(ROOT)} {formation_id} references missing rules ID "
                        f"{rule_id!r}"
                    )
                elif rule_records[rule_id].get("project_unit_id") != project_unit_id:
                    fail(
                        f"{path.relative_to(ROOT)} {formation_id} maps {project_unit_id!r} "
                        f"to {rule_id}, whose project_unit_id differs"
                    )

                occurrence = f"{force_id}/{formation_id}"
                if isinstance(rule_id, str):
                    expected_rule_occurrences.add((rule_id, occurrence))

                unit_points = unit.get("snapshot_points")
                if isinstance(unit_points, int):
                    unit_point_values.append(unit_points)

                for identity_key in ("project_identity", "collective_project_identity"):
                    identity = unit.get(identity_key)
                    if isinstance(identity, str) and identity not in project_characters:
                        fail(
                            f"{path.relative_to(ROOT)} {formation_id} references missing "
                            f"character {identity}"
                        )

            if len(unit_point_values) == len(units) and sum(unit_point_values) != formation_points:
                fail(
                    f"{path.relative_to(ROOT)} {formation_id} unit snapshot points "
                    f"sum to {sum(unit_point_values)}, not formation total {formation_points}"
                )

        listed_points = source_snapshot.get("listed_points")
        listed_models = source_snapshot.get("model_count")
        if point_total != listed_points:
            fail(
                f"{path.relative_to(ROOT)} formations total {point_total} points, "
                f"source_snapshot lists {listed_points}"
            )
        if model_total != listed_models:
            fail(
                f"{path.relative_to(ROOT)} formations total {model_total} models, "
                f"source_snapshot lists {listed_models}"
            )

        integrity = data.get("integrity")
        if not isinstance(integrity, dict):
            fail(f"{path.relative_to(ROOT)} missing integrity mapping")
        else:
            if integrity.get("formation_points_total") != point_total:
                fail(f"{path.relative_to(ROOT)} integrity formation_points_total is stale")
            if integrity.get("formation_models_total") != model_total:
                fail(f"{path.relative_to(ROOT)} integrity formation_models_total is stale")

            declared_occurrences = integrity.get("unit_occurrences")
            if declared_occurrences is not None and declared_occurrences != occurrence_count:
                fail(
                    f"{path.relative_to(ROOT)} integrity unit_occurrences={declared_occurrences}, "
                    f"actual={occurrence_count}"
                )

            expected_counts = integrity.get("expected_rules_records_used")
            if expected_counts is None:
                expected_counts = integrity.get("expected_rules_records")
            if isinstance(expected_counts, dict):
                expected_count = sum(
                    value for value in expected_counts.values() if isinstance(value, int)
                )
                if expected_count != occurrence_count:
                    fail(
                        f"{path.relative_to(ROOT)} expected rules count={expected_count}, "
                        f"actual unit occurrences={occurrence_count}"
                    )

        unknown_sources = collect_source_refs(data) - source_ids
        for source in sorted(unknown_sources):
            fail(f"{path.relative_to(ROOT)} references undefined source ID {source}")

    actual_rule_occurrences: set[tuple[str, str]] = set()
    for rule_id, record in rule_records.items():
        occurrences = record.get("roster_occurrences")
        if not isinstance(occurrences, list):
            continue
        for occurrence in occurrences:
            if not isinstance(occurrence, str):
                continue
            actual_rule_occurrences.add((rule_id, occurrence))
            match = re.fullmatch(r"([^/]+)/(F\d+-\d+)", occurrence)
            if not match:
                fail(f"Rules record {rule_id} has malformed roster occurrence {occurrence!r}")
                continue
            force_id, formation_id = match.groups()
            if force_id not in force_index:
                fail(f"Rules record {rule_id} references unknown force {force_id}")
            elif formation_id not in force_index[force_id][2]:
                fail(
                    f"Rules record {rule_id} references unknown formation "
                    f"{force_id}/{formation_id}"
                )

    for pair in sorted(expected_rule_occurrences - actual_rule_occurrences):
        fail(f"Army crosswalk occurrence missing from rules record: {pair[0]} -> {pair[1]}")
    for pair in sorted(actual_rule_occurrences - expected_rule_occurrences):
        fail(f"Rules record has stale/unmatched roster occurrence: {pair[0]} -> {pair[1]}")



def validate_core_markdown() -> None:
    core_paths = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "AUTHORITY.md",
        ROOT / "STATUS.md",
        ROOT / "SOURCES.md",
    ]
    for path in core_paths:
        text = read_text(path)
        headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
        duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
        for heading in duplicates:
            fail(
                f"{path.relative_to(ROOT)} contains duplicate level-2 heading "
                f"{heading!r}"
            )


def validate_illustrative_stories() -> None:
    story_root = ROOT / "Stories/Illustrative"
    if not story_root.exists():
        return

    boundary = story_root / "README.md"
    if not boundary.exists():
        fail("Stories/Illustrative exists without its README boundary file")

    story_paths = sorted(
        path for path in story_root.glob("*.md")
        if path.name != "README.md"
    )
    for path in story_paths:
        text = read_text(path)
        required = {
            "RECORD_TYPE": "illustrative_story",
            "CANON_STATUS": "PROPOSAL",
            "EVIDENCE_CLASS": "A7",
        }
        for field, expected in required.items():
            match = re.search(
                rf"^{re.escape(field)}:\s*(.+?)\s*$",
                text,
                flags=re.MULTILINE,
            )
            if not match:
                fail(f"{path.relative_to(ROOT)} missing {field}")
            elif match.group(1).strip() != expected:
                fail(
                    f"{path.relative_to(ROOT)} {field} must be {expected!r}, "
                    f"found {match.group(1).strip()!r}"
                )

        continuity = re.search(
            r"^CONTINUITY_BASIS:\s*(.+?)\s*$",
            text,
            flags=re.MULTILINE,
        )
        if not continuity or not continuity.group(1).strip():
            fail(f"{path.relative_to(ROOT)} missing CONTINUITY_BASIS")

        purpose = re.search(
            r"^PURPOSE:\s*(.+?)\s*$",
            text,
            flags=re.MULTILINE,
        )
        if not purpose or "not adopted" not in purpose.group(1).lower():
            fail(
                f"{path.relative_to(ROOT)} PURPOSE must explicitly state "
                "that the scene is not adopted into story history"
            )


def validate_connections() -> None:
    required_files = [
        ROOT / "AUTHORITY.md",
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "STATUS.md",
        ROOT / "SOURCES.md",
        ROOT / "scripts/validate_repository.py",
        ROOT / "requirements-validator.txt",
        ROOT / ".github/workflows/validate-repository.yml",
    ]
    for path in required_files:
        if not path.exists():
            fail(f"Missing required connected file: {path.relative_to(ROOT)}")

    checks = {
        ROOT / "README.md": ["scripts/validate_repository.py", "Validate repository integrity"],
        ROOT / "AGENTS.md": ["scripts/validate_repository.py"],
        ROOT / "AUTHORITY.md": ["scripts/validate_repository.py"],
    }
    for path, required_fragments in checks.items():
        text = read_text(path)
        for fragment in required_fragments:
            if fragment not in text:
                fail(f"{path.relative_to(ROOT)} does not connect validator reference {fragment!r}")


def main() -> int:
    validate_connections()
    validate_core_markdown()
    validate_illustrative_stories()
    validate_manifest()
    master_text = validate_master()
    source_ids = validate_source_index()
    rule_records, _ = validate_rules_files(master_text, source_ids)
    validate_armies(master_text, source_ids, rule_records)

    if errors:
        print(f"Repository validation FAILED with {len(errors)} error(s):")
        for number, message in enumerate(errors, start=1):
            print(f"{number}. {message}")
        return 1

    print("Repository validation PASSED.")
    print("Checked: tracked-file hashes, canonical Compendium identity, YAML syntax,")
    print("authority/status separation, army arithmetic, exact source payloads,")
    print("project/rules/source IDs, roster-occurrence links, current-claim provenance,")
    print("core-document heading uniqueness, and illustrative-story proposal boundaries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
