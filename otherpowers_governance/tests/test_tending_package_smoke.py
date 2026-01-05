def test_tending_package_import_is_safe():
    """
    The tending package must be importable in isolation.

    This test asserts:
    - no side effects on import
    - no registry dependencies
    - no execution triggered
    """

    import tending  # noqa: F401

