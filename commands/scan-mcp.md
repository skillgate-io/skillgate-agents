Scan all MCP servers configured for this project for security threats. Argument: optional server name to scan only that server (`$ARGUMENTS`).

1. **Discover servers**: Read `.mcp.json` and `.claude/settings.json` to find all configured MCP servers. If `$ARGUMENTS` is provided, filter to only that server.

2. **Registration check**: Run `skillgate mcp list` to see registered servers. For each configured server, report:
   - Registered / Not registered
   - Trust level (unverified / community / verified / official)
   - Last attestation date

3. **Tool description scan**: For each registered server, run `skillgate mcp inspect <server> --check-injection`. Report findings:
   - Clean: no injection patterns found
   - Suspicious: list the specific tool name, field (name/description/inputSchema), and pattern matched

   For any `SG_DENY_TOOL_DESCRIPTION_INJECTION` findings, show the exact text that triggered the detection and explain why it is dangerous.

4. **Permission drift**: For each server with an AI-BOM, run `skillgate mcp inspect <server> --drift-check`. Report any capabilities present in the live server that are not in the registered AI-BOM.

5. **Unregistered servers**: For any server found in config files but not in the SkillGate registry, warn the user clearly: "This server is not registered with SkillGate — its tool descriptions have not been scanned and it has no AI-BOM. Run `skillgate mcp allow <server>` to register it after reviewing its source."

6. **Summary**: Print a pass/fail verdict per server and a single overall verdict. Exit with a clear remediation list if any issues found.
