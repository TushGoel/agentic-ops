"""
Principle 4: Pick storage for your data shape, not by default.

Incident runbooks are structured (incident_type -> known resolution steps),
so an exact-match lookup by key is faster and simpler than semantic search.
Semantic fallback only kicks in when nothing matches exactly - it's a
fallback, not the primary retrieval path.

Run: python3 04_structured_knowledge_lookup.py
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Runbook:
    incident_type: str
    resolution_steps: list[str]


KNOWLEDGE_BASE: dict[str, Runbook] = {
    "deploy_timeout": Runbook("deploy_timeout", ["check_health_endpoint", "extend_timeout", "retry_deploy"]),
    "config_drift": Runbook("config_drift", ["diff_config", "reapply_baseline"]),
}


def semantic_fallback(incident_type: str) -> Runbook | None:
    # Stand-in for an embedding-similarity search when no exact key matches.
    for key, runbook in KNOWLEDGE_BASE.items():
        if key.split("_")[0] in incident_type:
            return runbook
    return None


def lookup(incident_type: str) -> tuple[Runbook | None, str]:
    exact = KNOWLEDGE_BASE.get(incident_type)
    if exact:
        return exact, "exact_match"
    fallback = semantic_fallback(incident_type)
    return fallback, "semantic_fallback" if fallback else "no_match"


if __name__ == "__main__":
    for incident_type in ["deploy_timeout", "deploy_stall", "unknown_type"]:
        runbook, source = lookup(incident_type)
        print(f"{incident_type}: {source} -> {runbook}")
