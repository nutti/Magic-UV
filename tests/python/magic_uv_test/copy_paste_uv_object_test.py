import bpy
import bmesh

from . import common
from . import compatibility as compat


class TestCopyPasteUVObject(common.TestBase):
    module_name = "copy_paste_uv_object"
    idname = [
        # Copy/Paste UV Coordinates (Among same objects)
        ('MENU', 'MUV_MT_CopyPasteUVObject_CopyUV'),
        ('OPERATOR', 'object.muv_copy_paste_uv_object_copy_uv'),
        ('MENU', 'MUV_MT_CopyPasteUVObject_PasteUV'),
        ('OPERATOR', 'object.muv_copy_paste_uv_object_paste_uv'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"
        self.uv_map = "UVMap"

        common.select_object_only(src_obj_name)
        common.duplicate_object_without_uv()
        common.select_object_only(src_obj_name)
        compat.set_active_object(bpy.data.objects[src_obj_name])
        bpy.ops.object.mode_set(mode='OBJECT')

    def test_paste_uv_ng_not_copy_first(self):
        # Warning: Need copy UV at first
        print("[TEST] (NG) Not copy first")
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.object.muv_copy_paste_uv_object_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_all(self):
        print("[TEST] (OK) All")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_copy_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified UV")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_copy_uv(uv_map=self.uv_map)
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        common.select_object_only(self.dest_obj_name)
        compat.set_active_object(bpy.data.objects[self.dest_obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='OBJECT')

    def test_paste_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        self.__prepare_paste_uv_test()
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_same_number_of_selected_face(self):
        # Warning: Number of faces is different from copied (src:6, dest:12)
        print("[TEST] (NG) Number of selected face is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.object.mode_set(mode='OBJECT')

    def test_paste_uv_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_all(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_new(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv(uv_map="__new")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified UV")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv(
            uv_map=self.uv_map,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ng_not_same_selected_face_size(self):
        # Warning: Some faces are different size
        print("[TEST] (NG) Selected face size is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        bpy.ops.mesh.select_all(action='DESELECT')
        for i, f in enumerate(bm.faces):
            if i <= 5:
                f.select = True
            else:
                f.select = False
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        result = bpy.ops.object.muv_copy_paste_uv_object_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
