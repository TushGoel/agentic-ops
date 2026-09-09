"""
Principle 1: Durable execution beats a custom retry loop.

A plain `while` loop in a worker process loses all progress if the process
restarts mid-workflow. This wrapper checkpoints progress after every step to
disk (a stand-in for what Step Functions / Temporal do with a state history),
so a crash mid-way resumes at the last completed step instead of step zero.

Run: python3 01_durable_execution.py
"""
import json
import os

CHECKPOINT_FILE = "/tmp/agentic-ops-checkpoint.json"


class DurableWorkflow:
    def __init__(self, workflow_id: str, steps: list[str]):
        self.workflow_id = workflow_id
        self.steps = steps

    def _load_checkpoint(self) -> int:
        if not os.path.exists(CHECKPOINT_FILE):
            return 0
        with open(CHECKPOINT_FILE) as f:
            state = json.load(f)
        if state.get("workflow_id") != self.workflow_id:
            return 0
        return state.get("completed_step_index", 0)

    def _save_checkpoint(self, step_index: int) -> None:
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump({"workflow_id": self.workflow_id, "completed_step_index": step_index}, f)

    def run(self, step_fn) -> None:
        start = self._load_checkpoint()
        if start > 0:
            print(f"Resuming workflow '{self.workflow_id}' at step {start} (skipping {start} completed steps)")
        for i in range(start, len(self.steps)):
            step_fn(self.steps[i])
            self._save_checkpoint(i + 1)
        os.remove(CHECKPOINT_FILE)


if __name__ == "__main__":
    steps = ["fetch_logs", "classify_failure", "apply_fix", "create_ticket"]
    workflow = DurableWorkflow("incident-4471", steps)
    workflow.run(lambda step: print(f"executing: {step}"))
