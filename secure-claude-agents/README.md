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
export SKILLGATE_ORG_ID=<org-id>
export SKILLGATE_WORKSPACE_ID=<workspace-id>
export SKILLGATE_ACTOR_ID=<actor-id-or-email>
skillgate mcp allow filesystem --endpoint http://127.0.0.1:8901 --checksum <sha256> --permissions fs.read,fs.write
skillgate mcp settings-check
skillgate claude policy-packs apply enterprise-ci --scope repo --directory .
skillgate claude behavior baseline --scope user --directory .
```
