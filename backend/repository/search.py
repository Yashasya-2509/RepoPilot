import re
from pathlib import Path

from backend.config import Settings
from backend.repository.loader import inspect_repository, safe_read_text


def search_repository(root: Path, query: str, limit: int, settings: Settings) -> list[dict]:
    """Simple explainable lexical search. Scores are ranking heuristics, not probabilities."""
    terms = [term.lower() for term in re.findall(r"[A-Za-z0-9_]+", query) if len(term) > 1]
    if not terms:
        return []

    inventory = inspect_repository(root, settings)
    hits = []
    for item in inventory["files"]:
        try:
            content = safe_read_text(root, item["path"], settings)
        except (OSError, ValueError):
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            lowered = line.lower()
            matched = sum(1 for term in terms if term in lowered)
            if matched:
                score = matched / len(set(terms))
                # Small boost for identifier-like matches; not a calibrated probability.
                if any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in terms):
                    score += 0.1
                hits.append({
                    "path": item["path"],
                    "line_number": line_number,
                    "line": line.strip()[:500],
                    "score": round(min(score, 1.1), 4),
                })

    hits.sort(key=lambda hit: (-hit["score"], hit["path"], hit["line_number"]))
    return hits[: min(limit, settings.max_search_results)]
