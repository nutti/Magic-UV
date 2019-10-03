import bpy

from . import common


class TestClipUV(common.TestBase):
    module_name = "clip_uv"
    idname = [
        # Clip UV
        ('OPERATOR', 'uv.muv_clip_uv'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_clip_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_clip_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_clip_uv(
            clip_uv_range_max=(1.5, 2.0),
            clip_uv_range_min=(-1.5, -3.0)
        )
        self.assertSetEqual(result, {'FINISHED'})