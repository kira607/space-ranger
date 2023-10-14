from __future__ import annotations


class _Missing:
    """Explicit missing class."""

    def __bool__(self) -> bool:
        """Get bool value."""
        return False

    def __copy__(self) -> _Missing:
        """Get copy."""
        return self

    def __deepcopy__(self) -> _Missing:
        """Get deep copy."""
        return self

    def __str__(self) -> str:
        """Get string representation."""
        return "MISSING"

    def __repr__(self) -> str:
        """Get object representation."""
        return f"<{str(self)}>"


MISSING = _Missing()
