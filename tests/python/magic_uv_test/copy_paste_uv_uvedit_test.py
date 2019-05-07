import bpy

from . import common


class TestCopyPasteUVUVEdit(common.TestBase):
    module_name = "copy_paste_uv_uvedit"
    idname = [
        # Copy/Paste UV Coordinates on UV/Image Editor
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_copy_uv'),
        ('OPERATOR', 'uv.muv_copy_paste_uv_uvedit_paste_uv'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_copy_uv_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_object_only(self.dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[self.dest_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')


    def test_paste_uv_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_copy_paste_uv_uvedit_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})