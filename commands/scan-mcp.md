Review MCP provider safety and registry health for this project.

Argument: optional server name (`$ARGUMENTS`) to focus the audit.

1. Discover configured MCP servers from project config files.
2. Run `skillgate mcp list` and map each configured server to registry status.
3. For each registered server, run `skillgate mcp inspect <server>` and summarize:
   - endpoint
   - trust level
   - checksum/version/publisher metadata
4. Run `skillgate mcp settings-check --ci` to detect permission expansion.
5. Run `skillgate mcp audit` and flag recent denied actions.
6. If a server is unregistered, explain the risk and provide a concrete allow command template:
   - `skillgate mcp allow <server> --endpoint <url> --checksum <sha256> --permissions <comma-list>`
7. End with:
   - per-server status (healthy / needs review / blocked)
   - one prioritized remediation list users can execute immediately
