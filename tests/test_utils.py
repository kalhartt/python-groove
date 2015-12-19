from enum import IntEnum

import pytest

from groove import utils

class TestUniqueEnum():
    """Test the utils.unique_enum decorator"""

    def test_unique(self):
        """It should raise a ValueError if values are repeated"""
        with pytest.raises(ValueError):
            @utils.unique_enum
            class MyEnum(IntEnum):
                x = 1
                y = 1

    def test_reverse(self):
        """It should create a value : member map called __values__"""
        @utils.unique_enum
        class MyEnum(IntEnum):
            x = -1
            y = 0
            z = 1

        assert MyEnum.__values__[-1] == MyEnum.x
        assert MyEnum.__values__[0] == MyEnum.y
        assert MyEnum.__values__[1] == MyEnum.z
