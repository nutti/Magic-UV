from . import common


class TestMoveUV(common.TestBase):
    module_name = "move_uv"
    idname = [
        # Move UV
        ('OPERATOR', "uv.muv_move_uv"),
    ]

    # modal operator can not invoke directly from cmdline
    def test_nothing(self):
        pass
