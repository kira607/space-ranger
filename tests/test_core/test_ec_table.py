from dataclasses import dataclass

import pytest

from space_ranger.core import Component
from space_ranger.core.component import EntityData
from space_ranger.core.ec_table import EcTable
from space_ranger.core.entity import Entity, generate_entity_uid
from space_ranger.core.errors import UnknownEntityUidError


@dataclass(slots=True)
class ComponentA(Component):  # noqa: D101
    a: int = 0


@dataclass(slots=True)
class ComponentB(Component):  # noqa: D101
    b: int = 0


def test_create_entity_auto_adds_entity_data(ec_table: EcTable) -> None:
    """Test that creating an entity automatically adds :class:`EntityData` component.

    The test also checks that :class:`EntityData` is filled properly.
    """
    name = "player"

    entity = ec_table.create_entity(name)

    entity_data: EntityData = ec_table._table[entity.uid][EntityData]  # type: ignore
    assert entity_data is not None
    assert entity_data.uid == entity.uid
    assert entity_data.name == name
    assert entity_data.enabled is True


def test_create_entity_adds_components(ec_table: EcTable) -> None:
    """Test that `create_entity()` adds components to an entity."""
    name = "player"
    component_a = ComponentA()
    component_b = ComponentB()

    entity = ec_table.create_entity(name, component_a, component_b)
    uid = entity.uid

    assert ec_table._table[uid][ComponentA] == component_a
    assert ec_table._table[uid][ComponentB] == component_b


def test_create_entity_no_components(ec_table: EcTable) -> None:
    """Test that `create_entity()` can create an entity with no components."""
    name = "player"

    entity = ec_table.create_entity(name)

    assert len(ec_table._table[entity.uid]) == 1


def test_get_entity_by_uid_returns_entity(ec_table: EcTable) -> None:
    """Test that `get_entity_by_uid()` returns an entity instance."""
    entity = ec_table.create_entity("player")
    assert isinstance(entity, Entity)
    assert ec_table.get_entity_by_uid(entity.uid) == entity


def test_get_entity_by_uid_returns_entity_if_exists(ec_table: EcTable) -> None:
    """Test that `get_entity_by_uid()` returns the entity with the given UID."""
    entity_uid = generate_entity_uid()
    entity_data = EntityData("entity", entity_uid)
    ec_table._table[entity_uid] = {EntityData: entity_data}  # type: ignore

    entity = ec_table.get_entity_by_uid(entity_uid)

    assert entity.uid == entity_uid
    assert entity.name == "entity"
    assert entity._ec_table == ec_table


def test_get_entity_by_uid_returns_default_value_if_not_exist_with_default(ec_table: EcTable) -> None:
    """Test that `get_entity_by_uid()` returns the default value.

    If the entity with the given UID does not exist and a default value was provided
    a default value should be returned.
    """
    default_value = "default"

    result = ec_table.get_entity_by_uid("nonexistent", default=default_value)

    assert result == default_value


def test_get_entity_by_uid_raises_error_if_not_exist_without_default(ec_table: EcTable) -> None:
    """Test that `get_entity_by_uid()` raises an :class:`UnknownEntityUidError`.

    If the entity with the given UID does not exist and a default value was not provided
    an :class:`UnknownEntityUidError` should be raised.
    """
    with pytest.raises(UnknownEntityUidError):
        ec_table.get_entity_by_uid("nonexistent")


def test_delete_entity_deletes_entity_with_valid_uid(ec_table: EcTable) -> None:
    """Test that `delete_entity()` deletes an entity with a valid UID."""
    entity = ec_table.create_entity("entity")
    uid = entity.uid

    ec_table.delete_entity(uid)

    assert uid not in ec_table._table


def test_delete_entity_raises_error_for_invalid_uid(ec_table: EcTable) -> None:
    """Test that `delete_entity()` raises :class:`UnknownEntityUidError` if UID is invalid."""
    # Create a new entity
    entity = ec_table.create_entity("entity")
    uid = entity.uid

    # Delete the entity with an invalid UID
    with pytest.raises(UnknownEntityUidError):
        ec_table.delete_entity("invalid_uid")

    # Check that the entity is not deleted from the table
    assert uid in ec_table._table


# TODO: write tests for components mantipulation methods in EcTable
# TODO: write tests for entities and components iterators in EcTable
# TODO: write tests for entities querying methods in EcTable
