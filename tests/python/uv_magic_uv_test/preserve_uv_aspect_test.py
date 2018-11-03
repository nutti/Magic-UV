import bpy
import bmesh

from . import common


class TestPreserveUVAspect(common.TestBase):
    module_name = "preserve_uv_aspect"
    idname = [
        # Preserve UV
        ('OPERATOR', 'uv.muv_preserve_uv_aspect_operator'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"
        self.dest_img_name = "Test"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(active_obj.data)
        tex_layer = bm.faces.layers.tex.verify()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.image.new(name=self.dest_img_name)
        for f in bm.faces:
            f[tex_layer].image = bpy.data.images[self.dest_img_name]

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_preserve_uv_aspect_operator(dest_img_name=self.dest_img_name)
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_preserve_uv_aspect_operator(dest_img_name=self.dest_img_name)
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) user specified")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_preserve_uv_aspect_operator(
            dest_img_name=self.dest_img_name,
            origin='RIGHT_TOP'
        )
        self.assertSetEqual(result, {'FINISHED'})
