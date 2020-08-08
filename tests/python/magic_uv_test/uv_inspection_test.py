import unittest

import bpy

from . import common
from . import compatibility as compat


class TestUVInspection(common.TestBase):
    module_name = "uv_inspection"
    idname = [
        # UV Inspection
        ('OPERATOR', "uv.muv_uv_inspection_render"),
        ('OPERATOR', "uv.muv_uv_inspection_update"),
    ]

    def setUpEachMethod(self):
        self.obj_names = ["Cube", "Cube.001"]

        common.select_object_only(self.obj_names[0])
        common.duplicate_object_without_uv()
        common.select_object_only(self.obj_names[0])
        compat.set_active_object(bpy.data.objects[self.obj_names[0]])
        bpy.ops.object.mode_set(mode='EDIT')

        sc = bpy.context.scene
        sc.muv_uv_inspection_show_overlapped = True
        sc.muv_uv_inspection_show_flipped = True
        sc.muv_uv_inspection_show_mode = 'FACE'

    def test_ok_update_single_object(self):
        print("[TEST] Single Object (OK)")
        result = bpy.ops.uv.muv_uv_inspection_update()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_update_multiple_objects(self):
        print("[TEST] Multiple Object (OK)")
        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_objects_only(self.obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_uv_inspection_update()
        self.assertSetEqual(result, {'FINISHED'})


class TestUVInspectionPaintUVIsland(common.TestBase):
    module_name = "uv_inspection"
    submodule_name = "paint_uv_island"
    idname = [
        # UV Inspection (Paint UV Island)
        ('OPERATOR', "uv.muv_uv_inspection_paint_uv_island"),
    ]

    def test_paint_uv_island_only_run(self):
        print("[TEST] (Only Run)")
        result = bpy.ops.uv.muv_uv_inspection_paint_uv_island()
        # Paint UV Island needs 'IMAGE_EDITOR' space and 'VIEW_3D' space,
        # but we can not setup such environment in this test.
        self.assertSetEqual(result, {'CANCELLED'})
