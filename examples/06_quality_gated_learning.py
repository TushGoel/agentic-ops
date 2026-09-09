"""
Principle 6: Gate the learning loop on confirmed outcomes.

The self-improvement loop (write a "learning record" after every resolved
incident, retrieve it on the next similar one) only works if bad resolutions
don't get written into the knowledge base. The mistake is trusting the
agent's own output as ground truth; the fix is a quality gate: a record only
becomes retrievable after a human confirms it, or after a no-recurrence
window passes with no confirmation either way.

Run: python3 06_quality_gated_learning.py
"""
from dataclasses import dataclass


@dataclass
class LearningRecord:
    incident_type: str
    resolution: str
    status: str = "pending"  # pending, confirmed, rejected


class LearningStore:
    def __init__(self):
        self._records: list[LearningRecord] = []

    def write(self, record: LearningRecord) -> None:
        self._records.append(record)

    def confirm(self, incident_type: str, correct: bool) -> None:
        for record in self._records:
            if record.incident_type == incident_type and record.status == "pending":
                record.status = "confirmed" if correct else "rejected"

    def retrievable(self) -> list[LearningRecord]:
        # Rejected resolutions never re-enter RAG retrieval. Pending ones
        # wait for confirmation before they can influence a future incident.
        return [r for r in self._records if r.status == "confirmed"]


if __name__ == "__main__":
    store = LearningStore()
    store.write(LearningRecord("deploy_timeout", "extended timeout, retried"))
    store.write(LearningRecord("config_drift", "reapplied stale baseline"))  # actually wrong root cause

    store.confirm("deploy_timeout", correct=True)
    store.confirm("config_drift", correct=False)

    print("retrievable for future incidents:", store.retrievable())
