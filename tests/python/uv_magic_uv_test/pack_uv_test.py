import bpy

from . import common


class TestPackUV(common.TestBase):
    module_name = "pack_uv"
    idname = [
        # Pack UV (with same UV island packing)
        ('OPERATOR', 'uv.muv_pack_uv_operator'),
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
        result = bpy.ops.uv.muv_pack_uv_operator()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_pack_uv_operator()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_pack_uv_operator(
            rotate=True,
            margin=0.03,
            allowable_center_deviation=(0.02, 0.05),
            allowable_size_deviation=(0.003, 0.0004)
        )
        self.assertSetEqual(result, {'FINISHED'})