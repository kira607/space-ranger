from space_ranger.core.component import Component
from space_ranger.core.property import Property


class TestProperty(Property):
    pass


class A(Component):
    p1 = TestProperty()
    p2 = TestProperty()


class B(A):
    p3 = TestProperty()
    p4 = TestProperty()


def test_value():
    a = A()
    b = B()
