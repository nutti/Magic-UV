from . import common


class TestSmoothUV(common.TestBase):
    module_name = "smooth_uv"
    idname = [
        # Smooth UV
        ('OPERATOR', 'uv.muv_smooth_uv_operator'),
    ]

    # Smooth UV has a complicated condition to test
    def test_nothing(self):
        pass
