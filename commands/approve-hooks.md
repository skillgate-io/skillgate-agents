Review and approve Claude Code hooks in the current project. Argument: optional hook file path to review only that file (`$ARGUMENTS`).

1. **List hooks**: Run `skillgate claude hooks list`. Display all hooks with their current status:
   - `approved` — hook is signed and matches attestation
   - `unapproved` — hook exists but has not been approved
   - `changed` — hook was approved but has since been modified (blocked until re-approved)
   - `denied` — hook is explicitly blocked

2. **Assess each unapproved/changed hook**:
   - Read the hook file content
   - Run `skillgate gateway check --command "<hook-command>"` to preview the enforcement decision
   - Identify capabilities requested: shell.exec, net.outbound, fs.write, etc.
   - Assess risk:
     - **Low risk**: read-only operations, local file checks, linting
     - **Medium risk**: file writes, git operations
     - **High risk**: network calls, subprocess spawning, eval
     - **Critical**: `curl | sh`, `wget | bash`, `dd`, `rm -rf`, writing to PATH

3. **Present findings**: For each hook, show:
   - Purpose (inferred from content)
   - Capabilities requested
   - Risk level with explanation
   - Recommendation: approve / modify / deny

4. **Await confirmation**: Do not approve any hook without explicit user confirmation. Ask: "Approve hook at `<path>`? (yes/no/skip)"

5. **Approve confirmed hooks**: For each confirmed hook, run `skillgate claude hooks approve <path>`. Report the attestation record created.

6. **Summary**: Show final hook inventory: approved count, denied count, still-pending count.
