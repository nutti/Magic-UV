import unittest

import bpy

from . import common
from . import compatibility as compat


class TestCopyPasteUVUVEdit(common.TestBase):
    module_name = "copy_paste_uv_uvedit"
    idname = [
        # Copy/Paste UV Coordinates on UV/Image Editor
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_copy_uv'),
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_paste_uv'),
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_copy_uv_island'),
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_paste_uv_island'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"

        common.select_object_only(src_obj_name)
        common.duplicate_object_without_uv()
        compat.set_active_object(bpy.data.objects[src_obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.context.scene.tool_settings.use_uv_select_sync = True

    def tearDownMethod(self):
        bpy.context.scene.tool_settings.use_uv_select_sync = False

    def test_copy_uv_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_island_ok(self):
        print("[TEST] (OK) Copy UV Island")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv_island()
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_copy_uv_island_multiple_objects(self):
        print("[TEST] (OK) Copy UV Island Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        bpy.ops.object.duplicate()

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

        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv_island()
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_object_only(self.dest_obj_name)
        compat.set_active_object(bpy.data.objects[self.dest_obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='EDIT')

    def __prepare_paste_uv_island_test(self):
        # Copy UV Island
        bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.uv_texture_add() fails for this test.
        # The reason is not clear, but this failure can be avoided
        # by using bpy.ops.uv.smart_project().
        bpy.ops.uv.smart_project()
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv_island()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok(self):
        print("[TEST] (OK)")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_island_ok(self):
        print("[TEST] (OK) Paste UV Island")
        self.__prepare_paste_uv_island_test()
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_paste_uv_island()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_island_ok_with_unique_target(self):
        print("[TEST] (OK) Paste UV Island with Unique Target")
        self.__prepare_paste_uv_island_test()
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_paste_uv_island(
            unique_target=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_paste_uv_island_multiple_objects(self):
        print("[TEST] (OK) Paste UV Island Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        bpy.ops.object.duplicate()

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

        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv_island()
        self.assertSetEqual(result, {'FINISHED'})
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_paste_uv_island(
            unique_target=True
        )
        self.assertSetEqual(result, {'FINISHED'})
