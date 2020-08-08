import bpy

from . import common
from . import compatibility as compat


class TestFlipRotateUV(common.TestBase):
    module_name = "flip_rotate_uv"
    idname = [
        # Flip/Rotate UVs
        ('OPERATOR', 'uv.muv_flip_rotate_uv'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_flip_rotate_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_selected_faces(self):
        # Warning: No faces are selected
        print("[TEST] (NG) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_flip_rotate_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_flip_rotate_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_flip_rotate_uv(flip=True, rotate=5, seams=False)
        self.assertSetEqual(result, {'FINISHED'})
