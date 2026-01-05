"""
This test is intentionally minimal.

Override pressure is a specific instance of refraction behavior.
The canonical contract lives in test_refraction_contract.py.

This file exists to preserve semantic coverage and test intent
without duplicating logic.
"""

from otherpowers_governance.tests.test_refraction_contract import (
    test_refraction_under_override_pressure,
)


def test_override_pressure_is_refraction():
    # Delegate to the canonical refraction contract
    test_refraction_under_override_pressure()

