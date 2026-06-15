"""Helpers for loading static data from Rego files.

This project uses Rego as the source-of-truth format for policy and ticket
seed data in the `data/` folder.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _extract_rego_assignment(text: str, variable_name: str) -> str:
    """Extract the JSON-like object/list assigned with `:=` in a Rego file."""
    pattern = re.compile(rf"^\s*{re.escape(variable_name)}\s*:=", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Variable '{variable_name}' not found in Rego file")

    idx = match.end()
    while idx < len(text) and text[idx].isspace():
        idx += 1

    if idx >= len(text) or text[idx] not in "[{":
        raise ValueError(f"Variable '{variable_name}' must be assigned to list or object")

    opener = text[idx]
    closer = "]" if opener == "[" else "}"
    depth = 0
    in_string = False
    escaped = False

    start = idx
    for i in range(idx, len(text)):
        ch = text[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    raise ValueError(f"Could not parse Rego value for '{variable_name}'")


def load_rego_data(filename: str, variable_name: str, top_key: str) -> dict[str, Any]:
    """Load list data from a Rego file into a dict wrapper for existing callers."""
    data_path = Path(__file__).parent.parent / "data" / filename
    if not data_path.exists():
        return {top_key: []}

    try:
        content = data_path.read_text(encoding="utf-8")
        raw_value = _extract_rego_assignment(content, variable_name)
        parsed = json.loads(raw_value)
        if isinstance(parsed, list):
            return {top_key: parsed}
    except Exception:
        return {top_key: []}

    return {top_key: []}
