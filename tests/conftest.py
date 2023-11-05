import pytest

from space_ranger.core import EcTable


@pytest.fixture
def ec_table() -> EcTable:
    """Create a new EcTable.

    :return: EcTable instance
    :rtype: EcTable
    """
    return EcTable()
