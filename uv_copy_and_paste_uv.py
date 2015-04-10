# <pep8-80 compliant>

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh
import math
from collections import namedtuple
from bpy.props import *

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "2.2"
__date__ = "3 April 2015"

bl_info = {
    "name" : "Copy and Paste UV",
    "author" : "Nutti",
    "version" : (2,2),
    "blender" : (2, 7, 3),
    "location" : "UV Mapping > Copy and Paste UV",
    "description" : "Copy and Paste UV data",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UV"
}

SelectedFaceInfo = namedtuple('SelectedFaceInfo', 'normal indices')

# master menu
class CopyAndPasteUVMenu(bpy.types.Menu):
    bl_idname = "uv.copy_and_paste_uv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV Menu"

    def draw(self, context):
        self.layout.operator(CopyAndPasteUVCopyUV.bl_idname)
        self.layout.operator(CopyAndPasteUVPasteUV.bl_idname)
        self.layout.operator(CopyAndPasteUVCopyUVBySelSeq.bl_idname)
        self.layout.operator(CopyAndPasteUVPasteUVBySelSeq.bl_idname)
        self.layout.menu(CopyAndPasteUVCopyUVMap.bl_idname)
        self.layout.menu(CopyAndPasteUVPasteUVMap.bl_idname)


# copy UV
class CopyAndPasteUVCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object."""
    
    bl_idname = "uv.copy_uv"
    bl_label = "Copy UV"
    bl_description = "Copy UV data"
    bl_options = {'REGISTER', 'UNDO'}
    
    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CopyAndPasteUVCopyUV.src_uv_map = None
        CopyAndPasteUVCopyUV.src_obj = None
        CopyAndPasteUVCopyUV.src_sel_face_info = None

    def execute(self, context):
    
        self.report({'INFO'}, "Copy UV coordinate.")
        
        # prepare for coping
        ret, CopyAndPasteUVCopyUV.src_obj, mode_orig = prep_copy(self)
        if ret != 0:
            return {'CANCELLED'}
        
        # copy
        CopyAndPasteUVCopyUV.src_sel_face_info = get_selected_faces(
            CopyAndPasteUVCopyUV.src_obj)
        ret, CopyAndPasteUVCopyUV.src_uv_map = copy_opt(
            self, "", CopyAndPasteUVCopyUV.src_obj,
            CopyAndPasteUVCopyUV.src_sel_face_info)
        
        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# paste UV
class CopyAndPasteUVPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied."""
    
    bl_idname = "uv.paste_uv"
    bl_label = "Paste UV"
    bl_description = "Paste UV data"
    bl_options = {'REGISTER', 'UNDO'}

    flip_copied_uv = BoolProperty(
        name = "Flip Copied UV",
        description = "Flip Copied UV...",
        default = False)

    rotate_copied_uv = IntProperty(
        default = 0,
        name = "Rotate Copied UV",
        min = 0,
        max = 30)
   
    def __init__(self):
        self.src_uv_map = CopyAndPasteUVCopyUV.src_uv_map
        self.src_obj = CopyAndPasteUVCopyUV.src_obj
        self.src_sel_face_info = CopyAndPasteUVCopyUV.src_sel_face_info

    def execute(self, context):
    
        self.report({'INFO'}, "Paste UV coordinate.")

        # prepare for pasting
        ret, dest_obj, mode_orig = prep_paste(
            self, self.src_obj, self.src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}
        
        # paste
        dest_sel_face_info = get_selected_faces(dest_obj)
        ret = paste_opt(
            self, "", self.src_obj, self.src_sel_face_info,
            self.src_uv_map, dest_obj, dest_sel_face_info)
        
        # finish pasting
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# copy UV (by selection sequence)
class CopyAndPasteUVCopyUVBySelSeq(bpy.types.Operator):
    """Copying UV coordinate on selected object by selection sequence."""
    
    bl_idname = "uv.copy_uv_sel_seq"
    bl_label = "Copy UV (Selection Sequence)"
    bl_description = "Copy UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CopyAndPasteUVCopyUVBySelSeq.src_uv_map = None
        CopyAndPasteUVCopyUVBySelSeq.src_obj = None
        CopyAndPasteUVCopyUVBySelSeq.src_sel_face_info = None

    def execute(self, context):

        self.report({'INFO'}, "Copy UV coordinate. (sequence)")
        
        # prepare for coping
        ret, CopyAndPasteUVCopyUVBySelSeq.src_obj, mode_orig = prep_copy(self)
        if ret != 0:
            return {'CANCELLED'}

        # copy
        CopyAndPasteUVCopyUVBySelSeq.src_sel_face_info = get_selected_faces_by_sel_seq(CopyAndPasteUVCopyUVBySelSeq.src_obj)
        ret, CopyAndPasteUVCopyUVBySelSeq.src_uv_map = copy_opt(
            self, "", CopyAndPasteUVCopyUVBySelSeq.src_obj,
            CopyAndPasteUVCopyUVBySelSeq.src_sel_face_info)

        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}


