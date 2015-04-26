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

# transfer UV
class CPUVTransferUVCopy(bpy.types.Operator):
    """Transfer UV copy."""
    
    bl_idname = "uv.transfer_uv_copy"
    bl_label = "Transfer UV Copy"
    bl_description = "Transfer UV Copy."
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        pass

    def execute(self, context):
        
        self.report({'INFO'}, "Transfer UV copy.")

        # get active object name
        dest_obj_name = bpy.context.active_object.name
        
        # get object from name
        src_obj = bpy.data.objects[src_obj_name]
        dest_obj = bpy.data.objects[dest_obj_name]

        # check if active object has more than one UV map
        if len(dest_obj.data.uv_textures.keys()) == 0:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}

        # get first selected faces
        src_sel_face = cpuv_common.get_selected_faces(src_obj)
        dest_sel_face = cpuv_common.get_selected_faces(dest_obj)
        #uv_map = obj.data.uv_layers.active.name

		# [TODO] fix copy operation
		src_sel_face_prev = serc_sel_face
        dest_sel_face_prev = dest_sel_face
        
        # change to 'EDIT' mode, in order to access internal data
        mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        while true:
        
        	# select more
        	bpy.ops.mesh.select_more()
        	dest_sel_face = cpuv_common.get_selected_faces(dest_obj)
        	
        	# if there is no more selection, process is completed
        	if len(dest_sel_face) == len(dest_sel_face_prev):
        		break
        	
        	# add to history
        	
        	sel_face_prev = sel_face  # [TODO]

        	
       	# now, do UV coordinate.
        
        

        # revert to original mode
        bpy.ops.object.mode_set(mode=mode)

        return {'FINISHED'}

