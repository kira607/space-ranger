import pytest

from space_ranger.core.common import HasProperties, Descriptor, Observer


def test_collector_descriptors_inheritance() -> None:
    class A(HasProperties):  # noqa: D101
        __children__: list[Descriptor]
        x = Descriptor()

    class B(A):  # noqa: D101
        y = Descriptor()

    b = B()
    assert b.__children__ == [A.x, B.y]


def test_per_class_attributes_are_unique() -> None:
    class A(HasProperties, Observer):  # noqa: D101
        __children__: list[Descriptor]
        x = Descriptor()

        def accept_notification(self) -> None:
            pass

    class B(A):  # noqa: D101
        y = Descriptor()

    a = A()
    b = B()
    a.x = 10
    b.x = 20
    assert a.x == 10
    a.x = 30
    assert b.x == 20


def test_error_when_descriptor_collection_collides() -> None:
    with pytest.raises(RuntimeError):

        class A(HasProperties):  # noqa: D101
            __children__: list[Descriptor]
            x = Descriptor()

        class C(A):  # noqa: D101
            __children2__: list[Descriptor]


def test_descriptor_redifinition():
    class A(HasProperties, Observer):  # noqa: D101
        __children__: list[Descriptor]
        x = Descriptor()

        def accept_notification(self) -> None:
            pass

    class B(A):  # noqa: D101
        x = Descriptor()

    a = A()
    b = B()
    a.x = 10
    b.x = 20
    assert a.x == 10
    a.x = 30
    assert b.x == 20
