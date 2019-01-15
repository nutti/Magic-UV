import bpy

import uv_magic_uv

from . import common


class TestCopyPasteUV(common.TestBase):
    module_name = "copy_paste_uv"
    idname = [
        # Copy/Paste UV Coordinates
        ('MENU', 'uv.muv_mt_copy_paste_uv_copy_uv'),
        ('OPERATOR', 'uv.muv_ot_copy_paste_uv_copy_uv'),
        ('MENU', 'uv.muv_mt_copy_paste_uv_paste_uv'),
        ('OPERATOR', 'uv.muv_ot_copy_paste_uv_paste_uv'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"
        self.uv_map = "UVMap"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

    def test_paste_uv_ng_not_copy_first(self):
        # Warning: Need copy UV at first
        print("[TEST] (NG) Not copy first")
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_no_selected_faces(self):
        # Warning: No faces are selected
        print("[TEST] (NG) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_all(self):
        print("[TEST] (OK) All")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv(uv_map=self.uv_map)
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_object_only(self.dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[self.dest_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

    def test_paste_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        self.__prepare_paste_uv_test()
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_no_selected_faces(self):
        # Warning: No faces are selected
        print("[TEST] (NG) No selected faces")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_same_number_of_selected_face(self):
        # Warning: Number of selected faces is different from copied(src:6, dest:1)
        print("[TEST] (NG) N:N and number of selected face is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.select_faces(self.active_obj, 1)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_same_selected_face_size(self):
        # Warning: Some faces are different size
        print("[TEST] (NG) N:N and selected face size is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.mesh.tris_convert_to_quads()

    def test_paste_uv_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_all(self):
        print("[TEST] (OK) All")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_new(self):
        print("[TEST] (OK) New")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv(uv_map="__new")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_paste_uv(
            uv_map=self.uv_map,
            strategy='N_N',
            flip_copied_uv=True,
            rotate_copied_uv=3,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestCopyPasteUVSelseq(common.TestBase):
    module_name = "copy_paste_uv"
    submodule_name = "selseq"
    idname = [
        # Copy/Paste UV Coordinates (by selection sequence)
        ('MENU', 'uv.muv_mt_copy_paste_uv_selseq_copy_uv'),
        ('OPERATOR', 'uv.muv_ot_copy_paste_uv_selseq_copy_uv'),
        ('MENU', 'uv.muv_mt_copy_paste_uv_selseq_paste_uv'),
        ('OPERATOR', 'uv.muv_ot_copy_paste_uv_selseq_paste_uv'),
    ]

    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"
        self.uv_map = "UVMap"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

    def test_paste_uv_ng_not_copy_first(self):
        # Warning: Need copy UV at first
        print("[TEST] (NG) Not copy first")
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_no_selected_faces(self):
        # Warning: No faces are selected
        print("[TEST] (NG) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_all(self):
        print("[TEST] (OK) All")
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_copy_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv(uv_map=self.uv_map)
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        common.select_object_only(self.dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[self.dest_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

    def test_paste_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        self.__prepare_paste_uv_test()
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_no_selected_faces(self):
        # Warning: No faces are selected
        print("[TEST] (NG) No selected faces")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_same_number_of_selected_face(self):
        # Warning: Number of selected faces is different from copied faces (src:2, dest:1)
        print("[TEST] (NG) N:N and number of selected face is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 1)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_same_selected_face_size(self):
        # Warning: Some faces are different size
        print("[TEST] (NG) N:N and selected face size is not same")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.quads_convert_to_tris()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.mesh.tris_convert_to_quads()

    def test_paste_uv_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_all(self):
        print("[TEST] (OK) All")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv(uv_map="__all")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_new(self):
        print("[TEST] (OK) New")
        self.__prepare_paste_uv_test()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv(uv_map="__new")
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_ot_copy_paste_uv_selseq_paste_uv(
            uv_map=self.uv_map,
            strategy='N_N',
            flip_copied_uv=True,
            rotate_copied_uv=3,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})
