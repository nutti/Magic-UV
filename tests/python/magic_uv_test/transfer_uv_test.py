import bpy
import bmesh

from . import common


class TestTransferUV(common.TestBase):
    module_name = "transfer_uv"
    idname = [
        # Transfer UV
        ('OPERATOR', 'uv.muv_transfer_uv_copy_uv'),
        ('OPERATOR', 'uv.muv_transfer_uv_paste_uv'),
    ]

    # some test is complicated to reproduce
    #  - there is no case more than 2 faces share one edge
    def setUpEachMethod(self):
        src_obj_name = "Cube"
        self.dest_obj_name = "Cube.001"

        common.select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        self.active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

    def test_copy_uv_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_not_select_two_faces(self):
        # Warning: Two faces must be selected
        print("[TEST] (NG) Not select two faces")
        bpy.ops.mesh.uv_texture_add()
        common.select_faces(self.active_obj, 1)
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_not_active_two_faces(self):
        # Warning: Two faces must be active
        print("[TEST] (NG) Not active two faces")
        bpy.ops.mesh.uv_texture_add()
        common.select_faces(self.active_obj, 2)
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        for f in bm.faces:
            if not f.select:
                bm.faces.active = f
                break
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ng_not_share_one_edge(self):
        # Warning: Two faces should share one edge
        print("[TEST] (NG) Not share one edge")
        bpy.ops.mesh.uv_texture_add()
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        selected_faces = common.select_and_active_faces_bm(bm, 1)
        common.select_unlink_faces_bm(bm, selected_faces[0], 1)
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_copy_uv_ok(self):
        print("[TEST] (OK)")
        bpy.ops.mesh.uv_texture_add()
        common.select_and_active_faces(self.active_obj, 1)
        common.select_link_face(self.active_obj, 1)
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def __prepare_paste_uv_test(self):
        # Copy UV
        bpy.ops.mesh.uv_texture_add()
        common.select_and_active_faces(self.active_obj, 1)
        common.select_link_face(self.active_obj, 1)
        result = bpy.ops.uv.muv_transfer_uv_copy_uv()
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
        result = bpy.ops.uv.muv_transfer_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_select_two_faces(self):
        # Warning: Two faces must be selected
        print("[TEST] (NG) Not two face select")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 1)
        result = bpy.ops.uv.muv_transfer_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ng_not_share_one_edge(self):
        # Warning: Two faces should share one edge
        print("[TEST] (NG) Two faces should share one edge")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        common.add_face_select_history(self.active_obj, 2)
        result = bpy.ops.uv.muv_transfer_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_paste_uv_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        bm.select_history.clear()
        selected_face = common.select_and_active_faces(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = common.select_link_face(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transfer_uv_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        bm.select_history.clear()
        selected_face = common.select_and_active_faces(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = common.select_link_face(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transfer_uv_paste_uv(
            invert_normals=True,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_paste_uv_ng_different_amount_of_faces(self):
        # Warning: Mesh has different amount of faces
        print("[TEST] (NG) Mesh has different amount of faces")
        self.__prepare_paste_uv_test()
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bm = bmesh.from_edit_mesh(self.active_obj.data)
        bm.select_history.clear()
        selected_face = common.select_and_active_faces(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = common.select_link_face(self.active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transfer_uv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.tris_convert_to_quads()

