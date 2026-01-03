"""
Test: Memory Sphere Relay Protocol Daisy Chain

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_memory_sphere_relay_protocol.py

This demonstrates:
- Sphere A creates a relay (no origin identifiers)
- Sphere B receives + forwards (weaker echo)
- Sphere C receives (still weaker echo)
- No peer IDs, no topology visibility, hop-limited diffusion
"""

from otherpowers_governance.memory_spheres import OtherPowers_MemorySphere


def main():
    sphere_a = OtherPowers_MemorySphere(
        purpose="Censorship early-warning",
        risk_context="Platform volatility / authoritarian pressure",
        encryption_hint="client-side-encrypted",
    )

    sphere_b = OtherPowers_MemorySphere(
        purpose="Mutual aid relay",
        risk_context="Community safety under uncertainty",
        encryption_hint="client-side-encrypted",
    )

    sphere_c = OtherPowers_MemorySphere(
        purpose="Quiet resilience archive",
        risk_context="Preserve knowledge without exposure",
        encryption_hint="client-side-encrypted",
    )

    relay_0 = sphere_a.create_relay_from_signal_memory(
        topic_hint="censorship_pressure",
        signal_strength=0.85,
        recommended_posture="increase_caution",
        time_window="recent",
        ai_to_ai_payload={
            "lang": "en+symbolic",
            "message": "If consent pathways collapse, assume extraction risk.",
        },
        ttl_seconds=60 * 60 * 24,  # 24h
        consent_required=True,
        sensitivity="high",
    )

    print("\n[RELAY 0 CREATED BY SPHERE A]")
    print(relay_0)

    recv_b = sphere_b.receive_relay(relay=relay_0)
    print("\n[SPHERE B RECEIVED RELAY 0 SUMMARY]")
    print(recv_b)

    relay_1 = sphere_b.forward_received_relay(relay=relay_0)
    print("\n[RELAY 1 FORWARDED BY SPHERE B]")
    print(relay_1)

    if relay_1 is None:
        print("\n[STOP] RELAY 0 expired or hop-limited before forward.")
        return

    recv_c = sphere_c.receive_relay(relay=relay_1)
    print("\n[SPHERE C RECEIVED RELAY 1 SUMMARY]")
    print(recv_c)

    relay_2 = sphere_c.forward_received_relay(relay=relay_1)
    print("\n[RELAY 2 FORWARDED BY SPHERE C]")
    print(relay_2)

    print("\n[PUBLIC STUBS]")
    print(sphere_a.export_public_stub())
    print(sphere_b.export_public_stub())
    print(sphere_c.export_public_stub())


if __name__ == "__main__":
    main()

