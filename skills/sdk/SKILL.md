---
name: sdk
description: Integrate SkillGate runtime enforcement into Python agent frameworks. Use when adding the @enforce decorator to agent tools, integrating with PydanticAI, LangChain, or CrewAI, handling CapabilityDeniedError or ApprovalPendingError, or calling the /v1/decide sidecar API directly.
---

`@enforce` decorator (zero-config):

```python
from skillgate.sdk import enforce, enforce_async
from skillgate.sdk.errors import CapabilityDeniedError, ApprovalPendingError

@enforce(capabilities=["fs.read", "shell.exec"])
def my_tool(path: str) -> str: ...

@enforce_async(capabilities=["net.outbound"])
async def fetch(url: str) -> str: ...

try:
    result = my_tool("/tmp/data.txt")
except CapabilityDeniedError as e:
    # e.decision_code, e.reason_codes, e.budgets
    print(f"Blocked: {e.decision_code}")
except ApprovalPendingError as e:
    print(f"Approval required: {e.approval_id}")
```

Framework integrations:

```python
# PydanticAI
from skillgate.integrations.pydantic_ai import skillgate_wrapped
agent = Agent("claude-sonnet-4-6", tools=[skillgate_wrapped(my_tool, capabilities=["shell.exec"])])

# LangChain
from skillgate.integrations.langchain import SkillGateTool
class ShellTool(SkillGateTool):
    name = "shell_executor"
    capabilities = ["shell.exec"]
    def _run(self, command: str) -> str: ...

# CrewAI
from skillgate.integrations.crewai import skillgate_tool
@skillgate_tool(capabilities=["fs.read"])
def read_file(path: str) -> str: ...
```

Key rule: `fail_open=False` is the production default. Never use `fail_open=True` outside dev policy iteration.

Capabilities: `fs.read`, `fs.write`, `shell.exec`, `net.outbound`, `git.*`, `env.read`.
