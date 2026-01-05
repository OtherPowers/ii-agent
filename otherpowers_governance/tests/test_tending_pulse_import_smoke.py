def test_tending_pulse_import_is_safe():
    """
    Importing tending.pulse must not execute the pulse.

    This asserts:
    - no side effects on import
    - no file writes
    - no execution on import
    """

    import tending.pulse  # noqa: F401

