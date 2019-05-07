from . import common


class TestAlignUVCircle(common.TestBase):
    module_name = "align_uv"
    submodule_name = "circle"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_circle'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass


class TestAlignUVStraighten(common.TestBase):
    module_name = "align_uv"
    submodule_name = "straighten"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_straighten'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass


class TestAlignUVAxis(common.TestBase):
    module_name = "align_uv"
    submodule_name = "axis"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_axis'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass
