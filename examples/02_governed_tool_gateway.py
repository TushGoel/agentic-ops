"""
Principle 2: Every tool call goes through a governed gateway, not a direct API call.

An LLM that calls APIs directly has no enforcement point between "the model
decided to do X" and "X happened." This gateway is that enforcement point:
every call is checked against a permission set and a risk level before it
runs, and every call - permitted or denied - is written to an audit trail.

Run: python3 02_governed_tool_gateway.py
"""
from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    risk: str  # LOW, MEDIUM, HIGH
    required_permission: str


class PermissionDenied(Exception):
    pass


class ConfirmationRequired(Exception):
    pass


class ToolGateway:
    def __init__(self, agent_permissions: set[str]):
        self.agent_permissions = agent_permissions
        self.audit_log: list[dict] = []

    def call(self, tool: ToolSpec, args: dict, confirmed: bool = False):
        entry = {"tool": tool.name, "args": args, "risk": tool.risk}
        try:
            if tool.required_permission not in self.agent_permissions:
                entry["result"] = "DENIED_NO_PERMISSION"
                raise PermissionDenied(f"agent lacks '{tool.required_permission}' for '{tool.name}'")
            if tool.risk == "HIGH" and not confirmed:
                entry["result"] = "DENIED_NEEDS_CONFIRMATION"
                raise ConfirmationRequired(f"'{tool.name}' is HIGH risk and requires confirmed=True")
            entry["result"] = "EXECUTED"
            return f"executed {tool.name}({args})"
        finally:
            self.audit_log.append(entry)


if __name__ == "__main__":
    gateway = ToolGateway(agent_permissions={"read_logs", "create_ticket"})

    get_logs = ToolSpec("get_logs", risk="LOW", required_permission="read_logs")
    print(gateway.call(get_logs, {"deployment_id": "d-123"}))

    rollback = ToolSpec("rollback_deployment", risk="HIGH", required_permission="deploy_write")
    try:
        gateway.call(rollback, {"deployment_id": "d-123"})
    except (PermissionDenied, ConfirmationRequired) as e:
        print(f"blocked: {e}")

    print("audit trail:", gateway.audit_log)
