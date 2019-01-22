from . import common


class TestUVBoundingBox(common.TestBase):
    module_name = "uv_bounding_box"
    idname = [
        # UV Bounding Box
        ('OPERATOR', "uv.muv_ot_uv_bounding_box"),
    ]

    # modal operator can not invoke directly from cmdline
    def test_nothing(self):
        pass