# paste UV (by selection sequence)
class CopyAndPasteUVPasteUVBySelSeq(bpy.types.Operator):
    """Paste UV coordinate which is copied by selection sequence."""
    
    bl_idname = "uv.paste_uv_sel_seq"
    bl_label = "Paste UV (Selection Sequence)"
    bl_description = "Paste UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    flip_copied_uv = BoolProperty(
        name = "Flip Copied UV",
        description = "Flip Copied UV...",
        default = False)

    rotate_copied_uv = IntProperty(
        default = 0,
        name = "Rotate Copied UV",
        min = 0,
        max = 30)

    def __init__(self):
        self.src_uv_map = CopyAndPasteUVCopyUVBySelSeq.src_uv_map
        self.src_obj = CopyAndPasteUVCopyUVBySelSeq.src_obj
        self.src_sel_face_info = CopyAndPasteUVCopyUVBySelSeq.src_sel_face_info

    def execute(self, context):
        
        self.report({'INFO'}, "Paste UV coordinate. (sequence)")

        # prepare for pasting
        ret, dest_obj, mode_orig = prep_paste(
            self, self.src_obj, self.src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}

        # paste
        dest_sel_face_info = get_selected_faces_by_sel_seq(dest_obj)
        ret = paste_opt(
            self, "", self.src_obj, self.src_sel_face_info,
            self.src_uv_map, dest_obj, dest_sel_face_info)
            
        # finish pasting
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}


# copy UV map (sub menu operator)
class CopyAndPasteUVCopyUVMapSubOpt(bpy.types.Operator):
    bl_idname = "uv.copy_uv_map_sub_opt"
    bl_label = "Copy UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()

    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CopyAndPasteUVCopyUVMapSubOpt.src_uv_map = None
        CopyAndPasteUVCopyUVMapSubOpt.src_obj = None
        CopyAndPasteUVCopyUVMapSubOpt.src_sel_face_info = None

    def execute(self, context):
        
        self.report(
            {'INFO'},
            "Copy UV coordinate. (UV map:" + self.uv_map + ")")

        # prepare for coping
        ret, CopyAndPasteUVCopyUVMapSubOpt.src_obj, mode_orig = prep_copy(self)
        if ret != 0:
            return {'CANCELLED'}
        
        # copy
        CopyAndPasteUVCopyUVMapSubOpt.src_sel_face_info = get_selected_faces(
            CopyAndPasteUVCopyUVMapSubOpt.src_obj)
        ret, CopyAndPasteUVCopyUVMapSubOpt.src_uv_map = copy_opt(
            self, self.uv_map, CopyAndPasteUVCopyUVMapSubOpt.src_obj,
            CopyAndPasteUVCopyUVMapSubOpt.src_sel_face_info)
        
        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# copy UV map
