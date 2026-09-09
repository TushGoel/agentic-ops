"""
Principle 3: Route by workflow shape, not through a single generic pipeline.

Batch triage (many known-pattern incidents, speed matters) and deep
investigation (one novel incident, accuracy matters) have opposite
requirements. A router that picks the configuration up front - instead of
one model/timeout/tool-budget for everything - lets each shape run well.

Run: python3 03_workflow_router.py
"""
from dataclasses import dataclass


@dataclass
class WorkflowConfig:
    model: str
    max_tool_calls: int
    timeout_seconds: int


BATCH_CONFIG = WorkflowConfig(model="claude-haiku", max_tool_calls=2, timeout_seconds=120)
DEEP_CONFIG = WorkflowConfig(model="claude-opus", max_tool_calls=15, timeout_seconds=1800)


def route_incident(known_pattern: bool, queue_depth: int) -> WorkflowConfig:
    if known_pattern and queue_depth > 1:
        return BATCH_CONFIG
    return DEEP_CONFIG


if __name__ == "__main__":
    cases = [
        ("known pattern, 12 similar incidents queued", True, 12),
        ("novel incident, alone in queue", False, 1),
    ]
    for label, known_pattern, queue_depth in cases:
        config = route_incident(known_pattern, queue_depth)
        print(f"{label} -> {config}")
