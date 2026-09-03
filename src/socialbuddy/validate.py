"""Validation entry points used by scripts/validate.py and tests."""

from __future__ import annotations

from pathlib import Path

from socialbuddy.context import load_bundle, validate_bundle
from socialbuddy.skills import (
    REQUIRED_HEADINGS,
    has_labeled_example,
    load_catalog,
    load_skill,
    repo_root,
)


class ValidationIssue(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


def validate_skills(root: Path | None = None) -> list[str]:
    base = root or repo_root()
    catalog = load_catalog(base)
    errors: list[str] = []
    seen_ids: set[str] = set()
    required = tuple(catalog.get("required_headings", REQUIRED_HEADINGS))

    if not catalog.get("skills"):
        errors.append("catalog.json has no skills")
        return errors

    for entry in catalog["skills"]:
        rel = entry["path"]
        path = base / rel
        skill_id = entry["id"]
        if skill_id in seen_ids:
            errors.append(f"duplicate catalog id: {skill_id}")
        seen_ids.add(skill_id)
        if not path.is_file():
            errors.append(f"missing skill file: {rel}")
            continue
        try:
            skill = load_skill(path)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        if skill.id != skill_id:
            errors.append(f"{rel}: frontmatter id {skill.id!r} != catalog {skill_id!r}")
        if skill.category != entry.get("category", skill.category):
            errors.append(f"{rel}: category mismatch with catalog")
        missing = [h for h in required if h not in skill.headings]
        if missing:
            errors.append(f"{rel}: missing headings {missing}")
        if not has_labeled_example(skill.body):
            errors.append(
                f"{rel}: Example Outputs must label examples "
                "(**Example**, 'illustration only', 'EXAMPLE —', or [example])"
            )
        if skill.status not in {"draft", "stable", "deprecated"}:
            errors.append(f"{rel}: invalid status {skill.status!r}")
    return errors


def validate_samples(root: Path | None = None) -> list[str]:
    base = root or repo_root()
    errors: list[str] = []
    sample_dir = base / "context" / "samples"
    paths = sorted(sample_dir.glob("*.json"))
    if not paths:
        errors.append("no JSON samples under context/samples")
        return errors
    for path in paths:
        try:
            bundle = load_bundle(path)
            validate_bundle(bundle, root=base)
        except (OSError, ValueError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if bundle.get("mock") is not True:
            errors.append(f"{path.name}: bundle.mock must be true")
        for i, record in enumerate(bundle.get("records", [])):
            if record.get("mock") is not True:
                errors.append(f"{path.name} record[{i}] ({record.get('id')}): mock must be true")
    return errors


def validate_repo(root: Path | None = None) -> list[str]:
    return validate_skills(root) + validate_samples(root)


def run(root: Path | None = None) -> int:
    errors = validate_repo(root)
    if errors:
        print("SocialBuddy validation failed:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("SocialBuddy validation passed.")
    return 0
