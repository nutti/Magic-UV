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
from ..op import copy_paste_uv_uvedit
from ..op import align_uv
from ..op import uv_inspection
from ..op import align_uv_cursor
from ..op import uv_bounding_box


__all__ = [
    'MUV_UVCPUVMenu',
    'MUV_AUVMenu',
    'MUV_SelUVMenu',
    'MUV_AUVCMenu',
    'MUV_UVInspMenu',
]


class MUV_UVCPUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate on UV/ImageEditor
    """

    bl_idname = "uv.muv_cpuv_ie_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate among object"

    def draw(self, _):
        layout = self.layout

        layout.operator(copy_paste_uv_uvedit.MUV_CPUVIECopyUV.bl_idname,
                        text="Copy")
        layout.operator(copy_paste_uv_uvedit.MUV_CPUVIEPasteUV.bl_idname,
                        text="Paste")


class MUV_AUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Align UV
    """

    bl_idname = "uv.muv_auv_menu"
    bl_label = "Align UV"
    bl_description = "Align UV"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        ops = layout.operator(align_uv.MUV_AUVCircle.bl_idname, text="Circle")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select

        ops = layout.operator(align_uv.MUV_AUVStraighten.bl_idname,
                              text="Straighten")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select
        ops.vertical = sc.muv_auv_vertical
        ops.horizontal = sc.muv_auv_horizontal

        ops = layout.operator(align_uv.MUV_AUVAxis.bl_idname,
                              text="XY-axis")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select
        ops.vertical = sc.muv_auv_vertical
        ops.horizontal = sc.muv_auv_horizontal
        ops.location = sc.muv_auv_location


class MUV_SelUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Select UV
    """

    bl_idname = "uv.muv_seluv_menu"
    bl_label = "Select UV"
    bl_description = "Select UV"

    def draw(self, _):
        layout = self.layout

        layout.operator(uv_inspection.MUV_UVInspSelectOverlapped.bl_idname,
                        text="Overlapped")
        layout.operator(uv_inspection.MUV_UVInspSelectFlipped.bl_idname,
                        text="Flipped")


class MUV_AUVCMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Align UV Cursor
    """

    bl_idname = "uv.muv_auvc_menu"
    bl_label = "Align UV Cursor"
    bl_description = "Align UV cursor"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Left Top")
        ops.position = 'LEFT_TOP'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Middle Top")
        ops.position = 'MIDDLE_TOP'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Right Top")
        ops.position = 'RIGHT_TOP'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Left Middle")
        ops.position = 'LEFT_MIDDLE'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Center")
        ops.position = 'CENTER'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Right Middle")
        ops.position = 'RIGHT_MIDDLE'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Left Bottom")
        ops.position = 'LEFT_BOTTOM'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Middle Bottom")
        ops.position = 'MIDDLE_BOTTOM'
        ops.base = sc.muv_auvc_align_menu

        ops = layout.operator(align_uv_cursor.MUV_AUVCAlign.bl_idname,
                              text="Right Bottom")
        ops.position = 'RIGHT_BOTTOM'
        ops.base = sc.muv_auvc_align_menu


class MUV_UVInspMenu(bpy.types.Menu):
    """
    Menu class: Master menu of UV Inspection
    """

    bl_idname = "uv.muv_uvinsp_menu"
    bl_label = "UV Inspection"
    bl_description = "UV Inspection"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.prop(sc, "muv_uvinsp_show", text="UV Inspection")
        layout.operator(uv_inspection.MUV_UVInspUpdate.bl_idname,
                        text="Update")
