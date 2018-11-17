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
__version__ = "5.2"
__date__ = "17 Nov 2018"

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
    'MenuCopyPasteUV',
    'MenuTransferUV',
    'MenuTextureLock',
    'MenuWorldScaleUV',
    'MenuTextureWrap',
    'MenuUVW',
    'MenuTextureProjection',
    'MenuPreserveUVAspect',
]


class MenuCopyPasteUV(bpy.types.Menu):
    """
    Menu class: Master menu of Copy/Paste UV coordinate
    """

    bl_idname = "uv.muv_copy_paste_uv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV coordinate"

    def draw(self, _):
        layout = self.layout

        layout.label("Default")
        layout.menu(copy_paste_uv.MenuCopyUV.bl_idname, text="Copy")
        layout.menu(copy_paste_uv.MenuPasteUV.bl_idname, text="Paste")

        layout.separator()

        layout.label("Selection Sequence")
        layout.menu(copy_paste_uv.MenuSelSeqCopyUV.bl_idname,
                    text="Copy")
        layout.menu(copy_paste_uv.MenuSelSeqPasteUV.bl_idname,
                    text="Paste")


class MenuTransferUV(bpy.types.Menu):
    """
    Menu class: Master menu of Transfer UV coordinate
    """

    bl_idname = "uv.muv_transfer_uv_menu"
    bl_label = "Transfer UV"
    bl_description = "Transfer UV coordinate"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.operator(transfer_uv.OperatorCopyUV.bl_idname, text="Copy")
        ops = layout.operator(transfer_uv.OperatorPasteUV.bl_idname,
                              text="Paste")
        ops.invert_normals = sc.muv_transfer_uv_invert_normals
        ops.copy_seams = sc.muv_transfer_uv_copy_seams


class MenuTextureLock(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Lock
    """

    bl_idname = "uv.muv_texture_lock_menu"
    bl_label = "Texture Lock"
    bl_description = "Lock texture when vertices of mesh (Preserve UV)"

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.label("Normal Mode")
        layout.operator(texture_lock.OperatorLock.bl_idname,
                        text="Lock"
                        if not texture_lock.OperatorLock.is_ready(context)
                        else "ReLock")
        ops = layout.operator(texture_lock.OperatorUnlock.bl_idname,
                              text="Unlock")
        ops.connect = sc.muv_texture_lock_connect

        layout.separator()

        layout.label("Interactive Mode")
        layout.prop(sc, "muv_texture_lock_lock", text="Lock")


class MenuWorldScaleUV(bpy.types.Menu):
    """
    Menu class: Master menu of world scale UV
    """

    bl_idname = "uv.muv_world_scale_uv_menu"
    bl_label = "World Scale UV"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.operator(world_scale_uv.OperatorMeasure.bl_idname,
                        text="Measure")

        layout.operator(world_scale_uv.OperatorApplyManual.bl_idname,
                        text="Apply (Manual)")

        ops = layout.operator(
            world_scale_uv.OperatorApplyScalingDensity.bl_idname,
            text="Apply (Same Desity)")
        ops.src_density = sc.muv_world_scale_uv_src_density
        ops.same_density = True

        ops = layout.operator(
            world_scale_uv.OperatorApplyScalingDensity.bl_idname,
            text="Apply (Scaling Desity)")
        ops.src_density = sc.muv_world_scale_uv_src_density
        ops.same_density = False
        ops.tgt_scaling_factor = sc.muv_world_scale_uv_tgt_scaling_factor

        ops = layout.operator(
            world_scale_uv.OperatorApplyProportionalToMesh.bl_idname,
            text="Apply (Proportional to Mesh)")
        ops.src_density = sc.muv_world_scale_uv_src_density
        ops.src_uv_area = sc.muv_world_scale_uv_src_uv_area
        ops.src_mesh_area = sc.muv_world_scale_uv_src_mesh_area
        ops.origin = sc.muv_world_scale_uv_origin


class MenuTextureWrap(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Wrap
    """

    bl_idname = "uv.muv_texture_wrap_menu"
    bl_label = "Texture Wrap"
    bl_description = ""

    def draw(self, _):
        layout = self.layout

        layout.operator(texture_wrap.OperatorRefer.bl_idname, text="Refer")
        layout.operator(texture_wrap.OperatorSet.bl_idname, text="Set")


class MenuUVW(bpy.types.Menu):
    """
    Menu class: Master menu of UVW
    """

    bl_idname = "uv.muv_uvw_menu"
    bl_label = "UVW"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        ops = layout.operator(uvw.OperatorBoxMap.bl_idname, text="Box")
        ops.assign_uvmap = sc.muv_uvw_assign_uvmap

        ops = layout.operator(uvw.OperatorBestPlanerMap.bl_idname,
                              text="Best Planner")
        ops.assign_uvmap = sc.muv_uvw_assign_uvmap


class MenuTextureProjection(bpy.types.Menu):
    """
    Menu class: Master menu of Texture Projection
    """

    bl_idname = "uv.muv_texture_projection_menu"
    bl_label = "Texture Projection"
    bl_description = ""

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.prop(sc, "muv_texture_projection_enable",
                    text="Texture Projection")
        layout.operator(texture_projection.OperatorProject.bl_idname,
                        text="Project")


class MenuPreserveUVAspect(bpy.types.Menu):
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
                preserve_uv_aspect.Operator.bl_idname, text=key)
            ops.dest_img_name = key
            ops.origin = sc.muv_preserve_uv_aspect_origin
