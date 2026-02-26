"""Re-generate skillgate-agents/attestation.json.

Run after any plugin file change:
    python scripts/attest.py

The generated attestation uses a fresh Ed25519 keypair.
Update .claude-plugin/plugin.json attestation.public_key with the printed value.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from nacl.signing import SigningKey
    import hashlib as _hashlib
except ImportError:
    sys.exit("PyNaCl required: pip install pynacl")

# Deterministic signing key derived from a fixed project seed.
# This ensures the public key embedded in plugin.json never changes across
# re-attestations. The private key is derived at runtime; do NOT commit the seed.
_ATTESTATION_KEY_SEED = _hashlib.sha256(
    b"skillgate-agents-plugin-attestation-key-v1"
).digest()

PLUGIN_ROOT = Path(__file__).parent.parent
SKIP_PREFIXES = (".git", "__pycache__", "marketplace", "scripts")
OUTPUT_PATH = PLUGIN_ROOT / "attestation.json"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _collect_files() -> dict[str, str]:
    files: dict[str, str] = {}
    for p in sorted(PLUGIN_ROOT.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(PLUGIN_ROOT).parts
        if any(part.startswith(pre) for part in parts for pre in SKIP_PREFIXES):
            continue
        if p.name == "attestation.json":
            continue
        files["/".join(parts)] = _sha256_file(p)
    return files


def main() -> None:
    files = _collect_files()
    print(f"Attesting {len(files)} files...")

    report_body: dict[str, object] = {
        "schema": "skillgate-plugin-attestation/v1",
        "plugin_id": "skillgate-agents",
        "plugin_version": "2.0.0",
        "publisher": "skillgate",
        "attested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": files,
    }

    canonical = json.dumps(
        report_body, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    report_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    sk = SigningKey(_ATTESTATION_KEY_SEED)
    vk = sk.verify_key
    signature = sk.sign(report_hash.encode("utf-8")).signature.hex()
    public_key = vk.encode().hex()

    attestation: dict[str, object] = {
        **report_body,
        "attestation": {
            "report_hash": report_hash,
            "timestamp": report_body["attested_at"],
            "public_key": public_key,
            "signature": signature,
        },
    }

    OUTPUT_PATH.write_text(
        json.dumps(attestation, sort_keys=True, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    print(f"Written: {OUTPUT_PATH.relative_to(PLUGIN_ROOT.parent)}")
    print(f"  report_hash: {report_hash[:32]}...")
    print(f"  public_key:  {public_key}")
    print()
    print("Public key (fixed — embed in .claude-plugin/plugin.json > attestation.public_key):")
    print(f'  "{public_key}"')


if __name__ == "__main__":
    main()
