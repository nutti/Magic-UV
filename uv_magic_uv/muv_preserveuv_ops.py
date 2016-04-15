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
from . import muv_common
from bpy.props import FloatProperty
from mathutils import Vector, Matrix
from math import sqrt, atan2
from bpy_extras import view3d_utils

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"



# Texture lock
class MUV_TexLockRotation(bpy.types.Operator):
    """Lock texture.(Rotation)"""

    bl_idname = "uv.muv_texlock_rotation"
    bl_label = "Rotation"
    bl_description = "Lock Texture (Rotation)"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        props = context.scene.muv_props.texlock
        redraw_all_areas()
        if event.type == 'MOUSEMOVE':
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            # get UV layer
            if not bm.loops.layers.uv:
                self.report({'WARNING'}, "Object must have more than one UV map.")
                return {'CANCELLED'}
            uv_layer = bm.loops.layers.uv.verify()



        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            self.first_time = True
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}



