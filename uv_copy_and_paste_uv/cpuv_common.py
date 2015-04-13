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
__version__ = "3.0"
__date__ = "X XXXX 2015"

SelectedFaceInfo = namedtuple('SelectedFaceInfo', 'normal indices')

class CPUVError(Exception):
    def __init__(self, level, str):
        self.err_level = level
        self.err_str= str
    def __str__(self):
        return repr(self.err_str)
    def report(self, obj):
        obj.report(self.err_level, self.err_str)

def prep_copy(self):
    """
    parepare for copy operation.
    @return active object
    """
    # get active (source) object to be copied from
    obj = bpy.context.active_object;
    
    # check if active object has more than one UV map
    if len(obj.data.uv_textures.keys()) == 0:
        raise CPUVError({'WARNING'}, "Object must have more than one UV map.")

    # change to 'OBJECT' mode, in order to access internal data
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return obj


# finish copy operation
def fini_copy():
    """
    finish copy operation.
    """
    pass

# prepare for paste operation
def prep_paste(self, src_obj, src_sel_face_info):
    """
    prepare for paste operation.
    @param  src_obj object that is copied from
    @param  src_sel_face_info information about faces will be copied
    @return active object
    """
     # check if copying operation was executed
    if src_sel_face_info is None or src_obj is None:
        raise CPUVError({'WARNING'}, "Do copy operation at first.")
    
    # get active (source) object to be pasted to
    obj = bpy.context.active_object

    # check if active object has more than one UV map
    if len(obj.data.uv_textures.keys()) == 0:
        raise CPUVError({'WARNING'}, "Object must have more than one UV map.")

    # change to 'OBJECT' mode, in order to access internal data
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return obj


# finish paste operation
def fini_paste():
    """
    finish paste operation.
    """
    pass


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
    @return UV map
    """
    # check if any faces are selected
    if len(src_sel_face_info) == 0:
        raise CPUVError({'WARNING'}, "No faces are selected.")
    else:
        self.report(
            {'INFO'}, "%d face(s) are selected." % len(src_sel_face_info))
    
    if uv_map == "":
        uv_map = src_obj.data.uv_layers.active.name
    else:
        uv_map = uv_map
    
    return uv_map


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
    """
    
    # check if any faces are selected
    if len(dest_sel_face_info) == 0:
        raise CPUVError({'WARNING'}, "No faces are selected.")
    
    if len(dest_sel_face_info) != len(src_sel_face_info):
        raise CPUVError(
            {'WARNING'},
            "Number of selected faces is different from copied faces." +
            "(src:%d, dest:%d)" %
            (len(src_sel_face_info), len(dest_sel_face_info)))

    for i in range(len(dest_sel_face_info)):
        if (len(dest_sel_face_info[i].indices) !=
            len(src_sel_face_info[i].indices)):
            raise CPUVError({'WARNING'}, "Some faces are different size.")
    
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
            
        dest_indices = flip_rotate_uvs(
            list(dest_indices), self.flip_copied_uv, self.rotate_copied_uv)

        # update
        for j in range(len(dest_indices)):
            dest_data = dest_uv.data[dest_indices[j]]
            src_data = src_uv.data[src_indices[j]]
            dest_data.uv = src_data.uv

    self.report({'INFO'}, "%d faces are copied." % len(dest_sel_face_info))


def flip_rotate_uvs(indices, flip, num_rotate):
    # Flip UVs
    if flip is True:
        indices.reverse()

    # Rotate UVs
    for i in range(num_rotate):
        idx = indices.pop()
        indices.insert(0, idx)

    return indices
