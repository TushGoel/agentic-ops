"""
Principle 7: Make unsafe actions structurally unavailable, not just discouraged.

Telling the model "be careful with rollbacks" in a prompt is not a control -
a confidently wrong model just ignores it. A blast-radius guard that raises
before the action runs, unless the caller explicitly opts in with a scope
that's within budget, is a control: the agent cannot execute the unsafe path
no matter what it decides.

Run: python3 07_blast_radius_guard.py
"""
from dataclasses import dataclass


@dataclass
class BlastRadiusBudget:
    max_resources_affected: int


class BlastRadiusExceeded(Exception):
    pass


def apply_rollback(deployment_ids: list[str], budget: BlastRadiusBudget, confirmed: bool):
    if len(deployment_ids) > budget.max_resources_affected and not confirmed:
        raise BlastRadiusExceeded(
            f"rollback touches {len(deployment_ids)} deployments, "
            f"budget is {budget.max_resources_affected} - requires confirmed=True"
        )
    return f"rolled back {deployment_ids}"


if __name__ == "__main__":
    budget = BlastRadiusBudget(max_resources_affected=1)

    print(apply_rollback(["d-1"], budget, confirmed=False))

    try:
        apply_rollback(["d-1", "d-2", "d-3"], budget, confirmed=False)
    except BlastRadiusExceeded as e:
        print(f"blocked: {e}")

    print(apply_rollback(["d-1", "d-2", "d-3"], budget, confirmed=True))
