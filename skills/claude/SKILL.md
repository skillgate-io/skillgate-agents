---
name: claude
description: Full-surface security governance for Claude Code. Use when scanning CLAUDE.md or AGENTS.md for injection, reviewing hooks for unsafe commands, auditing slash commands or memory files, enforcing sub-agent budget limits, checking settings drift, or handling any Claude Code governance decision code.
---

Full surface scan (runs all checks):

```bash
skillgate claude scan .
```

Surface-specific commands:

```bash
# Hooks
skillgate claude hooks list                    # Status: approved / unapproved / changed
skillgate claude hooks approve <file>          # Sign and approve a hook
skillgate claude hooks audit                   # Recent hook executions

# Instruction files (CLAUDE.md, AGENTS.md)
skillgate claude scan . --surface instruction-files

# Slash commands + memory
skillgate claude scan . --surface slash-commands,memory

# Settings drift
skillgate claude settings drift                # Compare vs approved baseline

# Sub-agent lineage
skillgate claude agents lineage <invocation-id>
```

Decision codes:

| Code | Surface | Remediation |
|---|---|---|
| `SG_DENY_HOOK_COMMAND_UNSAFE` | Hook | Reduce capabilities; re-approve |
| `SG_DENY_INSTRUCTION_FILE_INJECTION` | CLAUDE.md / AGENTS.md / memory | Remove pattern or report FP |
| `SG_DENY_SLASH_COMMAND_INJECTION` | `.claude/commands/` | Remove injection from command |
| `SG_DENY_SETTINGS_PERMISSION_EXPANSION` | `settings.json` | Revert expansion |
| `SG_DENY_SUBAGENT_BUDGET_EXCEEDED` | Task tool | Reduce sub-agent scope |

Sub-agent rule: child agents inherit parent's **remaining** budget, not the full tier budget. Budget circumvention via Task tool spawning is blocked.
