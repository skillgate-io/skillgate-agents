Validate enforcement readiness and help the user recover quickly if anything is missing.

Argument: action (`$ARGUMENTS`) can be `status` or empty.

1. Run `skillgate doctor --output json`.
2. Run `skillgate auth status`.
3. Run a fast runtime check:
   - `skillgate gateway check --command "echo skillgate-enforcement-check"`
4. If gateway output is blocked or errors:
   - explain the exact reason in plain language
   - suggest the next command (`skillgate auth login`, `skillgate keys list`, or policy fix)
5. If user asks for local sidecar startup guidance, provide this command:
   - `python -m uvicorn skillgate.sidecar.app:create_sidecar_app --factory --host 127.0.0.1 --port 9911`
6. Report a final one-line status:
   - `Enforcement readiness: READY`
   - or `Enforcement readiness: ACTION REQUIRED — <reason>`

Do not hide command errors. Show exact failing command + the user action to fix it.
