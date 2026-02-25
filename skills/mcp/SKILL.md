---
name: mcp
description: Manage MCP server security with SkillGate. Use when registering or blocking MCP servers, scanning tool descriptions for injection attacks, checking AI-BOM compliance, attesting plugins, detecting permission drift, or handling MCP-related decision codes.
---

MCP server management:

```bash
skillgate mcp list                         # All servers + AI-BOM + trust level
skillgate mcp allow <server>               # Register server (required before use)
skillgate mcp deny <server>                # Block server
skillgate mcp inspect <server>             # Full AI-BOM + permissions
skillgate mcp inspect <server> --check-injection   # Scan tool descriptions for injection
skillgate mcp inspect <server> --drift-check       # Compare live permissions vs AI-BOM
skillgate mcp attest <plugin>              # Sign plugin with Ed25519
skillgate mcp audit                        # Recent tool decisions
```

Tool description poisoning — fields scanned before model exposure: `tool.name`, `tool.description`, `tool.inputSchema` property descriptions.

MCP decision codes:

| Code | Remediation |
|---|---|
| `SG_DENY_UNTRUSTED_TOOL_PROVIDER` | `skillgate mcp allow <server>` |
| `SG_DENY_TOOL_DESCRIPTION_INJECTION` | Remove injection; report false positive if needed |
| `SG_DENY_PLUGIN_NOT_ATTESTED` | `skillgate mcp attest <plugin>` |
| `SG_DENY_CONFIG_POISONING_DETECTED` | `skillgate codex approve <provider>` after review |

Unknown MCP servers are blocked by default — explicit `skillgate mcp allow` required.
