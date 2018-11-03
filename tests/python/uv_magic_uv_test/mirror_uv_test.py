import bpy

from . import common


class TestMirrorUV(common.TestBase):
    module_name = "mirror_uv"
    idname = [
        # Mirror UV
        ('OPERATOR', 'uv.muv_mirror_uv_operator'),
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
        result = bpy.ops.uv.muv_mirror_uv_operator()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv_operator()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_1(self):
        print("[TEST] (OK) User specified 1")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv_operator(axis='Y', error=0.7)
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_2(self):
        print("[TEST] (OK) User specified 2")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv_operator(axis='Y', error=19.4)
        self.assertSetEqual(result, {'FINISHED'})
