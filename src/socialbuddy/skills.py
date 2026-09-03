"""Load and inspect skill Markdown modules (stdlib only)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re

REQUIRED_HEADINGS = (
    "Purpose",
    "Activation / Use Cases",
    "Inputs",
    "Procedure",
    "Quality Rubric",
    "Failure Modes",
    "Safety Notes",
    "Example Outputs",
    "Verified vs Assumed",
)

EXAMPLE_LABEL = re.compile(
    r"(\*\*Example\*\*|illustration only|EXAMPLE —|\[example\])",
    re.IGNORECASE,
)

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Skill:
    id: str
    title: str
    version: str
    status: str
    category: str
    path: Path
    headings: tuple[str, ...]
    body: str
    frontmatter: dict[str, object]


def repo_root(start: Path | None = None) -> Path:
    here = start or Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "skills" / "catalog.json").is_file():
            return candidate
    raise FileNotFoundError("Could not locate skills/catalog.json")


def parse_frontmatter(text: str) -> dict[str, object]:
    match = _FRONTMATTER.match(text)
    if not match:
        raise ValueError("Skill file is missing YAML-like frontmatter")
    data: dict[str, object] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - "):
            if current_list is None or current_key is None:
                raise ValueError(f"List item without key: {line}")
            current_list.append(line[4:].strip())
            data[current_key] = current_list
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            if value:
                data[current_key] = value
                current_list = None
            else:
                current_list = []
                data[current_key] = current_list
            continue
        raise ValueError(f"Unparseable frontmatter line: {line}")
    return data


def headings_in(text: str) -> tuple[str, ...]:
    return tuple(_HEADING.findall(text))


def load_skill(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    for key in ("id", "title", "version", "status", "category"):
        if key not in meta or not isinstance(meta[key], str):
            raise ValueError(f"{path}: frontmatter missing string field {key}")
    return Skill(
        id=str(meta["id"]),
        title=str(meta["title"]),
        version=str(meta["version"]),
        status=str(meta["status"]),
        category=str(meta["category"]),
        path=path,
        headings=headings_in(text),
        body=text,
        frontmatter=meta,
    )


def load_catalog(root: Path | None = None) -> dict:
    base = root or repo_root()
    return json.loads((base / "skills" / "catalog.json").read_text(encoding="utf-8"))


def example_section(text: str) -> str:
    match = re.search(
        r"^## Example Outputs\s*$",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        return ""
    start = match.end()
    nxt = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end]


def has_labeled_example(text: str) -> bool:
    return bool(EXAMPLE_LABEL.search(example_section(text)))
