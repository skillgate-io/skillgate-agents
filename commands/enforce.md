Start, verify, or troubleshoot the SkillGate runtime enforcement sidecar. Argument: action — `start`, `stop`, `restart`, `status`, or empty for smart start (`$ARGUMENTS`).

**Smart start (no argument or "start")**:

1. Run `skillgate sidecar health`. If sidecar is already running and healthy, report "Sidecar is running — enforcement active" and show current entitlements summary.

2. If not running:
   a. Check authentication: run `skillgate sidecar entitlements`. If it fails with `SG_FAIL_LICENSE_MISSING`, instruct the user to run `skillgate auth` (do not attempt auth automatically — it requires API key input).
   b. Start the sidecar: run `skillgate sidecar start`.
   c. Verify: run `skillgate sidecar health` again. Report success or failure with the exact error message.

3. Show entitlements: run `skillgate sidecar entitlements` and display:
   - License tier and mode (online / offline / limited)
   - SLT expiry
   - Capability budgets: shell.exec, net.outbound, fs.write (limit and remaining)
   - Policy preset active

**"stop"**: Run `skillgate sidecar stop`. Confirm stopped with health check.

**"restart"**: Stop then start. Show final health status.

**"status"**: Run `skillgate sidecar health` and `skillgate sidecar entitlements`. Display full status.

**Troubleshooting if sidecar fails to start**:
- Port conflict (7391): suggest `skillgate sidecar start --port 7392` and setting `SKILLGATE_SIDECAR_URL=http://localhost:7392`
- License error: instruct `skillgate auth` with API key
- Policy unavailable: instruct `skillgate auth` to refresh policy cache
- Any other error: show exact error text and link to https://docs.skillgate.io/troubleshooting

Report final state clearly: "Enforcement is ACTIVE" or "Enforcement is INACTIVE — reason: <explanation>".
