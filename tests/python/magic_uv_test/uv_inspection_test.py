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
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        sc = bpy.context.scene
        sc.muv_uv_inspection_show_overlapped = True
        sc.muv_uv_inspection_show_flipped = True
        sc.muv_uv_inspection_show_mode = 'FACE'

    def test_ok_update_single_object(self):
        print("[TEST] Single Object (OK)")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_uv_inspection_update()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_update_multiple_objects(self):
        print("[TEST] Multiple Object (OK)")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
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

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_paint_uv_island_only_run(self):
        print("[TEST] (Only Run)")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_uv_inspection_paint_uv_island()
        # Paint UV Island needs 'IMAGE_EDITOR' space and 'VIEW_3D' space,
        # but we can not setup such environment in this test.
        self.assertSetEqual(result, {'CANCELLED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_update_multiple_objects(self):
        print("[TEST] Multiple Object (Only Run)")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_uv_inspection_paint_uv_island()
        # Paint UV Island needs 'IMAGE_EDITOR' space and 'VIEW_3D' space,
        # but we can not setup such environment in this test.
        self.assertSetEqual(result, {'CANCELLED'})
