import bpy
import bmesh

import sys
import unittest
from io import StringIO


TESTEE_FILE = "testee.blend"


def check_addon_enabled(mod):
    result = bpy.ops.wm.addon_enable(module=mod)
    assert (result == {'FINISHED'}), "Failed to enable add-on %s" % (mod)
    assert (mod in bpy.context.user_preferences.addons.keys()), "Failed to enable add-on %s" % (mod)


def check_addon_disabled(mod):
    result = bpy.ops.wm.addon_disable(module=mod)
    assert (result == {'FINISHED'}), "Failed to disable add-on %s" % (mod)
    assert (not mod in bpy.context.user_preferences.addons.keys()), "Failed to disable add-on %s" % (mod)


def operator_exists(idname):
    try:
        from bpy.ops import op_as_string
        op_as_string(idname)
        return True
    except:
        return False


def menu_exists(idname):
    return idname in dir(bpy.types)


def select_object_only(obj_name):
    for o in bpy.data.objects:
        if o.name == obj_name:
            o.select = True
        else:
            o.select = False


def select_faces(obj, num_face, offset=0):
    bm = bmesh.from_edit_mesh(obj.data)
    selected_faces = []
    for i, f in enumerate(bm.faces[offset:]):
        if i >= num_face:
            f.select = False
        else:
            f.select = True
            selected_faces.append(f)
    return selected_faces

def select_and_active_faces(obj, num_face):
    bm = bmesh.from_edit_mesh(obj.data)
    selected_face = []
    for i, f in enumerate(bm.faces):
        if i >= num_face:
            f.select = False
        else:
            f.select = True
            bm.faces.active = f
            selected_face.append(f)
    return selected_face

def select_unlink_faces(obj, face, num_face):
    bm = bmesh.from_edit_mesh(obj.data)
    count = 0
    linked_faces = []
    selected_faces = []
    for e in face.edges:
        for lf in e.link_faces:
            linked_faces.append(lf)
    for f in bm.faces:
        if not f in linked_faces:
            f.select = True
            count = count + 1
            selected_faces.append(f)
        if count >= num_face:
            break
    return selected_faces

def select_link_face(obj, num_face):
    bm = bmesh.from_edit_mesh(obj.data)
    count = 0
    selected_face = []
    for f in bm.faces:
        if f.select:
            for e in f.edges:
                for lf in e.link_faces:
                    if not lf.select:
                        lf.select = True
                        selected_face.append(lf)
                        count = count + 1
                    if count >= num_face:
                        break
                if count >= num_face:
                    break
        if count >= num_face:
            break
    return selected_face

def add_face_select_history(obj, num_face, offset=0):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.select_history.clear()
    for i, f in enumerate(bm.faces[offset:]):
        if i < num_face:
            bm.select_history.add(f)
    for hist in bm.select_history:
        hist.select = True


class StdoutCapture():
    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def get_captured_value(self):
        return self.capture.getValue()


class TestBase(unittest.TestCase):

    modname = None
    idname = []

    @classmethod
    def setUpClass(cls):
        try:
            bpy.ops.wm.read_factory_settings()
            check_addon_enabled(cls.modname)
            for op in cls.idname:
                if op[0] == 'OPERATOR':
                    assert operator_exists(op[1]), "Operator %s does not exist" % (op[1])
                elif op[0] == 'MENU':
                    assert menu_exists(op[1]), "Menu %s does not exist" % (op[1])
            bpy.ops.wm.save_as_mainfile(filepath=TESTEE_FILE)
        except AssertionError as e:
            print(e)
            sys.exit(1)

    @classmethod
    def tearDownClass(cls):
        try:
            check_addon_disabled(cls.modname)
            for op in cls.idname:
                if op[0] == 'OPERATOR':
                    assert not operator_exists(op[1]), "Operator %s exists" % (op[1])
                elif op[0] == 'MENU':
                    assert not menu_exists(op[1]), "Menu %s exists" % (op[1])
        except AssertionError as e:
            print(e)
            sys.exit(1)


