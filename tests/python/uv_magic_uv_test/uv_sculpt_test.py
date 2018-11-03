from . import common


class TestUVSculpt(common.TestBase):
    module_name = "uv_sculpt"
    idname = [
        # UV Sculpt
        ('OPERATOR', "uv.muv_uv_sculpt_operator"),
    ]

    # modal operator can not invoke directly from cmdline
    def test_nothing(self):
        pass
