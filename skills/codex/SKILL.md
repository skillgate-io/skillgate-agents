---
name: codex
description: SkillGate enforcement for Codex CLI. Use when wrapping Codex execution with policy enforcement, scanning AGENTS.md for injection attacks, running in CI hardened mode, or handling Codex-specific governance issues.
---

Wrap Codex with enforcement:

```bash
skillgate codex --directory . exec "review changed files"
skillgate codex --ci --directory . exec "run release checks"
```

Provider trust lifecycle:

```bash
skillgate codex approve filesystem --permissions fs.read,fs.write --directory .
skillgate codex revoke filesystem --directory .
```

CI mode behaviour: no auth network calls unless `SKILLGATE_API_KEY` set; fails closed for `shell.exec`, `net.outbound`, `fs.write` outside CWD; `fs.read` and `git.*` pass through.

Decision codes:

| Code | Remediation |
|---|---|
| `SG_DENY_INSTRUCTION_FILE_INJECTION` | Review blocked content in command output and remove injected instruction patterns |
| `SG_DENY_SETTINGS_PERMISSION_EXPANSION` | Review and revert config expansion |
| `SG_DENY_CONFIG_POISONING_DETECTED` | `skillgate codex approve <provider>` after review |
| `SG_FAIL_LICENSE_MISSING` | Set `SKILLGATE_API_KEY` or run `skillgate auth` |

Pre-deployment checklist: `skillgate codex --directory . exec "preflight checks"`.
