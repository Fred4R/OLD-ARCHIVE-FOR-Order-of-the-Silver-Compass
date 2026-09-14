#!/usr/bin/env python3
"""Validate Silver Compass repository integrity.

This validator protects repository structure and provenance. It does not decide
fictional canon, infer missing facts, or certify Warhammer rules beyond the
claims already recorded in the repository.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "SHA256SUMS.txt"
MASTER_PATH = ROOT / "Order_of_the_Silver_Compass_MASTER_v4.3.41.txt"
SOURCE_INDEX_PATH = ROOT / "Rules/11e/SOURCE_INDEX.md"
DETACHMENT_ROOT = ROOT / "Rules/11e/detachments"
SYSTEM_ROOT = ROOT / "Rules/11e/system"

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


def immutable_evidence_files() -> list[str]:
    paths = [MASTER_PATH]
    paths.extend(sorted((ROOT / "Sources/Armies").glob("*.txt")))
    paths.extend(sorted((ROOT / "Sources/Methodology").glob("*.pdf")))
    return [str(path.relative_to(ROOT)) for path in paths]


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

    expected = set(immutable_evidence_files())
    actual = set(manifest)

    for rel in sorted(expected - actual):
        fail(f"Checksum manifest missing immutable evidence file: {rel}")
    for rel in sorted(actual - expected):
        fail(f"Checksum manifest has non-evidence or stale file: {rel}")

    for rel in sorted(expected & actual):
        path = ROOT / rel
        if not path.exists():
            fail(f"Immutable evidence file is missing: {rel}")
            continue
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


def validate_system_files(source_ids: set[str]) -> dict[str, tuple[Path, dict[str, Any]]]:
    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    required = {
        "STRIKE_FORCE_2000.yaml": "11E-SYSTEM-STRIKE-FORCE-2000",
        "ARMY_CONSTRUCTION.yaml": "11E-SYSTEM-ARMY-CONSTRUCTION",
        "BATTLE_SEQUENCE.yaml": "11E-SYSTEM-BATTLE-SEQUENCE",
        "BATTLE_SHOCK_AND_ACTIONS.yaml": "11E-SYSTEM-BATTLE-SHOCK-ACTIONS",
        "MOVEMENT_AND_RESERVES.yaml": "11E-SYSTEM-MOVEMENT-RESERVES",
        "SHOOTING.yaml": "11E-SYSTEM-SHOOTING",
        "COMBAT.yaml": "11E-SYSTEM-COMBAT",
        "SOURCE_AND_UPDATE_ROUTING.yaml": "11E-SYSTEM-SOURCE-UPDATE-ROUTING",
    }

    if not SYSTEM_ROOT.exists():
        fail("Missing Rules/11e/system")
        return records

    for filename in required:
        path = SYSTEM_ROOT / filename
        if not path.exists():
            fail(f"Missing required system record {path.relative_to(ROOT)}")

    for path in sorted(SYSTEM_ROOT.glob("*.yaml")):
        data = load_yaml(path)
        if not data:
            continue

        validate_category_separation(path, data)

        if data.get("record_type") != "current_system_rules_record":
            fail(f"{path.relative_to(ROOT)} must use record_type current_system_rules_record")

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
                fail(
                    f"{path.relative_to(ROOT)} source_index does not resolve to "
                    "Rules/11e/SOURCE_INDEX.md"
                )

        validate_date(
            data.get("verification_as_of"),
            f"{path.relative_to(ROOT)} verification_as_of",
        )

        if data.get("edition") != 11:
            fail(f"{path.relative_to(ROOT)} must declare edition 11")

        system_id = data.get("system_id")
        if not isinstance(system_id, str) or not re.fullmatch(
            r"11E-SYSTEM-[A-Z0-9-]+", system_id
        ):
            fail(f"{path.relative_to(ROOT)} has invalid system_id {system_id!r}")
            continue
        if system_id in records:
            previous = records[system_id][0].relative_to(ROOT)
            fail(
                f"Duplicate system_id {system_id} in "
                f"{path.relative_to(ROOT)} and {previous}"
            )
            continue

        expected_id = required.get(path.name)
        if expected_id is not None and system_id != expected_id:
            fail(
                f"{path.relative_to(ROOT)} system_id must be {expected_id!r}, "
                f"found {system_id!r}"
            )

        if not isinstance(data.get("system"), str) or not data.get("system"):
            fail(f"{path.relative_to(ROOT)} missing system name")

        unknown_sources = collect_source_refs(data) - source_ids
        for source in sorted(unknown_sources):
            fail(f"{path.relative_to(ROOT)} references undefined source ID {source}")

        if contains_current_verification(data) and not collect_source_refs(data):
            fail(
                f"{path.relative_to(ROOT)} contains a verified-current claim "
                "without any OFF-* source reference"
            )

        records[system_id] = (path, data)

    return records


def validate_detachment_files(
    source_ids: set[str],
) -> dict[str, tuple[Path, dict[str, Any]]]:
    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    detachment_paths = sorted(DETACHMENT_ROOT.glob("**/*.yaml"))

    if not detachment_paths:
        fail("No current detachment YAML files found under Rules/11e/detachments")
        return records

    for path in detachment_paths:
        data = load_yaml(path)
        if not data:
            continue

        validate_category_separation(path, data)

        if data.get("record_type") != "current_detachment_record":
            fail(f"{path.relative_to(ROOT)} must use record_type current_detachment_record")

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
                fail(
                    f"{path.relative_to(ROOT)} source_index does not resolve to "
                    "Rules/11e/SOURCE_INDEX.md"
                )

        validate_date(
            data.get("verification_as_of"),
            f"{path.relative_to(ROOT)} verification_as_of",
        )

        if data.get("edition") != 11:
            fail(f"{path.relative_to(ROOT)} must declare edition 11")

        detachment_id = data.get("detachment_id")
        if not isinstance(detachment_id, str) or not re.fullmatch(
            r"11E-[A-Z0-9-]+", detachment_id
        ):
            fail(f"{path.relative_to(ROOT)} has invalid detachment_id {detachment_id!r}")
            continue
        if detachment_id in records:
            previous = records[detachment_id][0].relative_to(ROOT)
            fail(
                f"Duplicate detachment_id {detachment_id} in "
                f"{path.relative_to(ROOT)} and {previous}"
            )
            continue

        if not isinstance(data.get("faction"), str) or not data.get("faction"):
            fail(f"{path.relative_to(ROOT)} missing faction")
        if not isinstance(data.get("detachment"), str) or not data.get("detachment"):
            fail(f"{path.relative_to(ROOT)} missing detachment name")

        unknown_sources = collect_source_refs(data) - source_ids
        for source in sorted(unknown_sources):
            fail(f"{path.relative_to(ROOT)} references undefined source ID {source}")

        if contains_current_verification(data) and not collect_source_refs(data):
            fail(
                f"{path.relative_to(ROOT)} contains a verified-current claim "
                "without any OFF-* source reference"
            )

        construction = data.get("current_construction")
        if isinstance(construction, dict):
            if construction.get("verification_status") == "verified_current":
                if not isinstance(construction.get("detachment_points"), int):
                    fail(
                        f"{path.relative_to(ROOT)} verified current construction "
                        "requires integer detachment_points"
                    )
                if not isinstance(construction.get("force_disposition"), str):
                    fail(
                        f"{path.relative_to(ROOT)} verified current construction "
                        "requires force_disposition"
                    )
                if not collect_source_refs(construction):
                    fail(
                        f"{path.relative_to(ROOT)} verified current construction "
                        "requires an OFF-* source"
                    )

        enhancements = data.get("enhancements")
        if not isinstance(enhancements, list) or not enhancements:
            fail(f"{path.relative_to(ROOT)} must contain an enhancements list")
        else:
            seen_names: set[str] = set()
            for number, enhancement in enumerate(enhancements, start=1):
                if not isinstance(enhancement, dict):
                    fail(
                        f"{path.relative_to(ROOT)} enhancement {number} must be a mapping"
                    )
                    continue
                name = enhancement.get("name")
                if not isinstance(name, str) or not name:
                    fail(
                        f"{path.relative_to(ROOT)} enhancement {number} missing name"
                    )
                elif name in seen_names:
                    fail(
                        f"{path.relative_to(ROOT)} contains duplicate enhancement {name!r}"
                    )
                else:
                    seen_names.add(name)

                if enhancement.get("verification_status") == "verified_current":
                    source = enhancement.get("source")
                    if not isinstance(source, str) or source not in source_ids:
                        fail(
                            f"{path.relative_to(ROOT)} enhancement {name!r} is "
                            "verified_current without a defined OFF-* source"
                        )
                    if not isinstance(enhancement.get("points"), int):
                        fail(
                            f"{path.relative_to(ROOT)} enhancement {name!r} is "
                            "verified_current without integer points"
                        )

        project_connections = data.get("project_connections")
        if isinstance(project_connections, dict):
            guide_ref = project_connections.get("constantia_guide")
            if isinstance(guide_ref, str):
                resolve_repo_path(path, guide_ref)

        records[detachment_id] = (path, data)

    return records


def validate_detachment_links(
    detachment_records: dict[str, tuple[Path, dict[str, Any]]],
) -> None:
    for path in sorted((ROOT / "Rules/11e/units").glob("*.yaml")):
        data = load_yaml(path)
        if not data:
            continue

        links = data.get("current_detachment_records")
        if links is None:
            continue
        if not isinstance(links, dict):
            fail(f"{path.relative_to(ROOT)} current_detachment_records must be a mapping")
            continue

        for label, link in links.items():
            if not isinstance(link, dict):
                fail(
                    f"{path.relative_to(ROOT)} detachment link {label!r} must be a mapping"
                )
                continue

            detachment_id = link.get("detachment_id")
            record_ref = link.get("record")
            if detachment_id not in detachment_records:
                fail(
                    f"{path.relative_to(ROOT)} references unknown detachment_id "
                    f"{detachment_id!r}"
                )
                continue
            if not isinstance(record_ref, str):
                fail(
                    f"{path.relative_to(ROOT)} detachment link {label!r} missing record"
                )
                continue

            resolved = resolve_repo_path(path, record_ref)
            expected_path = detachment_records[detachment_id][0]
            if resolved and resolved != expected_path:
                fail(
                    f"{path.relative_to(ROOT)} detachment link {label!r} resolves to "
                    f"{resolved.relative_to(ROOT)}, expected {expected_path.relative_to(ROOT)}"
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
    system_records: dict[str, tuple[Path, dict[str, Any]]],
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

        system_context = data.get("current_system_context")
        if not isinstance(system_context, dict):
            fail(f"{path.relative_to(ROOT)} missing current_system_context")
        else:
            validate_date(
                system_context.get("as_of"),
                f"{path.relative_to(ROOT)} current_system_context.as_of",
            )
            if system_context.get("relation_type") != "reference_for_current_rules_interpretation":
                fail(
                    f"{path.relative_to(ROOT)} current_system_context has invalid relation_type"
                )

            links = system_context.get("records")
            required_links = {
                "army_construction": "11E-SYSTEM-ARMY-CONSTRUCTION",
                "missions": "11E-SYSTEM-MISSIONS",
                "terrain_and_objectives": "11E-SYSTEM-TERRAIN-AND-OBJECTIVES",
            }
            if not isinstance(links, dict):
                fail(
                    f"{path.relative_to(ROOT)} current_system_context.records must be a mapping"
                )
            else:
                for label, expected_id in required_links.items():
                    if label not in links:
                        fail(
                            f"{path.relative_to(ROOT)} missing current system link {label!r}"
                        )

                for label, link in links.items():
                    if not isinstance(link, dict):
                        fail(
                            f"{path.relative_to(ROOT)} system link {label!r} must be a mapping"
                        )
                        continue

                    system_id = link.get("system_id")
                    expected_id = required_links.get(label)
                    if expected_id is not None and system_id != expected_id:
                        fail(
                            f"{path.relative_to(ROOT)} system link {label!r} must use "
                            f"{expected_id!r}, found {system_id!r}"
                        )
                    if system_id not in system_records:
                        fail(
                            f"{path.relative_to(ROOT)} references unknown system_id "
                            f"{system_id!r}"
                        )
                        continue

                    record_ref = link.get("record")
                    if not isinstance(record_ref, str):
                        fail(
                            f"{path.relative_to(ROOT)} system link {label!r} missing record"
                        )
                    else:
                        resolved = resolve_repo_path(path, record_ref)
                        expected_path = system_records[system_id][0]
                        if resolved and resolved != expected_path:
                            fail(
                                f"{path.relative_to(ROOT)} system link {label!r} resolves to "
                                f"{resolved.relative_to(ROOT)}, expected "
                                f"{expected_path.relative_to(ROOT)}"
                            )

                    for field in ("applicability", "use", "boundary"):
                        if not isinstance(link.get(field), str) or not link.get(field):
                            fail(
                                f"{path.relative_to(ROOT)} system link {label!r} "
                                f"missing non-empty {field}"
                            )

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




def load_markdown_frontmatter(path: Path) -> dict[str, Any]:
    text = read_text(path)
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} is missing YAML front matter")
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{path.relative_to(ROOT)} has malformed YAML front matter")
        return {}
    try:
        value = yaml.load(parts[1], Loader=UniqueKeyLoader)
    except Exception as exc:
        fail(f"Front matter parse failed for {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"Front matter must be a mapping: {path.relative_to(ROOT)}")
        return {}
    return value


def validate_story_and_character_layers() -> None:
    character_readme = ROOT / "Characters/README.md"
    relationship_path = ROOT / "Relationships/RELATIONSHIPS.md"
    current_state_path = ROOT / "CURRENT_STATE.md"
    story_readme = ROOT / "Story/README.md"
    acceptance_path = ROOT / "Story/ACCEPTANCE.md"
    scene_path = ROOT / "Story/CURRENT_SCENE.yaml"
    events_path = ROOT / "Story/EVENTS.yaml"
    knowledge_path = ROOT / "Story/KNOWLEDGE.yaml"

    required_character_files = [
        ROOT / "Characters/Fred.md",
        ROOT / "Characters/Aurelia-Montfort.md",
        ROOT / "Characters/Constantia-Continuity.md",
        ROOT / "Characters/Constantia-Serenitas.md",
        ROOT / "Characters/Eulalia-Veridica.md",
        ROOT / "Characters/Helverin-Pilot.md",
        ROOT / "Characters/Justina-Voss.md",
        ROOT / "Characters/Paragon-Trio.md",
        ROOT / "Characters/Valeria.md",
        ROOT / "Characters/Warhound-Princeps.md",
    ]
    character_files = sorted(
        path for path in (ROOT / "Characters").glob("*.md") if path.name != "README.md"
    )

    required_story_files = [
        story_readme,
        acceptance_path,
        scene_path,
        events_path,
        knowledge_path,
        relationship_path,
        character_readme,
    ]
    for path in required_character_files + required_story_files:
        if not path.exists():
            fail(f"Missing story/character continuity file: {path.relative_to(ROOT)}")

    identities: set[str] = set()
    record_ids: set[str] = set()
    character_readme_text = read_text(character_readme)

    for path in character_files:
        if not path.exists():
            continue
        front = load_markdown_frontmatter(path)
        record_id = front.get("record_id")
        if not isinstance(record_id, str) or not record_id:
            fail(f"{path.relative_to(ROOT)} missing record_id")
        elif record_id in record_ids:
            fail(f"Duplicate character/person record_id {record_id}")
        else:
            record_ids.add(record_id)

        record_type = front.get("record_type")
        if record_type not in {
            "character_continuity_record",
            "character_simulation_guide",
            "user_continuity_record",
        }:
            fail(f"{path.relative_to(ROOT)} has unsupported record_type {record_type!r}")

        authority_scope = front.get("authority_scope")
        if not isinstance(authority_scope, str) or not authority_scope:
            fail(f"{path.relative_to(ROOT)} missing authority_scope")

        if "as_of" in front:
            validate_date(front.get("as_of"), f"{path.relative_to(ROOT)} as_of")

        if record_type == "character_continuity_record":
            identity = front.get("project_character_id")
            if not isinstance(identity, str) or not identity.startswith("CHAR-"):
                fail(f"{path.relative_to(ROOT)} missing project_character_id")
            else:
                identities.add(identity)
        elif record_type == "user_continuity_record":
            identity = front.get("person_id")
            if identity != "PERSON-FRED":
                fail(f"{path.relative_to(ROOT)} user continuity must use PERSON-FRED")
            else:
                identities.add(identity)
        elif record_type == "character_simulation_guide":
            if front.get("canon_status") != "INTERPRETATION":
                fail(f"{path.relative_to(ROOT)} simulation guide must remain INTERPRETATION")
            if front.get("evidence_class") != "A6":
                fail(f"{path.relative_to(ROOT)} simulation guide must remain A6")

        if path.name not in character_readme_text:
            fail(f"Characters/README.md does not route {path.name}")

    if relationship_path.exists():
        relationship_front = load_markdown_frontmatter(relationship_path)
        if relationship_front.get("record_type") != "relationship_registry":
            fail("Relationships/RELATIONSHIPS.md must use record_type relationship_registry")
        validate_date(relationship_front.get("as_of"), "Relationships/RELATIONSHIPS.md as_of")
        relationship_text = read_text(relationship_path)
        relation_ids = re.findall(r"^## (REL-[A-Z0-9-]+)$", relationship_text, flags=re.MULTILINE)
        if not relation_ids:
            fail("Relationships/RELATIONSHIPS.md contains no REL-* records")
        for relation_id in sorted(set(relation_ids)):
            if relation_ids.count(relation_id) > 1:
                fail(f"Relationships/RELATIONSHIPS.md duplicate relation ID {relation_id}")
        for reference in re.findall(r"`(\.\./[^`#]+\.md)(?:#[^`]*)?`", relationship_text):
            resolve_repo_path(relationship_path, reference)

    acceptance = load_markdown_frontmatter(acceptance_path)
    if acceptance.get("record_type") != "conversation_adoption_policy":
        fail("Story/ACCEPTANCE.md must use record_type conversation_adoption_policy")
    validate_date(acceptance.get("as_of"), "Story/ACCEPTANCE.md as_of")

    scene = load_yaml(scene_path)
    if scene.get("record_type") != "current_scene_record":
        fail("Story/CURRENT_SCENE.yaml must use record_type current_scene_record")
    validate_date(scene.get("as_of"), "Story/CURRENT_SCENE.yaml as_of")
    for key in ("authority_map", "current_state", "acceptance_policy"):
        ref = scene.get(key)
        if not isinstance(ref, str):
            fail(f"Story/CURRENT_SCENE.yaml missing {key}")
        else:
            resolve_repo_path(scene_path, ref)

    location = scene.get("location")
    if not isinstance(location, dict):
        fail("Story/CURRENT_SCENE.yaml missing location mapping")
    else:
        if location.get("local_authority") not in identities:
            fail("Story/CURRENT_SCENE.yaml local_authority is not a known character identity")
        current_state_text = read_text(current_state_path)
        for field in ("vessel", "area"):
            value = location.get(field)
            if not isinstance(value, str) or not value:
                fail(f"Story/CURRENT_SCENE.yaml location.{field} must be non-empty")
            elif value not in current_state_text:
                fail(f"CURRENT_STATE.md does not contain current-scene {field} {value!r}")

    presence = scene.get("presence")
    if not isinstance(presence, dict):
        fail("Story/CURRENT_SCENE.yaml missing presence mapping")
    else:
        if presence.get("fred") != "PERSON-FRED":
            fail("Story/CURRENT_SCENE.yaml presence.fred must be PERSON-FRED")
        if presence.get("women_with_fred") != 9:
            fail("Story/CURRENT_SCENE.yaml must preserve exactly nine women with Fred")
        if presence.get("complete_attendance_resolved") is not False:
            fail("Story/CURRENT_SCENE.yaml must preserve unresolved complete attendance")
        protected = presence.get("protected_presence")
        protected_counts: dict[str, int] = {}
        if not isinstance(protected, list):
            fail("Story/CURRENT_SCENE.yaml protected_presence must be a list")
        else:
            for item in protected:
                if not isinstance(item, dict):
                    fail("Story/CURRENT_SCENE.yaml protected_presence item must be a mapping")
                    continue
                entity_id = item.get("entity_id")
                count = item.get("count")
                if entity_id not in identities:
                    fail(f"Story/CURRENT_SCENE.yaml references unknown protected identity {entity_id!r}")
                if not isinstance(count, int) or count < 1:
                    fail(f"Story/CURRENT_SCENE.yaml has invalid protected count for {entity_id!r}")
                elif isinstance(entity_id, str):
                    protected_counts[entity_id] = count
        if protected_counts.get("CHAR-EULALIA") != 1:
            fail("Story/CURRENT_SCENE.yaml must protect Eulalia's current presence")
        if protected_counts.get("CHAR-PARAGON-TRIO") != 3:
            fail("Story/CURRENT_SCENE.yaml must protect all three Paragon pilots")

        anchors = presence.get("positive_interaction_anchors", [])
        if not isinstance(anchors, list):
            fail("Story/CURRENT_SCENE.yaml positive_interaction_anchors must be a list")
        else:
            for item in anchors:
                if not isinstance(item, dict):
                    fail("Story/CURRENT_SCENE.yaml interaction anchor must be a mapping")
                    continue
                participants = item.get("participants")
                if not isinstance(participants, list):
                    fail("Story/CURRENT_SCENE.yaml interaction anchor participants must be a list")
                    continue
                for identity in participants:
                    if identity not in identities:
                        fail(f"Story/CURRENT_SCENE.yaml interaction anchor references unknown identity {identity!r}")

    for ref in scene.get("source_refs", []):
        if isinstance(ref, str):
            resolve_repo_path(scene_path, ref)
        else:
            fail("Story/CURRENT_SCENE.yaml source_refs must contain paths")

    events = load_yaml(events_path)
    if events.get("record_type") != "event_registry":
        fail("Story/EVENTS.yaml must use record_type event_registry")
    if not isinstance(events.get("participant_list_semantics"), str) or not events.get("participant_list_semantics"):
        fail("Story/EVENTS.yaml must define participant_list_semantics")
    validate_date(events.get("as_of"), "Story/EVENTS.yaml as_of")
    for key in ("authority_map", "acceptance_policy", "current_scene"):
        ref = events.get(key)
        if not isinstance(ref, str):
            fail(f"Story/EVENTS.yaml missing {key}")
        else:
            resolve_repo_path(events_path, ref)

    event_ids: set[str] = set()
    event_sequences: set[int] = set()
    event_list = events.get("events")
    if not isinstance(event_list, list) or not event_list:
        fail("Story/EVENTS.yaml must contain events")
    else:
        for event in event_list:
            if not isinstance(event, dict):
                fail("Story/EVENTS.yaml event must be a mapping")
                continue
            event_id = event.get("event_id")
            if not isinstance(event_id, str) or not event_id.startswith("EVENT-"):
                fail(f"Story/EVENTS.yaml invalid event_id {event_id!r}")
            elif event_id in event_ids:
                fail(f"Story/EVENTS.yaml duplicate event_id {event_id}")
            else:
                event_ids.add(event_id)
            sequence = event.get("sequence")
            if not isinstance(sequence, int):
                fail(f"Story/EVENTS.yaml {event_id} sequence must be integer")
            elif sequence in event_sequences:
                fail(f"Story/EVENTS.yaml duplicate sequence {sequence}")
            else:
                event_sequences.add(sequence)
            if event.get("canon_status") not in ALLOWED_CANON_STATUSES:
                fail(f"Story/EVENTS.yaml {event_id} has invalid canon_status")
            if event.get("evidence_class") not in ALLOWED_EVIDENCE_CLASSES:
                fail(f"Story/EVENTS.yaml {event_id} has invalid evidence_class")
            participants = event.get("participants", [])
            if not isinstance(participants, list):
                fail(f"Story/EVENTS.yaml {event_id} participants must be a list")
            else:
                for identity in participants:
                    if identity not in identities:
                        fail(f"Story/EVENTS.yaml {event_id} references unknown identity {identity!r}")
            refs = event.get("source_refs")
            if not isinstance(refs, list) or not refs:
                fail(f"Story/EVENTS.yaml {event_id} missing source_refs")
            else:
                for ref in refs:
                    if isinstance(ref, str):
                        resolve_repo_path(events_path, ref)
                    else:
                        fail(f"Story/EVENTS.yaml {event_id} source_refs must contain paths")

    knowledge = load_yaml(knowledge_path)
    if knowledge.get("record_type") != "knowledge_registry":
        fail("Story/KNOWLEDGE.yaml must use record_type knowledge_registry")
    validate_date(knowledge.get("as_of"), "Story/KNOWLEDGE.yaml as_of")
    auth_ref = knowledge.get("authority_map")
    if isinstance(auth_ref, str):
        resolve_repo_path(knowledge_path, auth_ref)
    else:
        fail("Story/KNOWLEDGE.yaml missing authority_map")

    claim_ids: set[str] = set()
    claims = knowledge.get("claims")
    if not isinstance(claims, list) or not claims:
        fail("Story/KNOWLEDGE.yaml must contain claims")
    else:
        for claim in claims:
            if not isinstance(claim, dict):
                fail("Story/KNOWLEDGE.yaml claim must be a mapping")
                continue
            claim_id = claim.get("claim_id")
            if not isinstance(claim_id, str) or not claim_id.startswith("KNOW-"):
                fail(f"Story/KNOWLEDGE.yaml invalid claim_id {claim_id!r}")
            elif claim_id in claim_ids:
                fail(f"Story/KNOWLEDGE.yaml duplicate claim_id {claim_id}")
            else:
                claim_ids.add(claim_id)
            holders = claim.get("holders")
            if not isinstance(holders, list) or not holders:
                fail(f"Story/KNOWLEDGE.yaml {claim_id} must have holders")
            else:
                for identity in holders:
                    if identity not in identities:
                        fail(f"Story/KNOWLEDGE.yaml {claim_id} references unknown holder {identity!r}")
            if not isinstance(claim.get("content"), str) or not claim.get("content"):
                fail(f"Story/KNOWLEDGE.yaml {claim_id} missing content")
            if not isinstance(claim.get("evidence_basis"), str) or not claim.get("evidence_basis"):
                fail(f"Story/KNOWLEDGE.yaml {claim_id} missing evidence_basis")
            refs = claim.get("source_refs")
            if not isinstance(refs, list) or not refs:
                fail(f"Story/KNOWLEDGE.yaml {claim_id} missing source_refs")
            else:
                for ref in refs:
                    if isinstance(ref, str):
                        resolve_repo_path(knowledge_path, ref)
                    else:
                        fail(f"Story/KNOWLEDGE.yaml {claim_id} source_refs must contain paths")

    routing_requirements = {
        ROOT / "README.md": ["Story/", "Characters/Fred.md", "Reference/Secondary/Wahapedia/"],
        ROOT / "AGENTS.md": ["Story/CURRENT_SCENE.yaml", "Story/KNOWLEDGE.yaml", "Story/EVENTS.yaml", "Story/ACCEPTANCE.md"],
        ROOT / "AUTHORITY.md": ["Story/CURRENT_SCENE.yaml", "Story/EVENTS.yaml", "Story/KNOWLEDGE.yaml", "Story/ACCEPTANCE.md", "Characters/Fred.md"],
        current_state_path: ["Story/CURRENT_SCENE.yaml", "Story/EVENTS.yaml", "Story/KNOWLEDGE.yaml", "Story/ACCEPTANCE.md", "Characters/Fred.md"],
        ROOT / "USING_REPOSITORY.md": ["Story/CURRENT_SCENE.yaml", "Story/EVENTS.yaml", "Story/KNOWLEDGE.yaml", "Story/ACCEPTANCE.md", "Characters/Fred.md"],
    }
    for path, required_strings in routing_requirements.items():
        text = read_text(path)
        for required in required_strings:
            if required not in text:
                fail(f"{path.relative_to(ROOT)} does not route required story record {required!r}")


def validate_secondary_reference() -> None:
    root = ROOT / "Reference/Secondary/Wahapedia"
    data_root = root / "11e"
    readme = root / "README.md"
    required = [
        readme,
        data_root / "Abilities.csv",
        data_root / "Datasheets.csv",
        data_root / "Detachments.csv",
        data_root / "Enhancements.csv",
        data_root / "Factions.csv",
        data_root / "Last_update.csv",
        data_root / "Source.csv",
        data_root / "Stratagems.csv",
    ]
    for path in required:
        if not path.exists():
            fail(f"Missing Wahapedia secondary-reference file: {path.relative_to(ROOT)}")

    readme_text = read_text(readme).lower()
    for phrase in ("secondary", "non-authoritative", "official"):
        if phrase not in readme_text:
            fail(f"Reference/Secondary/Wahapedia/README.md missing authority boundary term {phrase!r}")

    csv_paths = sorted(data_root.glob("*.csv"))
    if not csv_paths:
        fail("No Wahapedia CSV files found")
    for path in csv_paths:
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle, delimiter="|")
                header = next(reader, None)
        except Exception as exc:
            fail(f"Cannot parse secondary-reference CSV {path.relative_to(ROOT)}: {exc}")
            continue
        if not header or not any(str(cell).strip() for cell in header):
            fail(f"Secondary-reference CSV has no usable header: {path.relative_to(ROOT)}")

    rules_readme = read_text(ROOT / "Rules/11e/README.md")
    routing_text = read_text(ROOT / "Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml")
    for path, text in (
        (ROOT / "Rules/11e/README.md", rules_readme),
        (ROOT / "Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml", routing_text),
    ):
        if "Reference/Secondary/Wahapedia" not in text:
            fail(f"{path.relative_to(ROOT)} does not route the Wahapedia secondary reference")

    routing = load_yaml(ROOT / "Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml")
    secondary = routing.get("secondary_discovery_reference")
    if not isinstance(secondary, dict):
        fail("SOURCE_AND_UPDATE_ROUTING.yaml missing secondary_discovery_reference")
    else:
        if secondary.get("authority") != "non_authoritative":
            fail("Wahapedia secondary discovery route must remain non_authoritative")
        for key in ("record", "dataset"):
            ref = secondary.get(key)
            if not isinstance(ref, str):
                fail(f"Wahapedia secondary discovery route missing {key}")
            else:
                resolve_repo_path(ROOT / "Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml", ref)


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



def validate_connections() -> None:
    required_files = [
        ROOT / "AUTHORITY.md",
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "STATUS.md",
        ROOT / "SOURCES.md",
        ROOT / "CURRENT_STATE.md",
        ROOT / "USING_REPOSITORY.md",
        ROOT / "Story/README.md",
        ROOT / "Story/ACCEPTANCE.md",
        ROOT / "Story/CURRENT_SCENE.yaml",
        ROOT / "Story/EVENTS.yaml",
        ROOT / "Story/KNOWLEDGE.yaml",
        ROOT / "Characters/README.md",
        ROOT / "Characters/Fred.md",
        ROOT / "Relationships/RELATIONSHIPS.md",
        ROOT / "Reference/Secondary/Wahapedia/README.md",
        ROOT / "Rules/11e/README.md",
        ROOT / "Rules/11e/system/SOURCE_AND_UPDATE_ROUTING.yaml",
        ROOT / "scripts/validate_repository.py",
        ROOT / "requirements-validator.txt",
        ROOT / ".github/workflows/validate-repository.yml",
        ROOT / "Rules/11e/SOURCE_INDEX.md",
    ]
    for path in required_files:
        if not path.exists():
            fail(f"Missing required connected file: {path.relative_to(ROOT)}")

    retired_references = [
        "NEW_CONVERSATION.md",
        "CONTINUATION.md",
        "Stories/Illustrative",
        "Rules/11e/system/README.md",
        "Rules/11e/detachments/README.md",
        "Rules/11e/formations/Adepta-Sororitas/Constantia-Dialogus-Retributors.yaml",
    ]
    routing_files = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "AUTHORITY.md",
        ROOT / "CURRENT_STATE.md",
        ROOT / "USING_REPOSITORY.md",
        ROOT / "Rules/11e/README.md",
        ROOT / "Characters/README.md",
        ROOT / "Characters/Fred.md",
        ROOT / "Characters/Constantia-Serenitas.md",
        ROOT / "Story/README.md",
        ROOT / "Story/ACCEPTANCE.md",
    ]
    for path in routing_files:
        if not path.exists():
            continue
        text = read_text(path)
        for retired in retired_references:
            if retired in text:
                fail(
                    f"{path.relative_to(ROOT)} still references retired repository path "
                    f"{retired!r}"
                )


def main() -> int:
    validate_connections()
    validate_core_markdown()
    validate_story_and_character_layers()
    validate_secondary_reference()
    validate_manifest()
    master_text = validate_master()
    source_ids = validate_source_index()
    system_records = validate_system_files(source_ids)
    detachment_records = validate_detachment_files(source_ids)
    rule_records, _ = validate_rules_files(master_text, source_ids)
    validate_detachment_links(detachment_records)
    validate_armies(master_text, source_ids, rule_records, system_records)

    if errors:
        print(f"Repository validation FAILED with {len(errors)} error(s):")
        for number, message in enumerate(errors, start=1):
            print(f"{number}. {message}")
        return 1

    print("Repository validation PASSED.")
    print("Checked: immutable-evidence hashes, canonical Compendium identity, YAML syntax,")
    print("authority/status separation, army arithmetic, exact source payloads,")
    print("project/rules/source IDs, system/Detachment/army links, roster-occurrence links,")
    print("current-claim provenance, story/character/knowledge wiring, secondary-reference")
    print("integrity, core-document heading uniqueness, and routing integrity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
