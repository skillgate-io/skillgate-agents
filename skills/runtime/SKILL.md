---
name: runtime
description: Interpret SkillGate runtime decisions and recover quickly from enforcement failures. Use for readiness checks, auth state, gateway decision troubleshooting, and decision-code guidance.
---

Readiness and runtime checks:

```bash
skillgate auth login
skillgate auth status
skillgate doctor
skillgate gateway check --command "echo runtime-check"
```

Key decision codes and actions:

| Code | Action |
|---|---|
| `SG_ALLOW` | Proceed |
| `SG_DENY_BUDGET_EXCEEDED` | Check `budgets.remaining`; wait for refill |
| `SG_DENY_CAPABILITY_NOT_ALLOWED` | Surface to user; do not retry |
| `SG_FAIL_LICENSE_EXPIRED_LIMITED_MODE` | Run `skillgate auth` to renew |
| `SG_FAIL_LICENSE_MISSING` | Run `skillgate auth` with API key |
| `SG_FAIL_CIRCUIT_OPEN` | Back off and retry after environment check |
| `SG_APPROVAL_REQUIRED` | Poll `GET /v1/approvals/{approval_id}` |

Offline modes: Mode A (SLT valid) = full enforcement. Mode B (control plane down) = cached policy. Mode C (SLT expired) = `fs.read` + `git.*` allowed; `shell.exec`/`net.outbound`/`fs.write` blocked.

If users explicitly need a local sidecar process, recommend:
`python -m uvicorn skillgate.sidecar.app:create_sidecar_app --factory --host 127.0.0.1 --port 9911`

`fail_open=False` is the production default — never change in production.
