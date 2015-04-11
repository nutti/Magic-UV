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


# copy UV map (sub menu operator)
class CPUVUVMapCopyUVOperation(bpy.types.Operator):
    bl_idname = "uv.cpuv_uvmap_copy_uv_op"
    bl_label = "Copy UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()

    # static variables
    src_uv_map = None            # source uv map
    src_obj = None               # source object
    src_sel_face_info = None     # source selected faces information
    
    def __init__(self):
        CPUVUVMapCopyUVOperation.src_uv_map = None
        CPUVUVMapCopyUVOperation.src_obj = None
        CPUVUVMapCopyUVOperation.src_sel_face_info = None

    def execute(self, context):
        
        self.report(
            {'INFO'},
            "Copy UV coordinate. (UV map:" + self.uv_map + ")")

        # prepare for coping
        ret, CPUVUVMapCopyUVOperation.src_obj, mode_orig = cpuv_common.prep_copy(self)
        if ret != 0:
            return {'CANCELLED'}
        
        # copy
        CPUVUVMapCopyUVOperation.src_sel_face_info = cpuv_common.get_selected_faces(
            CPUVUVMapCopyUVOperation.src_obj)
        ret, CPUVUVMapCopyUVOperation.src_uv_map = cpuv_common.copy_opt(
            self, self.uv_map, CPUVUVMapCopyUVOperation.src_obj,
            CPUVUVMapCopyUVOperation.src_sel_face_info)
        
        # finish coping
        cpuv_common.fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# copy UV map
class CPUVUVMapCopyUV(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.cpuv_uvmap_copy_uv"
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
                CPUVUVMapCopyUVOperation.bl_idname,
                text=m).uv_map = m
            

# paste UV map (sub menu operator)
class CPUVUVMapPasteUVOperation(bpy.types.Operator):
    bl_idname = "uv.cpuv_uvmap_paste_uv_op"
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
        self.src_uv_map = CPUVUVMapCopyUVOperation.src_uv_map
        self.src_obj = CPUVUVMapCopyUVOperation.src_obj
        self.src_sel_face_info = CPUVUVMapCopyUVOperation.src_sel_face_info

    def execute(self, context):
        
        self.report(
            {'INFO'}, "Paste UV coordinate. (UV map:" + self.uv_map + ")")

        # prepare for pasting
        ret, dest_obj, mode_orig = cpuv_common.prep_paste(
            self, self.src_obj, self.src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}
        
        # paste
        dest_sel_face_info = cpuv_common.get_selected_faces(dest_obj)
        ret = cpuv_common.paste_opt(
            self, self.uv_map, self.src_obj, self.src_sel_face_info,
            self.src_uv_map, dest_obj, dest_sel_face_info)
        
        # finish pasting
        cpuv_common.fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# paste UV map
class CPUVUVMapPasteUV(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.cpuv_uvmap_paste_uv"
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
                CPUVUVMapPasteUVOperation.bl_idname,
                text=m).uv_map = m

