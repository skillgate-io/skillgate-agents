---
name: scan
description: Scan agent skill bundles, code, or project directories for security risks using SkillGate static analysis. Use when asked to scan for vulnerabilities, check a skill before publishing, run a security audit in CI, generate SARIF output, or sign scan results for compliance.
---

Run SkillGate static analysis on the target path. Core commands:

```bash
# Standard scan with human output
skillgate scan <path>

# CI enforcement (exit 1 on violation)
skillgate scan <path> --enforce --policy production

# SARIF for GitHub Security tab
skillgate scan <path> --output sarif > results.sarif

# Signed attestation for compliance
skillgate scan <path> --sign --report-file attestation.json

# Verify a signed report
skillgate verify attestation.json
```

First-time reputation setup (optional, recommended):

```bash
skillgate reputation init --store .skillgate/reputation/reputation.json
skillgate scan <path> --reputation-store .skillgate/reputation/reputation.json
```

Policy presets: `development` (permissive) → `staging` → `production` (recommended for CI) → `strict` (maximum).

Exit codes: 0=clean, 1=policy violation, 2=internal error, 3=invalid input.

Treat exit 1 as a hard stop in CI. Never suppress with `|| true`.

Detection categories: SG-SHELL (injection), SG-NET (exfiltration), SG-FS (path traversal), SG-EVAL (dynamic exec), SG-CRED (leaked credentials), SG-INJ (prompt injection), SG-OBF (obfuscation).

Custom policy override: create `skillgate.yml` in project root with `version: "1"` and `policy.preset`.
