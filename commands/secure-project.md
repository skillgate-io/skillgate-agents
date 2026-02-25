Set up a complete SkillGate security baseline for the current project. Run the following steps in sequence and report results for each:

1. **Verify installation**: Run `skillgate --version` to confirm SkillGate is installed. If not installed, instruct the user to run `pip install skillgate`.

2. **Authenticate**: Run `skillgate sidecar health` to check if the sidecar is running. If not, run `skillgate auth` to authenticate (prompt user for API key if `SKILLGATE_API_KEY` is not set), then `skillgate sidecar start`.

3. **Scan the project**: Run `skillgate claude scan .` to audit all Claude Code attack surfaces. Report findings grouped by surface: hooks, instruction files (CLAUDE.md/AGENTS.md), slash commands, memory files, settings.json.

4. **Register MCP servers**: Run `skillgate mcp list` to show registered servers. For any MCP servers found in `.mcp.json` or `settings.json` that are not registered, run `skillgate mcp allow <server-name>` for each and confirm with the user first.

5. **Approve hooks**: Run `skillgate claude hooks list`. For any unapproved hooks, show the user the hook content, explain the capabilities it requests, and ask for confirmation before running `skillgate claude hooks approve <file>`.

6. **Create policy file**: If no `skillgate.yml` exists in the project root, create one with the production preset:

```yaml
version: "1"
policy:
  preset: production
  plugin_policy: strict
  memory_policy: strict
```

7. **Report**: Summarise what was secured, what requires follow-up, and print the command to verify the full baseline: `skillgate claude scan . && skillgate sidecar health`.

If any step fails, explain the error and the remediation without retrying automatically.
