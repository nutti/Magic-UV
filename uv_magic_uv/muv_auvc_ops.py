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

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.5"
__date__ = "19 Nov 2017"


import bpy
from mathutils import Vector
from bpy.props import (
    EnumProperty,
)

from . import muv_common


class MUV_AUVCAlignOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_align"
    bl_label = "Align"
    bl_description = "Align cursor to the center of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    position = EnumProperty(
        items=(
            ('CENTER', "Center", "Align to Center"),
            ('LEFT_TOP', "Left Top", "Align to Left Top"),
            ('LEFT_MIDDLE', "Left Middle", "Align to Left Middle"),
            ('LEFT_BOTTOM', "Left Bottom", "Align to Left Bottom"),
            ('MIDDLE_TOP', "Middle Top", "Align to Middle Top"),
            ('MIDDLE_BOTTOM', "Middle Bottom", "Align to Middle Bottom"),
            ('RIGHT_TOP', "Right Top", "Align to Right Top"),
            ('RIGHT_MIDDLE', "Right Middle", "Align to Right Middle"),
            ('RIGHT_BOTTOM', "Right Bottom", "Align to Right Bottom")
        ),
        name="Position",
        description="Align position",
        default='CENTER'
    )
    base = EnumProperty(
        items=(
            ('TEXTURE', "Texture", "Align based on Texture"),
            ('UV_ISLAND', "UV Island", "Align based on UV Island")
        ),
        name="Base",
        description="Align base",
        default='TEXTURE'
    )

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            if self.base == 'UV_ISLAND':
                bd_size = muv_common.get_uvimg_editor_board_size(area)
                if self.position == 'CENTER':
                    cx = isl['center'][0] * bd_size[0]
                    cy = isl['center'][1] * bd_size[1]
                elif self.position == 'LEFT_TOP':
                    cx = isl['min'][0] * bd_size[0]
                    cy = isl['max'][1] * bd_size[1]
                elif self.position == 'LEFT_MIDDLE':
                    cx = isl['min'][0] * bd_size[0]
                    cy = isl['center'][1] * bd_size[1]
                elif self.position == 'LEFT_BOTTOM':
                    cx = isl['min'][0] * bd_size[0]
                    cy = isl['min'][1] * bd_size[1]
                elif self.position == 'MIDDLE_TOP':
                    cx = isl['center'][0] * bd_size[0]
                    cy = isl['max'][1] * bd_size[1]
                elif self.position == 'MIDDLE_BOTTOM':
                    cx = isl['center'][0] * bd_size[0]
                    cy = isl['min'][1] * bd_size[1]
                elif self.position == 'RIGHT_TOP':
                    cx = isl['max'][0] * bd_size[0]
                    cy = isl['max'][1] * bd_size[1]
                elif self.position == 'RIGHT_MIDDLE':
                    cx = isl['max'][0] * bd_size[0]
                    cy = isl['center'][1] * bd_size[1]
                elif self.position == 'RIGHT_BOTTOM':
                    cx = isl['max'][0] * bd_size[0]
                    cy = isl['min'][1] * bd_size[1]
                else:
                    self.report({'ERROR'}, "Unknown Operation")
            elif self.base == 'TEXTURE':
                bd_size = muv_common.get_uvimg_editor_board_size(area)
                if self.position == 'CENTER':
                    cx = bd_size[0] / 2.0
                    cy = bd_size[1] / 2.0
                elif self.position == 'LEFT_TOP':
                    cx = 0
                    cy = bd_size[1]
                elif self.position == 'LEFT_MIDDLE':
                    cx = 0
                    cy = bd_size[1] / 2.0
                elif self.position == 'LEFT_BOTTOM':
                    cx = 0
                    cy = 0
                elif self.position == 'MIDDLE_TOP':
                    cx = bd_size[0] / 2.0
                    cy = bd_size[1]
                elif self.position == 'MIDDLE_BOTTOM':
                    cx = bd_size[0] / 2.0
                    cy = 0
                elif self.position == 'RIGHT_TOP':
                    cx = bd_size[0]
                    cy = bd_size[1]
                elif self.position == 'RIGHT_MIDDLE':
                    cx = bd_size[0]
                    cy = bd_size[1] / 2.0
                elif self.position == 'RIGHT_BOTTOM':
                    cx = bd_size[0]
                    cy = 0
                else:
                    self.report({'ERROR'}, "Unknown Operation")
            else:
                self.report({'ERROR'}, "Unknown Operation")


            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}
