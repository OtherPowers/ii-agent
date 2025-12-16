"""
Test: Capability tokens + encrypted offline bundle export/import (v2)

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_memory_sphere_offline_bundle.py
"""

from otherpowers_governance.memory_spheres import (
    OtherPowers_MemorySphere,
    new_capability,
    verify_capability,
    export_encrypted_bundle_v2,
    import_encrypted_bundle_v2,
)

def main():
    # Capability key should be kept offline; treat as secret
    secret_key = b"REPLACE_ME_WITH_32+_BYTES_RANDOM_IN_REAL_USE"

    cap = new_capability(
        secret_key=secret_key,
        rules={
            "ttl_seconds": 60 * 60 * 24 * 3,  # 3 days
            "max_forwards": 2,
            "allow_receive": True,
            "allow_forward": True,
            "allow_project": False,
            "sensitivity_ceiling": "high",
        },
    )

    print("\n[CAPABILITY TOKEN]")
    print(cap)

    ok = verify_capability(token=cap, secret_key=secret_key)
    print("\n[CAPABILITY VERIFIED]")
    print(ok)

    sphere = OtherPowers_MemorySphere(
        purpose="Offline resilience bundle",
        risk_context="Censorship risk / platform collapse",
        encryption_hint="client-side-encrypted",
    )

    sphere.add_entry(
        content={"type": "joy", "note": "Mutual aid: share food, share warmth, share dignity."},
        sensitivity="high",
        consent_required=True,
    )

    export_data = sphere.export_full()

    passphrase = "REPLACE_ME_WITH_A_STRONG_PASSPHRASE"
    out_path = "audit_logs/memory_spheres/sphere_bundle_test.opms"

    fp = export_encrypted_bundle_v2(
        sphere_export=export_data,
        out_path=out_path,
        passphrase=passphrase,
        label="otherpowers_memory_sphere",
    )

    print("\n[ENCRYPTED BUNDLE WRITTEN]")
    print(fp)

    payload = import_encrypted_bundle_v2(
        in_path=fp,
        passphrase=passphrase,
        label="otherpowers_memory_sphere",
    )

    print("\n[DECRYPTED PAYLOAD METADATA]")
    print({k: payload.get(k) for k in ["type", "created_at_unix", "format_version"]})

    data = payload.get("data", {})
    print("\n[DECRYPTED SPHERE STUB]")
    print({
        "sphere_id": data.get("sphere_id"),
        "purpose": data.get("purpose"),
        "entry_count": len(data.get("entries", [])),
    })

if __name__ == "__main__":
    main()