class CopyAndPasteUVCopyUVMap(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.copy_uv_map"
    bl_label = "Copy UV Map"
    bl_description = "Copy UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        global menu_count
    
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CopyAndPasteUVCopyUVMapSubOpt.bl_idname,
                text=m).uv_map = m
            

# paste UV map (sub menu operator)
class CopyAndPasteUVPasteUVMapSubOpt(bpy.types.Operator):
    bl_idname = "uv.paste_uv_map_sub_opt"
    bl_label = "Paste UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()
    
    flip_copied_uv = BoolProperty(
        name = "Flip Copied UV",
        description = "Flip Copied UV...",
        default = False)

    rotate_copied_uv = IntProperty(
        default = 0,
        name = "Rotate Copied UV",
        min = 0,
        max = 30)

    def __init__(self):
        self.src_uv_map = CopyAndPasteUVCopyUVMapSubOpt.src_uv_map
        self.src_obj = CopyAndPasteUVCopyUVMapSubOpt.src_obj
        self.src_sel_face_info = CopyAndPasteUVCopyUVMapSubOpt.src_sel_face_info

    def execute(self, context):
        
        self.report(
            {'INFO'}, "Paste UV coordinate. (UV map:" + self.uv_map + ")")

        # prepare for pasting
        ret, dest_obj, mode_orig = prep_paste(
            self, self.src_obj, self.src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}
        
        # paste
        dest_sel_face_info = get_selected_faces(dest_obj)
        ret = paste_opt(
            self, self.uv_map, self.src_obj, self.src_sel_face_info,
            self.src_uv_map, dest_obj, dest_sel_face_info)
        
        # finish pasting
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# paste UV map
class CopyAndPasteUVPasteUVMap(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.paste_uv_map"
    bl_label = "Paste UV Map"
    bl_description = "Paste UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        global menu_count
    
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CopyAndPasteUVPasteUVMapSubOpt.bl_idname,
                text=m).uv_map = m


def prep_copy(self):
    """
    parepare for copy operation.
    @return tuple(error code, active object, current mode)
    """
    # get active (source) object to be copied from
    obj = bpy.context.active_object;
    
    # check if active object has more than one UV map
    if len(obj.data.uv_textures.keys()) == 0:
        self.report({'WARNING'}, "Object must have more than one UV map.")
        return (1, None, None)

    # change to 'OBJECT' mode, in order to access internal data
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return (0, obj, mode)


# finish copy operation
def fini_copy(mode_orig):
    """
    finish copy operation.
    @param  mode_orig orignal mode
    """
    # revert to original mode
    bpy.ops.object.mode_set(mode=mode_orig)


# prepare for paste operation
def prep_paste(self, src_obj, src_sel_face_info):
    """
    prepare for paste operation.
    @param  src_obj object that is copied from
    @param  src_sel_face_info information about faces will be copied
    @return tuple(error code, active object, current mode)
    """
     # check if copying operation was executed
    if src_sel_face_info is None or src_obj is None:
        self.report({'WARNING'}, "Do copy operation at first.")
        return (1, None, None)
    
    # get active (source) object to be pasted to
    obj = bpy.context.active_object

    # check if active object has more than one UV map
    if len(obj.data.uv_textures.keys()) == 0:
        self.report({'WARNING'}, "Object must have more than one UV map.")
        return (2, None, None)

    # change to 'OBJECT' mode, in order to access internal data
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return (0, obj, mode)


# finish paste operation
def fini_paste(mode):
    """
    finish paste operation.
    @param  mode_orig orignal mode
    """
    # revert to original mode
    bpy.ops.object.mode_set(mode=mode)


def get_selected_faces(obj):
    """
    get information about selected faces.
    @param  obj object
    @return information about selected faces (list of SelectedFaceInfo)
    """
    out = []
    for i in range(len(obj.data.polygons)):
        # get selected faces
        poly = obj.data.polygons[i]
        if poly.select:
            face_info = SelectedFaceInfo(
                poly.normal.copy(), list(poly.loop_indices))
            out.append(face_info)
    return out


