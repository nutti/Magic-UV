import bpy
import bmesh

from . import common
from . import compatibility as compat


class TestPreserveUVAspect(common.TestBase):
    module_name = "preserve_uv_aspect"
    idname = [
        # Preserve UV
        ('OPERATOR', 'uv.muv_preserve_uv_aspect'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"
        self.dest_img_name = "Test"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_preserve_uv_aspect(dest_img_name=self.dest_img_name)
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        active_obj = compat.get_active_object(bpy.context)
        common.assign_new_image(active_obj, self.dest_img_name)
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_preserve_uv_aspect(dest_img_name=self.dest_img_name)
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) user specified")
        active_obj = compat.get_active_object(bpy.context)
        common.assign_new_image(active_obj, self.dest_img_name)
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_preserve_uv_aspect(
            dest_img_name=self.dest_img_name,
            origin='RIGHT_TOP'
        )
        self.assertSetEqual(result, {'FINISHED'})
