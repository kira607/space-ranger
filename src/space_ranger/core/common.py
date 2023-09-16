from __future__ import annotations

import abc
import inspect
import typing as t

from typing_extensions import Unpack

_TOwner = t.TypeVar("_TOwner")
_TInstance = t.TypeVar("_TInstance", bound="Observer")
_TValue = t.TypeVar("_TValue")
_TInput = t.TypeVar("_TInput")


class DescriptorMetaKwargs(t.TypedDict):
    """**kwargs definition for :class:`DescriptorMeta`."""

    readonly: bool


class DescriptorMeta(type):
    """A :class:`Descriptor` metaclass.

    Creates a :class:`Descriptor` class.
    If readonly keyword argument is specified, the resulting :class:`Descriptor` class
    will be readonly (`__set__` will raise an error when called).
    """

    def __new__(
        mcs: type,  # noqa: N804
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, t.Any],
        **kwargs: Unpack[DescriptorMetaKwargs],
    ) -> type:
        """Construct a new :class:`Descriptor` class.

        :param mcs: Metaclass. Should be type
        :type mcs: type
        :param name: Name of the class.
        :type name: str
        :param bases: Tuple of class bases.
        :type bases: tuple[type, ...]
        :param namespace: Class namespace.
        :type namespace: dict[str, t.Any]

        :return: New class
        :rtype: type
        """
        _cls = super().__new__(mcs, name, bases, namespace)
        if kwargs.get("readonly"):

            def _set(self, *a, **k) -> None:  # noqa, type: ignore
                raise AttributeError(f"{self.__class__.__name__} attribute is readonly")

            _cls.__set__ = _set
        return _cls


class Descriptor(t.Generic[_TOwner, _TInstance, _TValue, _TInput], metaclass=DescriptorMeta):
    """A basic descriptor.

    On `__set__` sends notification to parent object instance.

    :ivar str name: Name of the class attribute accessed by this descriptor.
      It is set when a `__set_name__()` is called.
    :ivar _TValue default: The default value of the attribute.

    :param default: Default value of the descriptor value.
    :type default: _TPropertyValue
    """

    def __init__(self) -> None:
        self.public_name: str
        self.name: str

    def __get__(
        self,
        instance: _TInstance | None,
        owner: _TOwner | None = None,
    ) -> _TValue | Descriptor | None:
        """Get value.

        :param instance: Object instance that has the property.
        :type instance: _TInstance | None
        :param owner: Instance class/type.
        :type owner: _TOwner | None

        :return: Descriptor value if accessed from class instance, :class:`Descriptor` instance otherwise.
          If instance is not instantiated returns None.
        :rtype: _TValue | Descriptor
        """
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance: _TInstance, value: _TInput) -> None:
        """Set value.

        This will notify parent instance using `instance.accept_notification()`.

        :param instance: Instance that has the property.
        :type instance: _TInstance
        :param value: A new value of the attribute.
        :type value: _TInput
        """
        new_value = self.adapt(value)
        setattr(instance, self.name, new_value)
        instance.accept_notification()

    def __set_name__(self, owner: _TOwner, name: str) -> None:
        """Set descriptor name.

        Uses name to create a protected object attribute
        which is later accessed using this descriptor.

        :param type owner: Descriptor class.
        :type owner: _TOwner
        :param name: Descriptor name.
        :type name: str
        """
        if name.startswith("_"):
            raise RuntimeError(f"Protected {self.__class__.__name__} names are forbidden: {name}")
        self.public_name = name
        self.name = f"_{name}"

    def __str__(self) -> str:
        """Get string representation."""
        return f"{self.__class__.__name__}('{self.public_name}')"

    def __repr__(self) -> str:
        """Get object string representation."""
        return f"<{str(self)}>"

    def adapt(self, value: _TInput) -> _TValue:
        """Adapt input value to value type.

        :param value: Input value.
        :type value: _TInput

        :return: Value of correct type.
        :rtype: _TValue
        """
        return value

    def on_collect(self, instance: _TInstance) -> None:
        """Do something on collect."""
        pass


class Observer(abc.ABC):
    """Observer interface.

    The sole purpose of this class
    is to force child classes to implement
    `accept_notification()` method.
    """

    @abc.abstractmethod
    def accept_notification(self) -> None:
        """Accept a notification from a publisher."""
        raise NotImplementedError()


class HasProperties:
    """Proxy class to make child classes use CollectsChildrenMeta metaclass using inheritance.

    Modifies class __new__ method to collect class attributes that follow the rules:
      * attribute name must follow "special" rule: start and end with "__"
      * attribute type hint must be a list of Descriptors or Descriptor sub type (`list[Descriptor]`)
      * each collection should have a unique Descriptor (sub type) type hint.

    A collection of Descriptors is done after original __new__ method is called.

    For example::

        class A(Collector):
            __children__: list[Descriptor]
            a = Descriptor()
    """

    def __new__(cls, *args, **kwargs) -> HasProperties:
        """Construct collector."""
        obj = super().__new__(cls)
        for _, prop in inspect.getmembers(obj.__class__, lambda p: isinstance(p, Descriptor)):
            prop.on_collect(obj)
        return obj
