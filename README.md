# skillgate-agents

Runtime security for Claude Code. A Claude Code plugin that enforces capability policies, detects prompt injection across all attack surfaces, and produces signed audit records, all without leaving your editor.

## Install

```bash
# Load for the current session (development / trial)
claude --plugin-dir ./skillgate-agents

# Install from marketplace (once published)
/plugin install skillgate-agents
```

Requires [SkillGate CLI](https://skillgate.io):

```bash
pip install skillgate
skillgate auth
skillgate sidecar start
```

## What it covers

| Attack surface | Protection |
|---|---|
| MCP tool descriptions | Scans for injection before model exposure |
| `settings.json` | Detects permission expansion vs approved baseline |
| Plugins and skills | Blocks unattested plugins |
| PreToolUse / PostToolUse hooks | Scans commands against capability policy |
| `CLAUDE.md` / `AGENTS.md` | 30+ injection patterns blocked |
| Slash commands and memory files | Persistent injection path closed |
| Sub-agents (Task tool) | Budget circumvention impossible |

## Slash commands

| Command | What it does |
|---|---|
| `/skillgate-agents:secure-project` | Set up complete security baseline for this project |
| `/skillgate-agents:audit` | Show recent enforcement decisions and policy violations |
| `/skillgate-agents:scan-mcp` | Scan MCP servers for tool description poisoning and drift |
| `/skillgate-agents:approve-hooks` | Review and sign hooks against capability policy |
| `/skillgate-agents:check-injection` | Scan instruction files and slash commands for injection |
| `/skillgate-agents:enforce` | Start, verify, or troubleshoot the runtime sidecar |

## Skills (model-invoked)

Claude automatically uses these skills when relevant. No slash command needed:

| Skill | Triggers when you ask about |
|---|---|
| `scan` | Scanning skill bundles, CI enforcement, SARIF, attestation |
| `runtime` | Sidecar, SLT auth, decision codes, capability budgets |
| `mcp` | MCP servers, AI-BOM, tool poisoning, plugin attestation |
| `claude` | Hooks, CLAUDE.md injection, sub-agents, settings drift |
| `codex` | Codex CLI wrapping, AGENTS.md, CI guard mode |
| `sdk` | `@enforce` decorator, PydanticAI, LangChain, CrewAI |

## Automatic enforcement (hooks)

The plugin installs hooks that run SkillGate checks automatically. No explicit invocation needed:

- **Before every `Bash` call:** checks the command against capability policy
- **Before every `Write` / `Edit`:** checks the file path against `fs.write` policy
- **Before every `WebFetch` / `WebSearch`:** checks against `net.outbound` policy
- **Before every `Task`:** enforces sub-agent budget inheritance
- **After every `Bash` call:** scans output for exfiltration patterns

Hooks exit cleanly when the sidecar is not running. Enforcement is never a hard blocker in dev mode.

## Security agent

The **security-sentinel** agent (Sonnet 4.6) is available in `/agents`. It reviews actions, flags injection patterns, and returns structured verdicts: **SAFE / REVIEW REQUIRED / BLOCKED** with specific remediation commands.

## Plugin structure

```
skillgate-agents/
├── .claude-plugin/plugin.json    # Plugin manifest
├── commands/                     # 6 slash commands
├── skills/                       # 6 model-invoked skills
├── agents/security-sentinel.md  # Security review agent
└── hooks/hooks.json              # Automatic enforcement hooks
```

## Requirements

- Claude Code 1.0.33 or later
- SkillGate CLI: `pip install skillgate`
- Python 3.12+

Authentication required for runtime enforcement. Run `skillgate auth` once per session. Enforcement works offline using cached policy (see [offline modes](https://docs.skillgate.io/guides/offline)).

## Verify the plugin

The plugin ships with a signed attestation. Verify it has not been tampered with:

```bash
skillgate verify attestation.json
```

Output: `Verification PASSED` confirms the plugin content matches the signed record.

## License

MIT. See [LICENSE](LICENSE).

## Links

- SkillGate docs: https://docs.skillgate.io
- Claude Code plugin guide: https://docs.skillgate.io/guides/claude-code
- GitHub: https://github.com/skillgate-io/skillgate-agents
- Community: https://skillgate.io/community
