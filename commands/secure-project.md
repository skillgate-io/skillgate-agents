Set up a complete project baseline with user-friendly, low-friction steps.

1. Verify CLI availability:
   - `skillgate version`
   - If missing, tell user to install SkillGate first.

2. Verify auth and environment readiness:
   - `skillgate auth status`
   - `skillgate doctor`

3. Confirm identity context is present:
   - `SKILLGATE_ORG_ID`
   - `SKILLGATE_WORKSPACE_ID`
   - `SKILLGATE_ACTOR_ID`

4. Run full Claude ecosystem scan:
   - `skillgate claude scan . --scope repo --surface all`
   - Group findings by surface in your report.

5. Review MCP status:
   - `skillgate mcp list`
   - For unregistered servers, explain exactly what info is needed for registration:
     - endpoint
     - checksum
     - permissions
   - Command template:
     - `skillgate mcp allow <server> --endpoint <url> --checksum <sha256> --permissions <comma-list>`

6. Review and approve hooks:
   - `skillgate claude hooks list --directory .`
   - For each unapproved/changed hook, show risk and request explicit approval before:
     - `skillgate claude hooks approve <file> --directory .`

7. Initialize policy if missing:
   - `skillgate init --preset production`

8. Create governance baselines:
   - `skillgate claude behavior baseline --scope user --directory .`
   - `skillgate claude approvals baseline --scope repo --directory .`
   - `skillgate claude policy-packs apply enterprise-ci --scope repo --directory .`

9. Final verification command:
   - `skillgate claude scan . --scope repo --surface all`

If any command fails, show the exact command + error, and provide one clear next action.
