from . import common


class TestAlignUVCursor(common.TestBase):
    module_name = "align_uv_cursor"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_cursor_operator'),
    ]

    # this test can not be done because area always NoneType in console run
    def test_nothing(self):
        pass
