import bpy

from . import common


class TestUVInspection(common.TestBase):
    module_name = "uv_inspection"
    idname = [
        # UV Inspection
        ('OPERATOR', "uv.muv_uv_inspection_operator_render"),
        ('OPERATOR', "uv.muv_uv_inspection_operator_update"),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        sc = bpy.context.scene
        sc.muv_uv_inspection_show_overlapped = True
        sc.muv_uv_inspection_show_flipped = True
        sc.muv_uv_inspection_show_mode = 'FACE'

    def test_update_ok(self):
        print("[TEST] (OK)")
        result = bpy.ops.uv.muv_uv_inspection_operator_update()
        self.assertSetEqual(result, {'FINISHED'})
