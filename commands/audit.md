Show a concise security audit summary users can read in under 30 seconds.

Default scope: current repo and last 7 days.

1. Run `skillgate export --format json --workspace <workspace-id> --from <yyyy-mm-dd>`.
2. Summarize:
   - Total decisions
   - ALLOW vs DENY
   - Top DENY codes with plain-language explanation
   - Most frequently blocked tool actions
3. Run `skillgate mcp audit` and show recent MCP decisions.
4. Run `skillgate claude hooks audit --directory . --limit 10`.
5. Run:
   - `skillgate claude ledger verify --scope repo --directory .`
   - `skillgate claude ledger tail --scope repo --directory . --limit 10`
6. Highlight urgent follow-up if:
   - DENY ratio is high
   - injection-related denies appear repeatedly
   - ledger verification fails

Output style:
- lead with user impact
- include exact commands used
- no unexplained internal jargon
