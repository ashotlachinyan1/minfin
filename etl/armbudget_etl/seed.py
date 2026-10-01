"""Loader and structural checks for seed/headline_facts.json (spec 4.4, 14.3)."""

import json
from pathlib import Path
from typing import Any

from armbudget_etl.paths import SEED_DIR

CONFIDENCE_LEVELS = frozenset({"verified", "calc", "assumption", "estimate", "media"})
HEADLINE_FACTS_PATH = SEED_DIR / "headline_facts.json"


def load_headline_facts(path: Path = HEADLINE_FACTS_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
    return data


def check_headline_facts(data: dict[str, Any]) -> list[str]:
    """Return a list of structural problems; empty list means the seed file is usable."""
    problems: list[str] = []
    facts: list[dict[str, Any]] = data.get("facts", [])
    if not facts:
        problems.append("no facts")
    seen: set[str] = set()
    for fact in facts:
        fid = str(fact.get("id", "<missing id>"))
        if fid in seen:
            problems.append(f"{fid}: duplicate id")
        seen.add(fid)
        conf = fact.get("confidence")
        if conf not in CONFIDENCE_LEVELS:
            problems.append(f"{fid}: invalid confidence {conf!r}")
        if conf == "media" and not (fact.get("source") or {}).get("url"):
            problems.append(f"{fid}: media fact without source.url")
        if conf == "calc" and not fact.get("formula"):
            problems.append(f"{fid}: calc fact without formula")
    return problems
