"""E2E validation for scope-hardening guidance in plugin commands/docs."""

from __future__ import annotations

import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent


def _must_contain(path: Path, text: str) -> str | None:
    content = path.read_text(encoding="utf-8")
    if text not in content:
        return f"{path.relative_to(PLUGIN_ROOT)} missing required text: {text}"
    return None


def main() -> None:
    checks: list[tuple[str, str]] = [
        ("README.md", "SKILLGATE_ORG_ID"),
        ("README.md", "SKILLGATE_WORKSPACE_ID"),
        ("README.md", "SKILLGATE_ACTOR_ID"),
        ("commands/secure-project.md", "skillgate claude scan . --scope repo"),
        ("commands/secure-project.md", "skillgate claude behavior baseline --scope user"),
        ("commands/check-injection.md", "--scope repo"),
        ("commands/audit.md", "skillgate claude ledger verify --scope repo"),
        ("skills/claude/SKILL.md", "skillgate claude scan . --scope repo"),
        ("skills/claude/SKILL.md", "skillgate claude policy-packs apply enterprise-ci --scope repo"),
    ]

    failures: list[str] = []
    for rel, needle in checks:
        error = _must_contain(PLUGIN_ROOT / rel, needle)
        if error:
            failures.append(error)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: scope-hardening e2e checks passed ({len(checks)} assertions)")


if __name__ == "__main__":
    main()
