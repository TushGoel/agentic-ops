# Examples

One runnable file per principle from the [top-level README](../README.md). No AWS account, no dependencies beyond the Python 3.9+ standard library.

```bash
python3 01_durable_execution.py
python3 02_governed_tool_gateway.py
python3 03_workflow_router.py
python3 04_structured_knowledge_lookup.py
python3 05_decoupled_ingestion.py
python3 06_quality_gated_learning.py
python3 07_blast_radius_guard.py
python3 08_observability_signals.py
```

| File | Principle |
|------|-----------|
| [`01_durable_execution.py`](01_durable_execution.py) | Durable execution beats a custom retry loop |
| [`02_governed_tool_gateway.py`](02_governed_tool_gateway.py) | Every tool call goes through a governed gateway |
| [`03_workflow_router.py`](03_workflow_router.py) | Route by workflow shape, not one generic pipeline |
| [`04_structured_knowledge_lookup.py`](04_structured_knowledge_lookup.py) | Pick storage for your data shape, not by default |
| [`05_decoupled_ingestion.py`](05_decoupled_ingestion.py) | Decouple ingestion from processing |
| [`06_quality_gated_learning.py`](06_quality_gated_learning.py) | Gate the learning loop on confirmed outcomes |
| [`07_blast_radius_guard.py`](07_blast_radius_guard.py) | Make unsafe actions structurally unavailable |
| [`08_observability_signals.py`](08_observability_signals.py) | Instrument three signal types from day one |
