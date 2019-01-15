import bpy

from . import common


class TestUVWBox(common.TestBase):
    module_name = "uvw"
    submodule_name = "box"
    idname = [
        # UVW
        ('OPERATOR', 'uv.muv_ot_uvw_box_map'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_uvw_box_map(assign_uvmap=False)
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_uvw_box_map()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) user specified")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_ot_uvw_box_map(
            size=2.0,
            rotation=(0.2, 0.1, 0.4),
            offset=(1.2, 5.0, -20.0),
            tex_aspect=1.3,
            assign_uvmap=False
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestUVWBestPlaner(common.TestBase):
    module_name = "uvw"
    submodule_name = "best_planer"
    idname = [
        # UVW
        ('OPERATOR', 'uv.muv_ot_uvw_best_planer_map'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_uvw_best_planer_map(assign_uvmap=False)
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_uvw_best_planer_map()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) user specified")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_uvw_best_planer_map(
            size=0.5,
            rotation=-0.4,
            offset=(-5.0, 10.0),
            tex_aspect=0.6,
            assign_uvmap=True
        )
        self.assertSetEqual(result, {'FINISHED'})
