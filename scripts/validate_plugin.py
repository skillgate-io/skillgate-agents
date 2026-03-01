"""Plugin structure validation script for CI and local use.

Usage:
    python scripts/validate_plugin.py [check]

Checks: manifest, skills, commands, hooks, agent, frontmatter, readme, all
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent


def check_manifest() -> list[str]:
    errors: list[str] = []
    path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    if not path.exists():
        return ["plugin.json: file not found"]
    try:
        manifest = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"plugin.json: invalid JSON — {e}"]
    required = [
        "name", "version", "description", "author",
        "license", "skills", "commands", "agents", "hooks",
    ]
    for field in required:
        if field not in manifest:
            errors.append(f"plugin.json: missing field '{field}'")
    print(f"OK: plugin.json — {manifest.get('name', '?')} v{manifest.get('version', '?')}")
    return errors


def check_skills() -> list[str]:
    errors: list[str] = []
    required = ["scan", "runtime", "mcp", "claude", "codex", "sdk"]
    for name in required:
        skill_file = PLUGIN_ROOT / "skills" / name / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"skills/{name}/SKILL.md: missing")
    if not errors:
        print(f"OK: all {len(required)} skills present")
    return errors


def check_commands() -> list[str]:
    errors: list[str] = []
    required = [
        "secure-project", "audit", "scan-mcp",
        "approve-hooks", "check-injection", "enforce",
    ]
    for name in required:
        cmd_file = PLUGIN_ROOT / "commands" / f"{name}.md"
        if not cmd_file.exists():
            errors.append(f"commands/{name}.md: missing")
    if not errors:
        print(f"OK: all {len(required)} commands present")
    return errors


def check_hooks() -> list[str]:
    errors: list[str] = []
    path = PLUGIN_ROOT / "hooks" / "hooks.json"
    if not path.exists():
        return ["hooks/hooks.json: file not found"]
    try:
        hooks_data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"hooks/hooks.json: invalid JSON — {e}"]
    pre = hooks_data.get("hooks", {}).get("PreToolUse", [])
    matchers = {h.get("matcher", "") for h in pre}
    required_matchers = {
        "Bash", "Write|Edit|NotebookEdit", "WebFetch|WebSearch", "Task",
    }
    for m in required_matchers:
        if m not in matchers:
            errors.append(f"hooks.json: PreToolUse missing matcher '{m}'")
    if not errors:
        pre_commands: list[str] = []
        for entry in pre:
            for hook in entry.get("hooks", []):
                if isinstance(hook, dict):
                    command = hook.get("command")
                    if isinstance(command, str):
                        pre_commands.append(command)

        post = hooks_data.get("hooks", {}).get("PostToolUse", [])
        post_commands: list[str] = []
        for entry in post:
            for hook in entry.get("hooks", []):
                if isinstance(hook, dict):
                    command = hook.get("command")
                    if isinstance(command, str):
                        post_commands.append(command)

        if not pre_commands or not all("skillgate gateway check --command" in cmd for cmd in pre_commands):
            errors.append("hooks.json: PreToolUse commands must use 'skillgate gateway check --command'")
        if not post_commands or not all("skillgate gateway scan-output --output-text" in cmd for cmd in post_commands):
            errors.append(
                "hooks.json: PostToolUse commands must use 'skillgate gateway scan-output --output-text'"
            )

    if not errors:
        print(f"OK: hooks valid — {len(pre)} PreToolUse hooks")
    return errors


def check_agent() -> list[str]:
    errors: list[str] = []
    agent_path = PLUGIN_ROOT / "agents" / "security-sentinel.md"
    if not agent_path.exists():
        return ["agents/security-sentinel.md: file not found"]
    content = agent_path.read_text()
    for keyword in ["SAFE", "REVIEW REQUIRED", "BLOCKED", "model:"]:
        if keyword not in content:
            errors.append(f"security-sentinel.md: missing keyword '{keyword}'")
    if not errors:
        print("OK: security-sentinel agent valid")
    return errors


def check_frontmatter() -> list[str]:
    errors: list[str] = []
    for skill_file in sorted((PLUGIN_ROOT / "skills").rglob("SKILL.md")):
        content = skill_file.read_text()
        rel = skill_file.relative_to(PLUGIN_ROOT)
        if not content.startswith("---"):
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        try:
            fm_end = content.index("---", 3)
        except ValueError:
            errors.append(f"{rel}: frontmatter not closed")
            continue
        fm = content[3:fm_end]
        for field in ["name:", "description:"]:
            if field not in fm:
                errors.append(f"{rel}: frontmatter missing '{field}'")
    if not errors:
        print("OK: all skill frontmatter valid")
    return errors


def check_readme() -> list[str]:
    errors: list[str] = []
    readme = PLUGIN_ROOT / "README.md"
    if not readme.exists():
        return ["README.md: file not found"]
    content = readme.read_text()
    required_strings = [
        "pip install skillgate",
        "skillgate auth login",
        "skillgate doctor",
        "/skillgate-agents:secure-project",
        "/skillgate-agents:audit",
        "/skillgate-agents:scan-mcp",
        "/skillgate-agents:approve-hooks",
        "/skillgate-agents:check-injection",
        "/skillgate-agents:enforce",
    ]
    for s in required_strings:
        if s not in content:
            errors.append(f"README.md: missing '{s}'")
    if not errors:
        print("OK: README complete")
    return errors


CHECKS = {
    "manifest": check_manifest,
    "skills": check_skills,
    "commands": check_commands,
    "hooks": check_hooks,
    "agent": check_agent,
    "frontmatter": check_frontmatter,
    "readme": check_readme,
}


def main() -> None:
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        checks = list(CHECKS.values())
    elif target in CHECKS:
        checks = [CHECKS[target]]
    else:
        print(f"Unknown check '{target}'. Available: {', '.join(CHECKS)} all", file=sys.stderr)
        sys.exit(3)

    all_errors: list[str] = []
    for check_fn in checks:
        all_errors.extend(check_fn())

    if all_errors:
        for err in all_errors:
            print(f"FAIL: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
