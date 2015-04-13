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

# copy UV
class CPUVCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object."""
    
    bl_idname = "uv.cpuv_copy_uv"
    bl_label = "Copy UV"
    bl_description = "Copy UV data"
    bl_options = {'REGISTER', 'UNDO'}
    
    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CPUVCopyUV.src_uv_map = None
        CPUVCopyUV.src_obj = None
        CPUVCopyUV.src_sel_face_info = None

    def execute(self, context):
    
        self.report({'INFO'}, "Copy UV coordinate.")
        
        # save current mode
        mode_orig = bpy.context.object.mode
        
        try:
            # prepare for coping
            CPUVCopyUV.src_obj = cpuv_common.prep_copy(self)
        
            # copy
            CPUVCopyUV.src_sel_face_info = cpuv_common.get_selected_faces(
                CPUVCopyUV.src_obj)
            CPUVCopyUV.src_uv_map = cpuv_common.copy_opt(
                self, "", CPUVCopyUV.src_obj,
                CPUVCopyUV.src_sel_face_info)
            
            # finish coping
            cpuv_common.fini_copy()
            
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}
        
        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)
        
        return {'FINISHED'}


# paste UV
class CPUVPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied."""
    
    bl_idname = "uv.cpuv_paste_uv"
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
        self.src_uv_map = CPUVCopyUV.src_uv_map
        self.src_obj = CPUVCopyUV.src_obj
        self.src_sel_face_info = CPUVCopyUV.src_sel_face_info

    def execute(self, context):
    
        self.report({'INFO'}, "Paste UV coordinate.")
        
        # save current mode
        mode_orig = bpy.context.object.mode
        
        try:
            # prepare for pasting
            dest_obj = cpuv_common.prep_paste(
                self, self.src_obj, self.src_sel_face_info)
            
            # paste
            dest_sel_face_info = cpuv_common.get_selected_faces(dest_obj)
            cpuv_common.paste_opt(
                self, "", self.src_obj, self.src_sel_face_info,
                self.src_uv_map, dest_obj, dest_sel_face_info)
            
            # finish pasting
            cpuv_common.fini_paste()
            
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}
        
        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)
        
        return {'FINISHED'}
            


