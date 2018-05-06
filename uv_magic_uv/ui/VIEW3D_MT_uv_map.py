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
from ..op import copy_paste_uv
from ..op import transfer_uv
from ..op import texture_lock
from ..op import world_scale_uv
from ..op import uvw
from ..op import texture_projection
from ..op import texture_wrap


class MUV_CPUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate
    """

    bl_idname = "uv.muv_cpuv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate"

    def draw(self, _):
        layout = self.layout

        layout.menu(copy_paste_uv.MUV_CPUVCopyUVMenu.bl_idname,
                    icon="IMAGE_COL")
        layout.menu(copy_paste_uv.MUV_CPUVPasteUVMenu.bl_idname,
                    icon="IMAGE_COL")
        layout.menu(copy_paste_uv.MUV_CPUVSelSeqCopyUVMenu.bl_idname,
                    icon="IMAGE_COL")
        layout.menu(copy_paste_uv.MUV_CPUVSelSeqPasteUVMenu.bl_idname,
                    icon="IMAGE_COL")


class MUV_TransUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Transfer UV coordinate
    """

    bl_idname = "uv.muv_transuv_menu"
    bl_label = "Transfer UV"
    bl_description = "Transfer UV coordinate"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.operator(transfer_uv.MUV_TransUVCopy.bl_idname, icon="IMAGE_COL")
        ops = layout.operator(transfer_uv.MUV_TransUVPaste.bl_idname,
                              icon="IMAGE_COL")
        ops.invert_normals = sc.muv_transuv_invert_normals
        ops.copy_seams = sc.muv_transuv_copy_seams


class MUV_TexLockMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Lock
    """

    bl_idname = "uv.muv_texlock_menu"
    bl_label = "Texture Lock"
    bl_description = "Lock texture when vertices of mesh (Preserve UV)"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.operator(texture_lock.MUV_TexLockStart.bl_idname,
                        icon="IMAGE_COL")
        ops = layout.operator(texture_lock.MUV_TexLockStop.bl_idname,
                              icon="IMAGE_COL")
        ops.connect = sc.muv_texlock_connect

        layout.operator(texture_lock.MUV_TexLockIntrStart.bl_idname,
                        icon="IMAGE_COL")
        layout.operator(texture_lock.MUV_TexLockIntrStop.bl_idname,
                        icon="IMAGE_COL")


class MUV_WSUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of world scale UV
    """

    bl_idname = "uv.muv_wsuv_menu"
    bl_label = "World Scale UV"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.operator(world_scale_uv.MUV_WSUVMeasure.bl_idname,
                        icon="IMAGE_COL")
        ops = layout.operator(world_scale_uv.MUV_WSUVApply.bl_idname,
                              icon="IMAGE_COL")
        ops.origin = sc.muv_wsuv_origin


class MUV_TexWrapMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Wrap
    """

    bl_idname = "uv.muv_texwrap_menu"
    bl_label = "Texture Wrap"
    bl_description = ""

    def draw(self, _):
        layout = self.layout

        layout.operator(texture_wrap.MUV_TexWrapRefer.bl_idname,
                        icon="IMAGE_COL", text="Refer")
        layout.operator(texture_wrap.MUV_TexWrapSet.bl_idname,
                        icon="IMAGE_COL", text="Set")


class MUV_UVWMenu(bpy.types.Menu):
    """
    Menu class: Master menu of UVW
    """

    bl_idname = "uv.muv_uvw_menu"
    bl_label = "UVW"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        ops = layout.operator(uvw.MUV_UVWBoxMap.bl_idname,
                              text="Box", icon="IMAGE_COL")
        ops.assign_uvmap = sc.muv_uvw_assign_uvmap

        ops = layout.operator(uvw.MUV_UVWBestPlanerMap.bl_idname,
                              text="Best Planner", icon="IMAGE_COL")
        ops.assign_uvmap = sc.muv_uvw_assign_uvmap


class MUV_TexProjMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Projection
    """

    bl_idname = "uv.muv_texproj_menu"
    bl_label = "Texture Projection"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene
        props = sc.muv_props

        if not props.texproj.running:
            layout.operator(texture_projection.MUV_TexProjStart.bl_idname,
                            text="Start", icon='PLAY')
        else:
            layout.operator(texture_projection.MUV_TexProjStop.bl_idname,
                            text="Stop", icon='PAUSE')
        layout.operator(texture_projection.MUV_TexProjProject.bl_idname,
                        text="Project")