def get_selected_faces_by_sel_seq(obj):
    """
    get information about selected indices.
    @param  obj object
    @return information about selected faces (list of SelectedFaceInfo)
    """
    out = []
    faces = []
    
    # get selection sequence
    mode_orig = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    if bpy.app.version[0] >= 2 and bpy.app.version[1] >= 73:
        bm.faces.ensure_lookup_table()
    for e in bm.select_history:
        if isinstance(e, bmesh.types.BMFace) and e.select:
            faces.append(e.loops[0].face.index)
    
    # get selected faces by selection sequence
    bpy.ops.object.mode_set(mode='OBJECT')
    for f in faces:
        poly = obj.data.polygons[f]
        face_info = SelectedFaceInfo(
            poly.normal.copy(), list(poly.loop_indices))
        out.append(face_info)
        
    bpy.ops.object.mode_set(mode=mode_orig)
    
    return out


def copy_opt(self, uv_map, src_obj, src_sel_face_info):
    """
    copy operation.
    @param  self operation object
    @param  uv_map UV Map to be copied. (current map when null str)
    @param  src_obj source object
    @param  src_sel_face_info source information about selected faces
    @return tuple(error code, UV map)
    """
    # check if any faces are selected
    if len(src_sel_face_info) == 0:
        self.report({'WARNING'}, "No faces are not selected.")
        return (1, None)
    else:
        self.report(
            {'INFO'}, "%d face(s) are selected." % len(src_sel_face_info))
    
    if uv_map == "":
        uv_map = src_obj.data.uv_layers.active.name
    else:
        uv_map = uv_map
    
    return (0, uv_map)


def paste_opt(self, uv_map, src_obj, src_sel_face_info,
    src_uv_map, dest_obj, dest_sel_face_info):
    """
    paste operation.
    @param  self operation object
    @param  uv_map UV Map to be pasted. (current map when null str)
    @param  src_obj source object
    @param  src_sel_face_info source information about selected faces
    @param  src_uv_map source UV map
    @param  dest_obj destination object
    @param  dest_sel_face_info destination information about selected faces
    @return error code
    """
    if len(dest_sel_face_info) != len(src_sel_face_info):
        self.report(
            {'WARNING'},
            "Number of selected faces is different from copied faces." +
            "(src:%d, dest:%d)" %
            (len(src_sel_face_info), len(dest_sel_face_info)))
        return 1
    for i in range(len(dest_sel_face_info)):
        if (len(dest_sel_face_info[i].indices) !=
            len(src_sel_face_info[i].indices)):
            self.report({'WARNING'}, "Some faces are different size.")
            return 1
    
    if uv_map == "":
        dest_uv_map = dest_obj.data.uv_layers.active.name
    else:
        dest_uv_map = uv_map

    # update UV data
    src_uv = src_obj.data.uv_layers[src_uv_map]
    dest_uv = dest_obj.data.uv_layers[dest_uv_map]

    for i in range(len(dest_sel_face_info)):
        dest_indices = dest_sel_face_info[i].indices
        src_indices = src_sel_face_info[i].indices

        # Flip UVs
        if self.flip_copied_uv is True:
            dest_indices = list(dest_indices)
            dest_indices.reverse()

        # Rotate UVs
        for k in range(self.rotate_copied_uv):
            item_rotate = dest_indices.pop()
            dest_indices.insert(0, item_rotate)

        # update
        for j in range(len(dest_indices)):
            dest_data = dest_uv.data[dest_indices[j]]
            src_data = src_uv.data[src_indices[j]]
            dest_data.uv = src_data.uv

    self.report({'INFO'}, "%d faces are copied." % len(dest_sel_face_info))

    return 0


# registration
def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(CopyAndPasteUVMenu.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)


if __name__ == "__main__":
    register()
