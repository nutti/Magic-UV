import bpy

from . import common
from . import compatibility as compat


class TestTextureProjection(common.TestBase):
    module_name = "texture_projection"
    idname = [
        # Texture Lock
        ('OPERATOR', 'uv.muv_texture_projection'),
        ('OPERATOR', 'uv.muv_texture_projection_project'),
    ]

    # can not test interactive mode
    #  - modal operator can not invoke directly from cmdline
    # can not test OK case
    #  - context.region will be NoneType
    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_no_image(self):
        # Warning: No textures are selected
        print("[TEST] (NG) No Image")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.scene.muv_texture_projection_tex_image = 'None'
        result = bpy.ops.uv.muv_texture_projection_project()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        bpy.ops.image.new(name='Test')
        bpy.context.scene.muv_texture_projection_tex_image = 'Test'
        bpy.context.scene.muv_texture_projection_assign_uvmap = False
        result = bpy.ops.uv.muv_texture_projection_project()
        self.assertSetEqual(result, {'CANCELLED'})
