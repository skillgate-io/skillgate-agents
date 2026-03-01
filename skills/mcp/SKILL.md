---
name: mcp
description: Manage MCP provider governance with SkillGate. Use for registration, inspection, settings drift checks, attestation verification, and audit review.
---

MCP server management:

```bash
skillgate mcp list
skillgate mcp allow <server> --endpoint <url> --checksum <sha256> --permissions <comma-list>
skillgate mcp deny <server>
skillgate mcp inspect <server>
skillgate mcp settings-check --ci
skillgate mcp attest <plugin-file>
skillgate mcp verify <plugin-file>
skillgate mcp audit
```

Tool description poisoning — fields scanned before model exposure: `tool.name`, `tool.description`, `tool.inputSchema` property descriptions.

MCP decision codes:

| Code | Remediation |
|---|---|
| `SG_DENY_UNTRUSTED_TOOL_PROVIDER` | `skillgate mcp allow <server>` |
| `SG_DENY_TOOL_DESCRIPTION_INJECTION` | Remove injection; report false positive if needed |
| `SG_DENY_PLUGIN_NOT_ATTESTED` | `skillgate mcp attest <plugin>` |
| `SG_DENY_SETTINGS_PERMISSION_EXPANSION` | Run `skillgate mcp settings-check --ci` and revert expansion |

Unknown MCP servers are blocked by default — explicit `skillgate mcp allow` required.
