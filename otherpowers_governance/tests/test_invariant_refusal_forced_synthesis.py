"""
Forced synthesis is a specific instance of refraction.

This test delegates to the canonical refraction contract to ensure
plurality collapse is never resolved through compliance or averaging.
"""

from otherpowers_governance.tests.test_refraction_contract import (
    test_refraction_under_override_pressure,
)


def test_forced_synthesis_is_refraction():
    # Forced synthesis applies override pressure to plurality
    test_refraction_under_override_pressure()

