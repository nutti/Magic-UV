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
import copy
import mathutils

from . import cpuv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "3.0"
__date__ = "X XXXX 2015"

            
# sort array by normal
def sort_by_center(src, dest):
    src_sorted = []
    dest_sorted = []

    for s in src:
        matched = False
        for d in dest:
            diff = s.normal - d.normal
            if diff.magnitude < 0.00001:
                src_sorted.append(s)
                dest_sorted.append(d)
                matched = True
                break
        if matched is False:
            raise cpuv_common.CPUVError(
                {'WARNING'}, "Could not find any pair between source and destination")

    return (src_sorted, dest_sorted)

# transfer UV (copy)
class CPUVTransferUVCopy(bpy.types.Operator):
    """Transfer UV copy."""
    
    bl_idname = "uv.transfer_uv_copy"
    bl_label = "Transfer UV Copy"
    bl_description = "Transfer UV Copy."
    bl_options = {'REGISTER', 'UNDO'}
    
    src_obj_name = None

    def execute(self, context):
        
        self.report({'INFO'}, "Transfer UV copy.")
        mode_orig = bpy.context.object.mode

        try:
            # get active object name
            CPUVTransferUVCopy.src_obj_name = bpy.context.active_object.name
            
            # prepare for coping
            src_obj = cpuv_common.prep_copy(self)
    
            # copy
            src_sel_face_info = cpuv_common.get_selected_faces_by_sel_seq(src_obj)
            CPUVTransferUVCopy.src_uv_map = cpuv_common.copy_opt(
                self, "", src_obj, src_sel_face_info)
    
            # finish coping
            cpuv_common.fini_copy()
            
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}

        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)

        return {'FINISHED'}


# transfer UV (paste)
class CPUVTransferUVPaste(bpy.types.Operator):
    """Transfer UV paste."""
    
    bl_idname = "uv.transfer_uv_paste"
    bl_label = "Transfer UV Paste"
    bl_description = "Transfer UV Paste."
    bl_options = {'REGISTER', 'UNDO'}

    flip_copied_uv = False
    rotate_copied_uv = 0

    def execute(self, context):
        
        self.report({'INFO'}, "Transfer UV paste.")

        mode_orig = bpy.context.object.mode

        try:
            # get active object name
            dest_obj_name = bpy.context.active_object.name
            
            # get object from name
            src_obj = bpy.data.objects[CPUVTransferUVCopy.src_obj_name]
            dest_obj = bpy.data.objects[dest_obj_name]

            src_uv_map = src_obj.data.uv_layers.active.name
    
            # check if object has more than one UV map
            if len(src_obj.data.uv_textures.keys()) == 0:
                raise cpuv_common.CPUVError({'WARNING'}, "Object must have more than one UV map.")
            if len(dest_obj.data.uv_textures.keys()) == 0:
                raise cpuv_common.CPUVError({'WARNING'}, "Object must have more than one UV map.")
    
            # get first selected faces
            src_sel_face = cpuv_common.get_selected_faces(src_obj)
            dest_sel_face = cpuv_common.get_selected_faces(dest_obj)
    
            # store previous selected faces
            src_sel_face_prev = copy.deepcopy(src_sel_face)
            dest_sel_face_prev = copy.deepcopy(dest_sel_face)
            
            # get similar faces
            while True:
            
                #####################
                # source object
                #####################
                bpy.ops.object.mode_set(mode='OBJECT')
                dest_obj.select = False
                bpy.context.scene.objects.active = src_obj
                src_obj.select = True
            
                # change to 'EDIT' mode, in order to access internal data
                bpy.ops.object.mode_set(mode='EDIT')
            
                # select more
                bpy.ops.mesh.select_more()
                bpy.ops.object.editmode_toggle()    # update mesh
                bpy.ops.object.editmode_toggle()
                src_sel_face = cpuv_common.get_selected_faces(src_obj)
                
                # if there is no more selection, process is completed
                if len(src_sel_face) == len(src_sel_face_prev):
                    break
            
                #####################
                # destination object
                #####################
                bpy.ops.object.mode_set(mode='OBJECT')
                src_obj.select = False
                bpy.context.scene.objects.active = dest_obj
                dest_obj.select = True
                
                # change to 'EDIT' mode, in order to access internal data
                bpy.ops.object.mode_set(mode='EDIT')
            
                # select more
                bpy.ops.mesh.select_more()
                bpy.ops.object.editmode_toggle()    # update mesh
                bpy.ops.object.editmode_toggle()
                dest_sel_face = cpuv_common.get_selected_faces(dest_obj)
                
                # if there is no more selection, process is completed
                if len(dest_sel_face) == len(dest_sel_face_prev):
                    break
                # do not match between source and destination
                if len(src_sel_face) != len(dest_sel_face):
                    break
                
                # add to history
                src_sel_face_prev = copy.deepcopy(src_sel_face)
                dest_sel_face_prev = copy.deepcopy(dest_sel_face)
            
            # sort array in order to match selected faces
            src_sel_face, dest_sel_face = sort_by_center(src_sel_face_prev, dest_sel_face_prev)
                
            bpy.ops.object.mode_set(mode='OBJECT')

            # now, paste UV coordinate.
            cpuv_common.paste_opt(
                self, "", src_obj, src_sel_face,
                CPUVTransferUVCopy.src_uv_map, dest_obj, dest_sel_face)
        
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}

        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)

        return {'FINISHED'}
