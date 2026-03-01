# skillgate-agents

Protect Claude Code projects with practical, local-first security checks.

This plugin helps you catch risky instructions, unsafe hooks, and MCP governance drift before they turn into runtime incidents.

## Install

```bash
# Use for the current session
claude --plugin-dir ./skillgate-agents

# Or install from marketplace (when available)
/plugin install skillgate-agents
```

Requires [SkillGate CLI](https://skillgate.io):

```bash
pip install skillgate
skillgate auth login
skillgate sidecar start
skillgate doctor
```

## Quick start

Set identity context once per session so governance artifacts map cleanly to your workspace:

```bash
export SKILLGATE_ORG_ID=<org-id>
export SKILLGATE_WORKSPACE_ID=<workspace-id>
export SKILLGATE_ACTOR_ID=<actor-id-or-email>
```

Then run:

```bash
skillgate claude scan . --scope repo
```

## What users get

| Surface | Protection |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, memory, slash commands | Injection pattern detection before risky instructions spread |
| Claude hooks | Hook review, approval, and attestation workflow |
| MCP providers | Registry-based governance and settings drift checks |
| Plugin trust | Signed attestation verification and policy enforcement |
| Audit trail | Exportable decisions for review and compliance workflows |

## Slash commands

| Command | User outcome |
|---|---|
| `/skillgate-agents:secure-project` | Sets a baseline for scans, hooks, and governance files |
| `/skillgate-agents:audit` | Summarizes recent policy decisions and risks |
| `/skillgate-agents:scan-mcp` | Reviews MCP registration and trust posture |
| `/skillgate-agents:approve-hooks` | Walks through hook approval safely |
| `/skillgate-agents:check-injection` | Scans instruction surfaces for injection risk |
| `/skillgate-agents:enforce` | Verifies enforcement readiness and next actions |

## Model-invoked skills

Claude uses these skills automatically when relevant:

| Skill | Used for |
|---|---|
| `scan` | Security scan and policy enforcement flow |
| `runtime` | Runtime decisions, failure codes, and enforcement interpretation |
| `mcp` | MCP registry and provider governance |
| `claude` | Claude-specific hooks, settings, and surface scans |
| `codex` | Codex bridge workflows and preflight checks |
| `sdk` | Framework integration guidance |

## Automatic hooks

Hooks run checks around tool calls:

- Before `Bash`, `Write`, `Edit`, `NotebookEdit`, `WebFetch`, `WebSearch`, and `Task`
- After `Bash` output to scan returned content

Hooks degrade safely when dependencies are unavailable and keep normal development flow intact.
If the sidecar is not running, hooks fail open and your workflow continues in offline-safe mode.

## Verify plugin integrity

```bash
skillgate verify attestation.json
```

`Verification PASSED` confirms plugin files match the signed attestation.

## Requirements

- Claude Code 1.0.33+
- Python 3.12+
- SkillGate CLI installed and authenticated

## License

MIT. See [LICENSE](LICENSE).

## Links

- SkillGate docs: https://docs.skillgate.io
- Claude integration docs: https://docs.skillgate.io/integrations/claude-code
- GitHub: https://github.com/skillgate-io/skillgate-agents
