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
from . import muv_cpuv_ops
from . import muv_cpuv_selseq_ops
from . import muv_transuv_ops
from . import muv_texlock_ops
from . import muv_wsuv_ops
from . import muv_uvw_ops
from . import muv_auv_ops


class MUV_CPUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate
    """

    bl_idname = "uv.muv_cpuv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate"

    def draw(self, _):
        self.layout.menu(
            muv_cpuv_ops.MUV_CPUVCopyUVMenu.bl_idname, icon="IMAGE_COL")
        self.layout.menu(
            muv_cpuv_ops.MUV_CPUVPasteUVMenu.bl_idname, icon="IMAGE_COL")
        self.layout.menu(
            muv_cpuv_selseq_ops.MUV_CPUVSelSeqCopyUVMenu.bl_idname,
            icon="IMAGE_COL")
        self.layout.menu(
            muv_cpuv_selseq_ops.MUV_CPUVSelSeqPasteUVMenu.bl_idname,
            icon="IMAGE_COL")


class MUV_CPUVObjMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate per object
    """

    bl_idname = "object.muv_cpuv_obj_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate per object"

    def draw(self, _):
        self.layout.menu(
            muv_cpuv_ops.MUV_CPUVObjCopyUVMenu.bl_idname, icon="IMAGE_COL")
        self.layout.menu(
            muv_cpuv_ops.MUV_CPUVObjPasteUVMenu.bl_idname, icon="IMAGE_COL")


class MUV_TransUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Transfer UV coordinate
    """

    bl_idname = "uv.muv_transuv_menu"
    bl_label = "Transfer UV"
    bl_description = "Transfer UV coordinate"

    def draw(self, _):
        self.layout.operator(
            muv_transuv_ops.MUV_TransUVCopy.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_transuv_ops.MUV_TransUVPaste.bl_idname, icon="IMAGE_COL")


class MUV_TexLockMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Lock
    """

    bl_idname = "uv.muv_texlock_menu"
    bl_label = "Texture Lock"
    bl_description = "Lock texture when vertices of mesh (Preserve UV)"

    def draw(self, _):
        self.layout.operator(
            muv_texlock_ops.MUV_TexLockStart.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_texlock_ops.MUV_TexLockStop.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_texlock_ops.MUV_TexLockIntrStart.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_texlock_ops.MUV_TexLockIntrStop.bl_idname, icon="IMAGE_COL")


class MUV_WSUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of world scale UV
    """

    bl_idname = "uv.muv_wsuv_menu"
    bl_label = "World Scale UV"
    bl_description = ""

    def draw(self, _):
        self.layout.operator(
            muv_wsuv_ops.MUV_WSUVMeasure.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_wsuv_ops.MUV_WSUVApply.bl_idname, icon="IMAGE_COL")


class MUV_UVWMenu(bpy.types.Menu):
    """
    Menu class: Master menu of UVW
    """

    bl_idname = "uv.muv_uvw_menu"
    bl_label = "UVW"
    bl_description = ""

    def draw(self, _):
        self.layout.operator(
            muv_uvw_ops.MUV_UVWBoxMap.bl_idname, icon="IMAGE_COL")
        self.layout.operator(
            muv_uvw_ops.MUV_UVWBestPlanerMap.bl_idname, icon="IMAGE_COL")


class IMAGE_PT_MUV(bpy.types.Panel):
    """
    Panel class: Magic UV on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Magic UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, _):
        layout = self.layout

        layout.label("Align UV")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator(muv_auv_ops.MUV_AUVCircle.bl_idname, text="Circle")
        row.operator(muv_auv_ops.MUV_AUVSmooth.bl_idname, text="Smooth")

        row = col.row(align=True)
        row.operator(muv_auv_ops.MUV_AUVStraighten.bl_idname, text="Straighten")
        row.operator(muv_auv_ops.MUV_AUVAxis.bl_idname, text="XY-axis")

        layout.label("Copy/Paste UV")

        row = layout.row(align=True)
        row.operator(muv_cpuv_ops.MUV_CPUVIECopyUV.bl_idname, text="Copy UV")
        row.operator(muv_cpuv_ops.MUV_CPUVIEPasteUV.bl_idname, text="Paste UV")

