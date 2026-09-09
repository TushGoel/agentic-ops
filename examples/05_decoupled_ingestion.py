"""
Principle 5: Decouple ingestion from processing.

A burst of correlated alerts (one root cause, many downstream failures)
should not spawn one workflow execution per alert. A queue in front of the
trigger buffers the burst and deduplicates related events before anything
downstream even starts.

Run: python3 05_decoupled_ingestion.py
"""
import time
from dataclasses import dataclass, field


@dataclass
class IngestionQueue:
    dedup_window_seconds: int = 60
    _seen: dict[str, float] = field(default_factory=dict)
    _buffered: list[dict] = field(default_factory=list)

    def enqueue(self, event: dict, now: float) -> bool:
        dedup_key = event["dedup_key"]
        last_seen = self._seen.get(dedup_key)
        if last_seen is not None and now - last_seen < self.dedup_window_seconds:
            return False  # duplicate within window, dropped
        self._seen[dedup_key] = now
        self._buffered.append(event)
        return True

    def drain(self) -> list[dict]:
        buffered, self._buffered = self._buffered, []
        return buffered


if __name__ == "__main__":
    queue = IngestionQueue(dedup_window_seconds=60)
    now = time.time()

    events = [
        {"dedup_key": "deploy-svc-a-failed", "detail": "first alert"},
        {"dedup_key": "deploy-svc-a-failed", "detail": "duplicate 4s later"},
        {"dedup_key": "deploy-svc-b-failed", "detail": "unrelated failure"},
    ]
    for i, event in enumerate(events):
        accepted = queue.enqueue(event, now=now + i * 4)
        print(f"{event['detail']}: {'accepted' if accepted else 'deduplicated'}")

    print("workflows to trigger:", queue.drain())
