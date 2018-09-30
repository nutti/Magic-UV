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
from ..op import preserve_uv_aspect


__all__ = [
    'MUV_CPUVMenu',
    'MUV_TransUVMenu',
    'MUV_TexLockMenu',
    'MUV_WSUVMenu',
    'MUV_TexWrapMenu',
    'MUV_UVWMenu',
    'MUV_TexProjMenu',
    'MUV_PreserveUVMenu',
]


class MUV_CPUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate
    """

    bl_idname = "uv.muv_cpuv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate"

    def draw(self, _):
        layout = self.layout

        layout.label("Default")
        layout.menu(copy_paste_uv.MUV_CPUVCopyUVMenu.bl_idname, text="Copy")
        layout.menu(copy_paste_uv.MUV_CPUVPasteUVMenu.bl_idname, text="Paste")

        layout.separator()

        layout.label("Selection Sequence")
        layout.menu(copy_paste_uv.MUV_CPUVSelSeqCopyUVMenu.bl_idname,
                    text="Copy")
        layout.menu(copy_paste_uv.MUV_CPUVSelSeqPasteUVMenu.bl_idname,
                    text="Paste")


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

        layout.operator(transfer_uv.MUV_TransUVCopy.bl_idname, text="Copy")
        ops = layout.operator(transfer_uv.MUV_TransUVPaste.bl_idname,
                              text="Paste")
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

        layout.label("Normal Mode")
        layout.operator(texture_lock.MUV_TexLockLock.bl_idname,
                        text="Lock" if not texture_lock.MUV_TexLockLock.is_ready(context) else "ReLock")
        ops = layout.operator(texture_lock.MUV_TexLockUnlock.bl_idname,
                              text="Unlock")
        ops.connect = sc.muv_texlock_connect

        layout.separator()

        layout.label("Interactive Mode")
        layout.prop(sc, "muv_texlock_lock", text="Lock")


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
                        text="Measure")

        layout.operator(world_scale_uv.MUV_WSUVApplyManual.bl_idname,
                        text="Apply (Manual)")

        ops = layout.operator(
            world_scale_uv.MUV_WSUVApplyScalingDensity.bl_idname,
            text="Apply (Same Desity)")
        ops.src_density = sc.muv_wsuv_src_density
        ops.same_density = True

        ops = layout.operator(
            world_scale_uv.MUV_WSUVApplyScalingDensity.bl_idname,
            text="Apply (Scaling Desity)")
        ops.src_density = sc.muv_wsuv_src_density
        ops.same_density = False
        ops.tgt_scaling_factor = sc.muv_wsuv_tgt_scaling_factor

        ops = layout.operator(world_scale_uv.MUV_WSUVApplyProportionalToMesh.bl_idname,
                              text="Apply (Proportional to Mesh)")
        ops.src_density = sc.muv_wsuv_src_density
        ops.src_uv_area = sc.muv_wsuv_src_uv_area
        ops.src_mesh_area = sc.muv_wsuv_src_mesh_area
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

        layout.operator(texture_wrap.MUV_TexWrapRefer.bl_idname, text="Refer")
        layout.operator(texture_wrap.MUV_TexWrapSet.bl_idname, text="Set")


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

        ops = layout.operator(uvw.MUV_UVWBoxMap.bl_idname, text="Box")
        ops.assign_uvmap = sc.muv_uvw_assign_uvmap

        ops = layout.operator(uvw.MUV_UVWBestPlanerMap.bl_idname,
                              text="Best Planner")
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

        layout.prop(sc, "muv_texproj_enable", text="Texture Projection")
        layout.operator(texture_projection.MUV_TexProjProject.bl_idname,
                        text="Project")


class MUV_PreserveUVMenu(bpy.types.Menu):
    """
    Menu class: Master menu of Preserve UV Aspect
    """

    bl_idname = "uv.muv_preserve_uv_aspect_menu"
    bl_label = "Preserve UV Aspect"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        for key in bpy.data.images.keys():
            ops = layout.operator(
                preserve_uv_aspect.MUV_PreserveUVAspect.bl_idname, text=key)
            ops.dest_img_name = key
            ops.origin = sc.muv_preserve_uv_origin
