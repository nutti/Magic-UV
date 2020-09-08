import sys
import unittest

import bpy
import bmesh

from . import compatibility as compat


TESTEE_FILE = "testee.blend"


def check_addon_enabled(mod):
    if compat.check_version(2, 80, 0) < 0:
        result = bpy.ops.wm.addon_enable(module=mod)
    else:
        result = bpy.ops.preferences.addon_enable(module=mod)
    assert (result == {'FINISHED'}), "Failed to enable add-on %s" % (mod)
    assert (mod in compat.get_user_preferences(bpy.context).addons.keys()), "Failed to enable add-on %s" % (mod)


def check_addon_disabled(mod):
    if compat.check_version(2, 80, 0) < 0:
        result = bpy.ops.wm.addon_disable(module=mod)
    else:
        result = bpy.ops.preferences.addon_disable(module=mod)
    assert (result == {'FINISHED'}), "Failed to disable add-on %s" % (mod)
    assert (not mod in compat.get_user_preferences(bpy.context).addons.keys()), "Failed to disable add-on %s" % (mod)


def operator_exists(idname):
    try:
        from bpy.ops import op_as_string
        op_as_string(idname)
        return True
    except:
        return False


def menu_exists(idname):
    return idname in dir(bpy.types)


def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_preferences

    return context.preferences


def set_object_select(obj, select):
    if compat.check_version(2, 80, 0) < 0:
        obj.select = select
    else:
        obj.select_set(select)


def select_object_only(obj_name):
    for o in bpy.data.objects:
        if o.name == obj_name:
            set_object_select(o, True)
        else:
            set_object_select(o, False)


def select_objects_only(obj_names):
    for o in bpy.data.objects:
        set_object_select(o, False)
    for name in obj_names:
        set_object_select(bpy.data.objects[name], True)


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


def add_face_select_history_by_indices(obj, indices):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm.select_history.clear()
    for i in indices:
        bm.select_history.add(bm.faces[i])
    for hist in bm.select_history:
        hist.select = True


# This is a workaround for >2.80 because UV Map will be assigned
# automatically while creating a object
def delete_all_uv_maps(obj):
    mode_orig = bpy.context.active_object.mode
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    for i in reversed(range(len(bm.loops.layers.uv))):
        bm.loops.layers.uv.remove(bm.loops.layers.uv[i])
    bmesh.update_edit_mesh(obj.data)

    bpy.ops.object.mode_set(mode=mode_orig)


def find_texture_nodes_from_material(mtrl):
    nodes = []
    if not mtrl.node_tree:
        return nodes
    for node in mtrl.node_tree.nodes:
        tex_node_types = [
            'TEX_ENVIRONMENT',
            'TEX_IMAGE',
        ]
        if node.type not in tex_node_types:
            continue
        if not node.image:
            continue
        nodes.append(node)

    return nodes


def find_texture_nodes(obj):
    nodes = []
    for slot in obj.material_slots:
        if not slot.material:
            continue
        nodes.extend(find_texture_nodes_from_material(slot.material))

    return nodes


def assign_new_image(obj, image_name):
    bpy.ops.image.new(name=image_name)
    img = bpy.data.images[image_name]
    if compat.check_version(2, 80, 0) < 0:
        bm = bmesh.from_edit_mesh(obj.data)
        tex_layer = bm.faces.layers.tex.verify()
        for f in bm.faces:
            f[tex_layer].image = img
        bmesh.update_edit_mesh(obj.data)
    else:
        node_tree = obj.active_material.node_tree
        output_node = node_tree.nodes["Material Output"]

        nodes = find_texture_nodes_from_material(obj.active_material)
        if len(nodes) >= 1:
            tex_node = nodes[0]
        else:
            tex_node = node_tree.nodes.new(type="ShaderNodeTexImage")
        tex_node.image = img
        node_tree.links.new(output_node.inputs["Surface"], tex_node.outputs["Color"])


def duplicate_object_without_uv():
    bpy.ops.object.duplicate()
    delete_all_uv_maps(compat.get_active_object(bpy.context))


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
        delete_all_uv_maps(compat.get_active_object(bpy.context))
        self.setUpEachMethod()

    def setUpEachMethod(self):
        pass

    def tearDown(self):
        pass
