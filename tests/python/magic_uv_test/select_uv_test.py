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
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=True")
        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_no_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=False")
        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_select_overlapped(
            same_polygon_threshold=0.005
        )
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] Multiple Object (With UV Select Sync)")

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

        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] Multiple Object (Without UV Select Sync)")

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

        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_select_overlapped(
            same_polygon_threshold=0.005
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestSelectUVFlipped(common.TestBase):
    module_name = "select_uv"
    submodule_name = "flipped"
    idname = [
        # Select UV
        ('OPERATOR', 'uv.muv_select_uv_select_flipped'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
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
        print("[TEST] Multiple Object (With UV Select Sync)")

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

        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] Multiple Object (Without UV Select Sync)")

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

        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})


class TestSelectUVZoomSelectedUV(common.TestBase):
    module_name = "uv_inspection"
    submodule_name = "zoom_selected_uv"
    idname = [
        # Select UV (Zoom Selected UV)
        ('OPERATOR', "uv.muv_select_uv_zoom_selected_uv"),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_select_uv_zoom_selected_uv()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_multiple_objects_ok(self):
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

        result = bpy.ops.uv.muv_select_uv_zoom_selected_uv()
        self.assertSetEqual(result, {'FINISHED'})
