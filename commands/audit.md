Show a concise audit summary of recent SkillGate enforcement decisions. Run `$ARGUMENTS` as the time window if provided (e.g., "1h", "24h", "7d"), otherwise default to the last 24 hours.

1. **Check sidecar**: Run `skillgate sidecar health`. If the sidecar is not running, report "Sidecar not running — decisions from last session only" and continue with available data.

2. **Recent decisions**: Run `skillgate export --format json --from <window>` to get recent decisions. Display a summary table:
   - Total decisions
   - ALLOW count vs DENY count
   - DENY breakdown by decision code
   - Top 5 most-blocked tools or capabilities

3. **MCP audit**: Run `skillgate mcp audit` and show the last 10 MCP tool decisions. Flag any `SG_DENY_TOOL_DESCRIPTION_INJECTION` or `SG_DENY_PLUGIN_NOT_ATTESTED` findings.

4. **Hook audit**: Run `skillgate claude hooks audit` and show the last 10 hook executions. Flag any blocked hooks.

5. **Pending approvals**: Run `skillgate sidecar entitlements` and check for pending approvals. If any exist, list them with their `approval_id` and required capabilities.

6. **Risk summary**: If any DENY rate exceeds 10% in the window, or any critical decision codes appear (`SG_DENY_INSTRUCTION_FILE_INJECTION`, `SG_DENY_TOOL_DESCRIPTION_INJECTION`), flag these prominently as requiring investigation.

Format the output as a clear summary the user can scan in 30 seconds. Use plain language — no internal codes without explanation.
