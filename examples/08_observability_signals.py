"""
Principle 8: Instrument three signal types from day one, not after incidents force it.

Operational metrics tell you if the system is running. Agent-quality metrics
tell you if the agent is behaving well. Business metrics tell you if any of
this matters. Emitting only the first type is how teams get paged by a
"healthy" agent that's quietly wrong.

Run: python3 08_observability_signals.py
"""
from dataclasses import dataclass, field


@dataclass
class WorkflowOutcome:
    duration_seconds: float
    auto_resolved: bool
    human_reversed: bool
    tool_calls: int
    manual_minutes_saved: float


@dataclass
class SignalAggregator:
    outcomes: list[WorkflowOutcome] = field(default_factory=list)

    def record(self, outcome: WorkflowOutcome) -> None:
        self.outcomes.append(outcome)

    def report(self) -> dict:
        n = len(self.outcomes)
        auto_resolved = sum(o.auto_resolved for o in self.outcomes)
        reversed_count = sum(o.human_reversed for o in self.outcomes)
        return {
            "operational": {
                "avg_duration_seconds": sum(o.duration_seconds for o in self.outcomes) / n,
                "avg_tool_calls": sum(o.tool_calls for o in self.outcomes) / n,
            },
            "agent_quality": {
                "resolution_rate": auto_resolved / n,
                "false_positive_rate": reversed_count / n,
            },
            "business": {
                "total_manual_minutes_saved": sum(o.manual_minutes_saved for o in self.outcomes),
            },
        }


if __name__ == "__main__":
    aggregator = SignalAggregator()
    aggregator.record(WorkflowOutcome(90, True, False, 3, 40))
    aggregator.record(WorkflowOutcome(150, True, True, 5, 40))
    aggregator.record(WorkflowOutcome(600, False, False, 12, 0))

    import json
    print(json.dumps(aggregator.report(), indent=2))
