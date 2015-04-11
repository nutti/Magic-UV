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
from bpy.props import *

from . import cpuv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "3.0"
__date__ = "X XXXX 2015"


# copy UV (by selection sequence)
class CPUVSelSeqCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object by selection sequence."""
    
    bl_idname = "uv.cpuv_selseq_copy_uv"
    bl_label = "Copy UV (Selection Sequence)"
    bl_description = "Copy UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CPUVSelSeqCopyUV.src_uv_map = None
        CPUVSelSeqCopyUV.src_obj = None
        CPUVSelSeqCopyUV.src_sel_face_info = None

    def execute(self, context):

        self.report({'INFO'}, "Copy UV coordinate. (sequence)")
        
        # prepare for coping
        ret, CPUVSelSeqCopyUV.src_obj, mode_orig = cpuv_common.prep_copy(self)
        if ret != 0:
            return {'CANCELLED'}

        # copy
        CPUVSelSeqCopyUV.src_sel_face_info = cpuv_common.get_selected_faces_by_sel_seq(CPUVSelSeqCopyUV.src_obj)
        ret, CPUVSelSeqCopyUV.src_uv_map = cpuv_common.copy_opt(
            self, "", CPUVSelSeqCopyUV.src_obj,
            CPUVSelSeqCopyUV.src_sel_face_info)

        # finish coping
        cpuv_common.fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}


# paste UV (by selection sequence)
class CPUVSelSeqPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied by selection sequence."""
    
    bl_idname = "uv.cpuv_selseq_paste_uv"
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
        self.src_uv_map = CPUVSelSeqCopyUV.src_uv_map
        self.src_obj = CPUVSelSeqCopyUV.src_obj
        self.src_sel_face_info = CPUVSelSeqCopyUV.src_sel_face_info

    def execute(self, context):
        
        self.report({'INFO'}, "Paste UV coordinate. (sequence)")

        # prepare for pasting
        ret, dest_obj, mode_orig = cpuv_common.prep_paste(
            self, self.src_obj, self.src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}

        # paste
        dest_sel_face_info = cpuv_common.get_selected_faces_by_sel_seq(dest_obj)
        ret = cpuv_common.paste_opt(
            self, "", self.src_obj, self.src_sel_face_info,
            self.src_uv_map, dest_obj, dest_sel_face_info)
            
        # finish pasting
        cpuv_common.fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}

