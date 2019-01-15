import bpy

from . import common


class TestTextureWrap(common.TestBase):
    module_name = "texture_wrap"
    idname = [
        # Texture Wrap
        ('OPERATOR', 'uv.muv_ot_texture_wrap_refer'),
        ('OPERATOR', 'uv.muv_ot_texture_wrap_set'),
    ]

    # "More than 1 vertex must be unshared" does rarely occur,
    # so skip this test
    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        sc = bpy.context.scene

        sc.muv_texture_wrap_set_and_refer = False


    def test_refer_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_ot_texture_wrap_refer()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_set_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_refer_ng_not_select_one_face(self):
        # Warning: Must select only one face
        print("[TEST] (NG) Not select 1 face")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_ot_texture_wrap_refer()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_refer_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        common.select_faces(self.active_obj, 1)
        result = bpy.ops.uv.muv_ot_texture_wrap_refer()
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_set_test(self):
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        common.select_faces(self.active_obj, 1)
        result = bpy.ops.uv.muv_ot_texture_wrap_refer()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.mesh.select_all(action='DESELECT')

    def test_set_ng_not_select_one_face(self):
        # Warning: Must select only one face
        print("[TEST] (NG) Not select 1 face")
        self.__prepare_set_test()
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_set_ng_not_select_different_face(self):
        # Warning: Must select different face
        print("[TEST] (NG) Not select different face")
        self.__prepare_set_test()
        common.select_faces(self.active_obj, 1)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_set_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_set_test()
        common.select_faces(self.active_obj, 1, 2)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'FINISHED'})

    def test_set_ok_set_and_refer(self):
        sc = bpy.context.scene
        sc.muv_texture_wrap_set_and_refer = True

        self.__prepare_set_test()
        common.select_faces(self.active_obj, 1, 2)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.mesh.select_all(action='DESELECT')
        common.select_faces(self.active_obj, 1, 3)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'FINISHED'})

    def test_set_ng_not_share_2_vertices(self):
        # Warning: 2 vertices must be shared among faces
        print("[TEST] (NG) Not share 2 vertices")
        self.__prepare_set_test()
        common.select_faces(self.active_obj, 1, 1)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_set_ng_selseq_no_selected_face(self):
        sc = bpy.context.scene
        sc.muv_texture_wrap_selseq = True

        # Warning: Must select more than one face
        print("[TEST] (NG) No selected face")
        self.__prepare_set_test()
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_set_ok_selseq(self):
        print("[TEST] (OK) Selection Sequence")
        self.__prepare_set_test()
        common.add_face_select_history(self.active_obj, 1, 2)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'FINISHED'})

    def test_set_ng_different_object(self):
        sc = bpy.context.scene
        sc.muv_texture_wrap_selseq = False

        # Warning: Object must be same
        print("[TEST] (NG) Different object")
        self.__prepare_set_test()
        common.add_face_select_history(self.active_obj, 1, 2)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()
        common.select_object_only("Cube.001")
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        common.select_faces(active_obj, 1, 1)
        result = bpy.ops.uv.muv_ot_texture_wrap_set()
        self.assertSetEqual(result, {'CANCELLED'})
