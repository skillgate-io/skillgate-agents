# secure-claude-agents

Reference blueprint for running Claude Code with SkillGate MCP governance.

## Security guarantees

- Unknown MCP servers blocked by default.
- Tool description poisoning blocked (`SG_DENY_TOOL_DESCRIPTION_INJECTION`).
- Claude settings drift blocked (`SG_DENY_SETTINGS_PERMISSION_EXPANSION`).
- Unattested plugins blocked in CI (`SG_DENY_PLUGIN_NOT_ATTESTED`).
- Combined escalation (`fs.write + git.write + shell.exec`) blocked.

## Quick start

```bash
skillgate mcp allow filesystem --endpoint http://127.0.0.1:8901 --checksum <sha256> --permissions fs.read,fs.write
skillgate mcp settings-check
```
