#!/usr/bin/env python3
"""Validate skill contracts, catalog paths, and labeled mock context samples."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from socialbuddy.validate import run  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(run(ROOT))
