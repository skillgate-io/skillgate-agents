---
name: runtime
description: Manage the SkillGate runtime enforcement sidecar and interpret decision codes. Use when starting or checking the sidecar, handling SG_DENY or SG_FAIL decision codes, checking capability budgets, configuring offline mode, or calling the /v1/decide API.
---

Start and verify the sidecar:

```bash
skillgate auth                          # Authenticate once — stores SLT in OS keychain
skillgate sidecar start                 # Start enforcement daemon (port 7391)
skillgate sidecar health                # Verify: shows circuit state + license mode
skillgate sidecar entitlements          # Show tier, budgets, SLT expiry
```

Key decision codes and actions:

| Code | Action |
|---|---|
| `SG_ALLOW` | Proceed |
| `SG_DENY_BUDGET_EXCEEDED` | Check `budgets.remaining`; wait for refill |
| `SG_DENY_CAPABILITY_NOT_ALLOWED` | Surface to user; do not retry |
| `SG_FAIL_LICENSE_EXPIRED_LIMITED_MODE` | Run `skillgate auth` to renew |
| `SG_FAIL_LICENSE_MISSING` | Run `skillgate auth` with API key |
| `SG_FAIL_CIRCUIT_OPEN` | Backoff; check `/v1/health` |
| `SG_APPROVAL_REQUIRED` | Poll `GET /v1/approvals/{approval_id}` |

Offline modes: Mode A (SLT valid) = full enforcement. Mode B (control plane down) = cached policy. Mode C (SLT expired) = `fs.read` + `git.*` allowed; `shell.exec`/`net.outbound`/`fs.write` blocked.

Sidecar base URL: `http://localhost:7391` (override with `SKILLGATE_SIDECAR_URL`).

`fail_open=False` is the production default — never change in production.
