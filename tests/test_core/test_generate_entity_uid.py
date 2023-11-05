from space_ranger.core.entity import generate_entity_uid


def test_returns_unique_string_each_time() -> None:
    """Test that `generate_entity_uid()` returns a unique string each time it is called."""
    uid1 = generate_entity_uid()
    uid2 = generate_entity_uid()
    assert uid1 != uid2


def test_generate_unique_values_with_high_calls_count() -> None:
    """Test that `generate_entity_uid()` generates unique values for high amount of calls."""
    num = 10000
    uids = {generate_entity_uid() for _ in range(num)}
    assert len(uids) == num
