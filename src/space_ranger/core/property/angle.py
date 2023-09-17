from .float import Float


class Angle(Float):
    """An angle property.

    Holds angle value in degrees [0.0, 360.0]
    """

    @classmethod
    def adapt(cls, value: Float.InputType) -> Float.ValueType:
        """Adapt input value to correct value type.

        :param value: Input value.
        :type value: InputType

        :return: Value of correct type.
        :rtype: ValueType
        """
        return abs(float(value) % 360.0)