class TestUVMagicUV(TestBase):

    modname = 'uv_magic_uv'
    idname = [
        # Copy/Paste UV Coordinates
        ('MENU', 'uv.muv_cpuv_copy_uv_menu'),
        ('OPERATOR', 'uv.muv_cpuv_copy_uv'),
        ('MENU', 'uv.muv_cpuv_paste_uv_menu'),
        ('OPERATOR', 'uv.muv_cpuv_paste_uv'),

        # Copy/Paste UV Coordinates (Among same objects)
        ('MENU', 'object.muv_cpuv_obj_copy_uv_menu'),
        ('OPERATOR', 'object.muv_cpuv_obj_copy_uv'),
        ('MENU', 'object.muv_cpuv_obj_paste_uv_menu'),
        ('OPERATOR', 'object.muv_cpuv_obj_paste_uv'),

        # Copy/Paste UV Coordinates on UV/Image Editor
        ('OPERATOR', 'uv.muv_cpuv_ie_copy_uv'),
        ('OPERATOR', 'uv.muv_cpuv_ie_paste_uv'),

        # Copy/Paste UV Coordinates (by selection sequence)
        ('MENU', 'uv.muv_cpuv_selseq_copy_uv_menu'),
        ('OPERATOR', 'uv.muv_cpuv_selseq_copy_uv'),
        ('MENU', 'uv.muv_cpuv_selseq_paste_uv_menu'),
        ('OPERATOR', 'uv.muv_cpuv_selseq_paste_uv'),

        # Flip/Rotate UVs
        ('OPERATOR', 'uv.muv_fliprot'),

        # Transfer UV
        ('OPERATOR', 'uv.muv_transuv_copy'),
        ('OPERATOR', 'uv.muv_transuv_paste'),

        # Manipulate UV with Bouding Box in UV Editor
        ('OPERATOR', "uv.muv_uvbb_renderer"),
        ('OPERATOR', 'uv.muv_uvbb_updater'),

        # Move UV from 3D View
        ('OPERATOR', 'view3d.muv_mvuv'),

        # Texture Projection
        ('OPERATOR', 'uv.muv_texproj_renderer'),
        ('OPERATOR', 'uv.muv_texproj_start'),
        ('OPERATOR', 'uv.muv_texproj_stop'),
        ('OPERATOR', 'uv.muv_texproj_project'),

        # Pack UV (with same UV island packing)
        ('OPERATOR', 'uv.muv_packuv'),

        # Texture Lock
        ('OPERATOR', 'uv.muv_texlock_start'),
        ('OPERATOR', 'uv.muv_texlock_stop'),
        ('OPERATOR', 'uv.muv_texlock_updater'),
        ('OPERATOR', 'uv.muv_texlock_intr_start'),
        ('OPERATOR', 'uv.muv_texlock_intr_stop'),

        # Mirror UV
        ('OPERATOR', 'uv.muv_mirror_uv'),

        # World Scale UV
        ('OPERATOR', 'uv.muv_wsuv_measure'),
        ('OPERATOR', 'uv.muv_wsuv_apply'),

        # Unwrap Constraint
        ('OPERATOR', 'uv.muv_unwrap_constraint'),

        # Preserve UV
        ('OPERATOR', 'uv.muv_preserve_uv_aspect'),

        # Align UV
        ('OPERATOR', 'uv.muv_auv_circle'),
        ('OPERATOR', 'uv.muv_auv_smooth'),
        ('OPERATOR', 'uv.muv_auv_straighten'),
        ('OPERATOR', 'uv.muv_auv_axis'),

        # Align UV Cursor
        ('OPERATOR', 'uv.muv_auvc_align'),

        # Texture Wrap
        ('OPERATOR', 'uv.muv_texwrap_refer'),
        ('OPERATOR', 'uv.muv_texwrap_set'),

        # UV Inspection
        ('OPERATOR', 'uv.muv_uvinsp_renderer'),
        ('OPERATOR', 'uv.muv_uvinsp_update'),
        ('OPERATOR', 'uv.muv_uvinsp_display'),
        ('OPERATOR', 'uv.muv_uvinsp_select_overlapped'),
        ('OPERATOR', 'uv.muv_uvinsp_select_flipped'),

        # UV Sculpt
        ('OPERATOR', 'uv.muv_uvsculpt_renderer'),
        ('OPERATOR', 'uv.muv_uvsculpt_ops'),

        # UVW
        ('OPERATOR', 'uv.muv_uvw_box_map'),
        ('OPERATOR', 'uv.muv_uvw_best_planer_map'),
    ]

    def setUp(self):
        bpy.ops.wm.open_mainfile(filepath=TESTEE_FILE)

    def tearDown(self):
        pass

    def test_cpuv(self):
        print("======== Copy/Paste UV Coordinates ========")
        src_obj_name = "Cube"
        dest_obj_name = "Cube.001"
        uv_map = "UVMap"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Need copy UV at first
        print("[TEST] (Fail) Not copy first")
        result = bpy.ops.uv.muv_cpuv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_cpuv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: No faces are selected
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_cpuv_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_cpuv_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified UV")
        result = bpy.ops.uv.muv_cpuv_copy_uv(uv_map=uv_map)
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        select_object_only(dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[dest_obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_cpuv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: No faces are selected
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_cpuv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Number of selected faces is different from copied(src:6, dest:1)
        print("[TEST] (Fail) N:N and number of selected face is not same")
        select_faces(active_obj, 1)
        result = bpy.ops.uv.muv_cpuv_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Some faces are different size
        print("[TEST] (Fail) N:N and selected face size is not same")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        result = bpy.ops.uv.muv_cpuv_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.mesh.tris_convert_to_quads()

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_cpuv_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_cpuv_paste_uv(
            uv_map=uv_map,
            strategy='N_N',
            flip_copied_uv=True,
            rotate_copied_uv=3,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_cpuv_obj(self):
        print("======== Copy/Paste UV Coordinates (Among same objects) ========")
        src_obj_name = "Cube"
        dest_obj_name = "Cube.001"
        uv_map = "UVMap"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        select_object_only(src_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]

        # Warning: Need copy UV at first
        print("[TEST] (Fail) No UV")
        result = bpy.ops.object.muv_cpuv_obj_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.object.muv_cpuv_obj_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.object.muv_cpuv_obj_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified UV")
        result = bpy.ops.object.muv_cpuv_obj_copy_uv(uv_map=uv_map)
        self.assertSetEqual(result, {'FINISHED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        select_object_only(dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[dest_obj_name]
        active_obj = bpy.context.scene.objects.active
        result = bpy.ops.object.muv_cpuv_obj_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Number of faces is different from copied (src:6, dest:12)
        print("[TEST] (Fail) Number of selected face is not same")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')
        result = bpy.ops.object.muv_cpuv_obj_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.object.mode_set(mode='OBJECT')

        print("[TEST] (OK) Default")
        result = bpy.ops.object.muv_cpuv_obj_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified UV")
        result = bpy.ops.object.muv_cpuv_obj_paste_uv(
            uv_map=uv_map,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

        # Warning: Some faces are different size
        print("[TEST] (Fail) Number of selected face is not same")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bm = bmesh.from_edit_mesh(active_obj.data)
        bpy.ops.mesh.select_all(action='DESELECT')
        for i, f in enumerate(bm.faces):
            if i <= 5:
                f.select = True
            else:
                f.select = False
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.object.mode_set(mode='OBJECT')
        result = bpy.ops.object.muv_cpuv_obj_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_cpuv_selseq(self):
        print("======== Copy/Paste UV Coordinates (by selection sequence) ========")
        src_obj_name = "Cube"
        dest_obj_name = "Cube.001"
        uv_map = "UVMap"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Need copy UV at first
        print("[TEST] (Fail) Not copy first")
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_cpuv_selseq_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: No faces are selected
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_cpuv_selseq_copy_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default UV")
        add_face_select_history(active_obj, 2)
        result = bpy.ops.uv.muv_cpuv_selseq_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified UV")
        result = bpy.ops.uv.muv_cpuv_selseq_copy_uv(uv_map=uv_map)
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        select_object_only(dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[dest_obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: No faces are selected
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Number of selected faces is different from copied faces (src:2, dest:1)
        print("[TEST] (Fail) N:N and number of selected face is not same")
        add_face_select_history(active_obj, 1)
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Some faces are different size
        print("[TEST] (Fail) N:N and selected face size is not same")
        bpy.ops.mesh.quads_convert_to_tris()
        add_face_select_history(active_obj, 2)
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv(strategy='N_N')
        self.assertSetEqual(result, {'CANCELLED'})
        bpy.ops.mesh.tris_convert_to_quads()

        print("[TEST] (OK) Default")
        add_face_select_history(active_obj, 2)
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option")
        result = bpy.ops.uv.muv_cpuv_selseq_paste_uv(
            uv_map=uv_map,
            strategy='N_N',
            flip_copied_uv=True,
            rotate_copied_uv=3,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_fliprot(self):
        print("======== Flip/Rotate UVs ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_fliprot()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: No faces are selected
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_fliprot()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_fliprot()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option")
        result = bpy.ops.uv.muv_fliprot(flip=True, rotate=5, seams=False)
        self.assertSetEqual(result, {'FINISHED'})

    def test_transuv(self):
        print("======== Transfer UV ========")
        src_obj_name = "Cube"
        dest_obj_name = "Cube.001"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(active_obj.data)

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_transuv_copy()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Two faces must be selected
        print("[TEST] (Fail) Not two face select")
        bpy.ops.mesh.uv_texture_add()
        select_faces(active_obj, 1)
        result = bpy.ops.uv.muv_transuv_copy()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Two faces must be active
        print("[TEST] (Fail) Not two face active")
        select_faces(active_obj, 2)
        for f in bm.faces:
            if not f.select:
                bm.faces.active = f
                break
        result = bpy.ops.uv.muv_transuv_copy()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Two faces should share one edge
        print("[TEST] (Fail) Two faces should share one edge")
        bpy.ops.mesh.select_all(action='DESELECT')
        selected_faces = select_and_active_faces(active_obj, 1)
        selected_faces = select_unlink_faces(active_obj, selected_faces[0], 1)
        result = bpy.ops.uv.muv_transuv_copy()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK)")
        bpy.ops.mesh.select_all(action='DESELECT')
        select_and_active_faces(active_obj, 1)
        select_link_face(active_obj, 1)
        result = bpy.ops.uv.muv_transuv_copy()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.ops.object.mode_set(mode='OBJECT')
        select_object_only(dest_obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[dest_obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_transuv_paste()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Two faces must be selected
        print("[TEST] (Fail) Not two face select")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        add_face_select_history(active_obj, 1)
        result = bpy.ops.uv.muv_transuv_paste()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Two faces should share one edge
        print("[TEST] (Fail) Two faces should share one edge")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        add_face_select_history(active_obj, 2)
        result = bpy.ops.uv.muv_transuv_paste()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(active_obj.data)
        bm.select_history.clear()
        selected_face = select_and_active_faces(active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = select_link_face(active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transuv_paste()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option")
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(active_obj.data)
        bm.select_history.clear()
        selected_face = select_and_active_faces(active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = select_link_face(active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transuv_paste(
            invert_normals=True,
            copy_seams=False
        )
        self.assertSetEqual(result, {'FINISHED'})

        # there is no case more than 2 faces share one edge

        # Warning: Mesh has different amount of faces
        print("[TEST] (Fail) Mesh has different amount of faces")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bm = bmesh.from_edit_mesh(active_obj.data)
        bm.select_history.clear()
        selected_face = select_and_active_faces(active_obj, 1)
        bm.select_history.add(selected_face[0])
        selected_face = select_link_face(active_obj, 1)
        bm.select_history.add(selected_face[0])
        for hist in bm.select_history:
            hist.select = True
        result = bpy.ops.uv.muv_transuv_paste()
        self.assertSetEqual(result, {'FINISHED'})
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.tris_convert_to_quads()

        # print("[TEST] (Fail) Face have different amount of vertices")
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.quads_convert_to_tris()
        # bm = bmesh.from_edit_mesh(active_obj.data)
        # bm.faces.ensure_lookup_table()
        # del_total = len(bm.faces) / 2
        # del_faces = [bm.faces[i] for i in range(int(del_total))]
        # bmesh.ops.delete(bm, geom=del_faces, context=5)
        # bm.select_history.clear()
        # selected_face = select_and_active_faces(active_obj, 1)
        # bm.select_history.add(selected_face[0])
        # selected_face = select_link_face(active_obj, 1)
        # bm.select_history.add(selected_face[0])
        # for hist in bm.select_history:
        #     hist.select = True
        # result = bpy.ops.uv.muv_transuv_paste()
        # self.assertSetEqual(result, {'FINISHED'})
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.tris_convert_to_quads()

    # modal operator can not invoke directly from cmdline
    def test_uvbb(self):
        print("======== Manipulate UV with Bouding Box in UV Editor ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # if not bm.loops.layers.uv: (__get_uv_info)
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_uvbb_updater()
        self.assertSetEqual(result, {'CANCELLED'})

        # if not uv_info: ( __get_uv_info)
        print("[TEST] (Fail) No selected faces")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_uvbb_updater()
        self.assertSetEqual(result, {'CANCELLED'})

    # modal operator can not invoke directly from cmdline
    def test_mvuv(self):
        print("======== Move UV from 3D View ========")

    # modal operator can not invoke directly from cmdline
    def test_texproj(self):
        print("======== Texture Projection ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: No textures are selected
        print("[TEST] (Fail) No Image")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_texproj_project()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.image.new(name='Test')
        bpy.context.scene.muv_texproj_tex_image = 'Test'
        bpy.context.scene.muv_texproj_assign_uvmap = False
        result = bpy.ops.uv.muv_texproj_project()
        self.assertSetEqual(result, {'CANCELLED'})

        # bpy.context.region has no VIEW_3D from cmdline

    def test_packuv(self):
        print("======== Pack UV (with same UV island packing) ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_packuv()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_packuv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option")
        result = bpy.ops.uv.muv_packuv(
            rotate=True,
            margin=0.03,
            allowable_center_deviation=(0.02, 0.05),
            allowable_size_deviation=(0.003, 0.0004)
        )
        self.assertSetEqual(result, {'FINISHED'})

    # can not test interactive mode
    def test_texlock(self):
        print("======== Texture Lock ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV (Start)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_texlock_start()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV (Stop)")
        result = bpy.ops.uv.muv_texlock_stop()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV (Intr Start)")
        result = bpy.ops.uv.muv_texlock_intr_start()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) (Start)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.image.new(name='Test')
        result = bpy.ops.uv.muv_texlock_start()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) (Stop)")
        result = bpy.ops.uv.muv_texlock_stop()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) (Stop) With connect")
        bpy.ops.uv.smart_project()    # this needs because previous result corrupts UV and arise errors
        result = bpy.ops.uv.muv_texlock_start()
        self.assertSetEqual(result, {'FINISHED'})
        result = bpy.ops.uv.muv_texlock_stop(
            connect=False
        )
        self.assertSetEqual(result, {'FINISHED'})

        # may not occur below situation : bmesh's index is not same between
        # start and stop
        # print("[TEST] (Fail) Internal Error")
        # result = bpy.ops.uv.muv_texlock_start()
        # self.assertSetEqual(result, {'FINISHED'})
        # bpy.ops.mesh.select_all(action='DESELECT')
        # result = bpy.ops.uv.muv_texlock_stop()
        # self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (Fail) not running (Intr Stop)")
        result = bpy.ops.uv.muv_texlock_intr_stop()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_mirroruv(self):
        print("======== Mirror UV ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_mirror_uv()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option 1")
        result = bpy.ops.uv.muv_mirror_uv(axis='Y', error=0.7)
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) User specified option 2")
        result = bpy.ops.uv.muv_mirror_uv(axis='Y', error=19.4)
        self.assertSetEqual(result, {'FINISHED'})

    def test_wsuv(self):
        print("======== World Scale UV ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        active_obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(active_obj.data)

        # Warning: Object must have more than one UV map and texture
        print("[TEST] (Fail) No UV (Measure)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_wsuv_measure()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map and texture
        print("[TEST] (Fail) No UV (Apply)")
        result = bpy.ops.uv.muv_wsuv_apply()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) (Measure)")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.image.new(name='Test')
        img = bpy.data.images['Test']
        tex_layer = bm.faces.layers.tex.verify()
        for f in bm.faces:
            f[tex_layer].image = img
        bmesh.update_edit_mesh(active_obj.data)
        result = bpy.ops.uv.muv_wsuv_measure()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) (Apply)")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_wsuv_apply()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) (Apply) Origin option specified")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_wsuv_apply(origin='RIGHT_TOP')
        self.assertSetEqual(result, {'FINISHED'})

    def test_unwrapconst(self):
        print("======== Unwrap Constraint ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # This test is not needed now
        # print("[TEST] (Fail) No UV")
        # bpy.ops.mesh.select_all(action='SELECT')
        # result = bpy.ops.uv.muv_unwrap_constraint()
        # self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_unwrap_constraint()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) user specified option")
        result = bpy.ops.uv.muv_unwrap_constraint(
            method='CONFORMAL',
            fill_holes=False,
            correct_aspect=False,
            use_subsurf_data=True,
            margin=0.1,
            u_const=True,
            v_const=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_preserve_uv_aspect(self):
        print("======== Preserve UV Aspect ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(active_obj.data)
        tex_layer = bm.faces.layers.tex.verify()

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.image.new(name='Test')
        for f in bm.faces:
            f[tex_layer].image = bpy.data.images['Test']
        result = bpy.ops.uv.muv_preserve_uv_aspect(dest_img_name='Test')
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_preserve_uv_aspect(dest_img_name='Test')
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) user specified option")
        result = bpy.ops.uv.muv_preserve_uv_aspect(
            dest_img_name='Test',
            origin='RIGHT_TOP'
        )
        self.assertSetEqual(result, {'FINISHED'})

    # this test can not be done because area always NoneType in console run
    def test_auvc(self):
        print("======== Align UV Cursor ========")

    # modal operator can not invoke directly from cmdline
    def test_uvsculpt(self):
        print("======== UV Sculpt ========")

    def test_cpuv_ie(self):
        print("======== Copy/Paste UV (UV/Image Editor) ========")
        src_obj_name = "Cube"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        print("[TEST] (OK)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_cpuv_ie_copy_uv()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_cpuv_ie_paste_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_uvw(self):
        print("======== UVW ========")
        src_obj_name = "Cube"

        select_object_only(src_obj_name)
        bpy.ops.object.duplicate()
        bpy.context.scene.objects.active = bpy.data.objects[src_obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_box_map(assign_uvmap=False)
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_best_planer_map(assign_uvmap=False)
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_box_map()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) user specified option")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_box_map(
            size=2.0,
            rotation=(0.2, 0.1, 0.4),
            offset=(1.2, 5.0, -20.0),
            tex_aspect=1.3,
            assign_uvmap=False
        )
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_best_planer_map()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) user specified option")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvw_best_planer_map(
            size=0.5,
            rotation=-0.4,
            offset=(-5.0, 10.0),
            tex_aspect=0.6,
            assign_uvmap=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_uvinsp(self):
        print("======== UV Inspection ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')
        sc = bpy.context.scene

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvinsp_display()
        self.assertSetEqual(result, {'FINISHED'})
        result = bpy.ops.uv.muv_uvinsp_display()
        self.assertSetEqual(result, {'FINISHED'})

        sc.muv_uvinsp_show_overlapped = True
        sc.muv_uvinsp_show_flipped = True
        sc.muv_uvinsp_show_mode = 'FACE'

        print("[TEST] (OK) another pattern")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_uvinsp_display()
        self.assertSetEqual(result, {'FINISHED'})
        result = bpy.ops.uv.muv_uvinsp_display()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK)")
        result = bpy.ops.uv.muv_uvinsp_update()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.context.tool_settings.use_uv_select_sync = True

        print("[TEST] (OK) UV Select Sync = True")
        result = bpy.ops.uv.muv_uvinsp_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) UV Select Sync = True")
        result = bpy.ops.uv.muv_uvinsp_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

        bpy.context.tool_settings.use_uv_select_sync = False

        print("[TEST] (OK) UV Select Sync = False")
        result = bpy.ops.uv.muv_uvinsp_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

        print("[TEST] (OK) UV Select Sync = False")
        result = bpy.ops.uv.muv_uvinsp_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_texwrap(self):
        print("======== Texture Wrap ========")
        obj_name = "Cube"

        select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        sc = bpy.context.scene

        sc.muv_texwrap_set_and_refer = False

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_texwrap_refer()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Object must have more than one UV map
        print("[TEST] (Fail) No UV")
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Must select only one face
        print("[TEST] (Fail) Not 1 selected face")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_texwrap_refer()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK)")
        select_faces(active_obj, 1)
        result = bpy.ops.uv.muv_texwrap_refer()
        self.assertSetEqual(result, {'FINISHED'})

        # Warning: Must select only one face
        print("[TEST] (Fail) Not 1 selected face")
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

        # Warning: Must select different face
        print("[TEST] (Fail) Not select different face")
        select_faces(active_obj, 1)
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='DESELECT')
        select_faces(active_obj, 1, 2)
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'FINISHED'})

        # Warning: 2 verticies must be shared among faces
        print("[TEST] (Fail) Not share 2 verticies")
        bpy.ops.mesh.select_all(action='DESELECT')
        select_faces(active_obj, 1, 1)
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

        # "More than 1 vertex must be unshared" does rarely occur

        sc.muv_texwrap_selseq = True

        # Warning: Must select more than one face
        print("[TEST] (Fail) No selected face")
        bpy.ops.mesh.select_all(action='DESELECT')
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

        print("[TEST] (OK) Selection Sequence")
        add_face_select_history(active_obj, 1, 2)
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'FINISHED'})

        sc.muv_texwrap_selseq = False

        # Warning: Object must be same
        print("[TEST] (Fail) Not select different face")
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate()
        select_object_only("Cube.001")
        active_obj = bpy.context.scene.objects.active
        bpy.ops.object.mode_set(mode='EDIT')
        select_faces(active_obj, 1, 1)
        result = bpy.ops.uv.muv_texwrap_set()
        self.assertSetEqual(result, {'CANCELLED'})

    # Align UV has a complicated condition to test
    def test_auv(self):
        print("======== Align UV ========")


if __name__ == "__main__":
    test_cases = [
        TestUVMagicUV
    ]

    suite = unittest.TestSuite()
    for case in test_cases:
        suite.addTest(unittest.makeSuite(case))
    ret = unittest.TextTestRunner().run(suite).wasSuccessful()
    sys.exit(not ret)
