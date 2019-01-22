import sys
import unittest

import bpy
import bmesh


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
    return select_and_active_faces_bm(bm, num_face)


def select_unlink_faces(obj, face, num_face):
    bm = bmesh.from_edit_mesh(obj.data)
    return select_unlink_faces_bm(bm, face, num_face)


def select_and_active_faces_bm(bm, num_face):
    selected_face = []
    for i, f in enumerate(bm.faces):
        if i >= num_face:
            f.select = False
        else:
            f.select = True
            bm.faces.active = f
            selected_face.append(f)
    return selected_face


def select_unlink_faces_bm(bm, face, num_face):
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


class TestBase(unittest.TestCase):

    package_name = "magic_uv"
    module_name = ""
    submodule_name = None
    idname = []

    @classmethod
    def setUpClass(cls):
        if cls.submodule_name is not None:
            print("\n======== Module Test: {}.{} ({}) ========"
               .format(cls.package_name, cls.module_name, cls.submodule_name))
        else:
            print("\n======== Module Test: {}.{} ========"
               .format(cls.package_name, cls.module_name))
        try:
            bpy.ops.wm.read_factory_settings()
            check_addon_enabled(cls.package_name)
            for op in cls.idname:
                if op[0] == 'OPERATOR':
                    assert operator_exists(op[1]), \
                        "Operator {} does not exist".format(op[1])
                elif op[0] == 'MENU':
                    assert menu_exists(op[1]), \
                        "Menu {} does not exist".format(op[1])
            bpy.ops.wm.save_as_mainfile(filepath=TESTEE_FILE)
        except AssertionError as e:
            print(e)
            sys.exit(1)

    @classmethod
    def tearDownClass(cls):
        try:
            check_addon_disabled(cls.package_name)
            for op in cls.idname:
                if op[0] == 'OPERATOR':
                    assert not operator_exists(op[1]), "Operator {} exists".format(op[1])
                elif op[0] == 'MENU':
                    assert not menu_exists(op[1]), "Menu %s exists".format(op[1])
        except AssertionError as e:
            print(e)
            sys.exit(1)

    def setUp(self):
        bpy.ops.wm.open_mainfile(filepath=TESTEE_FILE)
        self.setUpEachMethod()

    def setUpEachMethod(self):
        pass

    def tearDown(self):
        pass
