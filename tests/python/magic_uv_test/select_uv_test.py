import unittest

import bpy

from . import common
from . import compatibility as compat


class TestSelectUVOverlapped(common.TestBase):
    module_name = "select_uv"
    submodule_name = "overlapped"
    idname = [
        # Select UV
        ('OPERATOR', 'uv.muv_select_uv_select_overlapped'),
    ]

    def setUpEachMethod(self):
        self.obj_names = ["Cube", "Cube.001"]

        common.select_object_only(self.obj_names[0])
        common.duplicate_object_without_uv()
        common.select_object_only(self.obj_names[0])
        compat.set_active_object(bpy.data.objects[self.obj_names[0]])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=True")
        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_no_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=False")
        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] Multiple Object (OK)")
        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_objects_only(self.obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_select_uv_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})


class TestSelectUVFlipped(common.TestBase):
    module_name = "select_uv"
    submodule_name = "flipped"
    idname = [
        # Select UV
        ('OPERATOR', 'uv.muv_select_uv_select_flipped'),
    ]

    def setUpEachMethod(self):
        self.obj_names = ["Cube", "Cube.001"]

        common.select_object_only(self.obj_names[0])
        common.duplicate_object_without_uv()
        common.select_object_only(self.obj_names[0])
        compat.set_active_object(bpy.data.objects[self.obj_names[0]])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok_select_sync(self):
        print("[TEST] (OK) Select Flipped with UV_Select_Sync=True")
        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_no_select_sync(self):
        print("[TEST] (OK) Select Flipped with UV_Select_Sync=False")
        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] Multiple Object (OK)")
        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_objects_only(self.obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_select_uv_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})
