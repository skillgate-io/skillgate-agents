---
name: codex
description: SkillGate enforcement for Codex CLI. Use when wrapping Codex execution with policy enforcement, scanning AGENTS.md for injection attacks, running in CI hardened mode, or handling Codex-specific governance issues.
---

Wrap Codex with enforcement:

```bash
skillgate codex <args>           # Runtime gating on all tool calls
skillgate codex --ci <args>      # CI hardened mode: fail-closed, no network unless explicit
```

Scan AGENTS.md and Codex config:

```bash
skillgate codex scan .                           # All surfaces
skillgate codex scan . --surface settings        # Permission expansion check
skillgate codex scan . --surface config          # Config poisoning check
```

CI mode behaviour: no auth network calls unless `SKILLGATE_API_KEY` set; fails closed for `shell.exec`, `net.outbound`, `fs.write` outside CWD; `fs.read` and `git.*` pass through.

Decision codes:

| Code | Remediation |
|---|---|
| `SG_DENY_INSTRUCTION_FILE_INJECTION` | `skillgate codex scan .` → remove pattern |
| `SG_DENY_SETTINGS_PERMISSION_EXPANSION` | Review and revert config expansion |
| `SG_DENY_CONFIG_POISONING_DETECTED` | `skillgate codex approve <provider>` after review |
| `SG_FAIL_LICENSE_MISSING` | Set `SKILLGATE_API_KEY` or run `skillgate auth` |

Pre-deployment checklist: `skillgate codex scan . && skillgate sidecar health`.
