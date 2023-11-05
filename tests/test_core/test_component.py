from dataclasses import dataclass

from space_ranger.core import Component


@dataclass(slots=True)
class MyComponent(Component):  # noqa: D101
    speed: float = 0.0
    max_speed: float = 5.0
    is_jumping: bool = False


def test_inheriting_from_component() -> None:
    """Creating a new component by inheriting from the base class should result in a valid component."""
    component = MyComponent()
    assert isinstance(component, Component)
    assert isinstance(component, MyComponent)


def test_get_key_method() -> None:
    """Retrieving a component key using the 'get_key' method should return a valid component key."""
    class_key = MyComponent.get_key()
    instance_key = MyComponent().get_key()
    assert class_key == instance_key == MyComponent
