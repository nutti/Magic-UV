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
__version__ = "5.1"
__date__ = "24 Feb 2018"

import bpy

from ..op import flip_rotate_uv
from ..op import mirror_uv
from ..op import move_uv
from ..op import preserve_uv_aspect
from ..op import texture_lock
from ..op import texture_wrap
from ..op import uv_sculpt
from ..op import world_scale_uv


__all__ = [
    'OBJECT_PT_MUV_UVManip',
]


class OBJECT_PT_MUV_UVManip(bpy.types.Panel):
    """
    Panel class: UV Manipulation on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "UV Manipulation"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        box = layout.box()
        box.prop(sc, "muv_fliprot_enabled", text="Flip/Rotate UV")
        if sc.muv_fliprot_enabled:
            row = box.row()
            ops = row.operator(flip_rotate_uv.MUV_FlipRot.bl_idname,
                               text="Flip/Rotate")
            ops.seams = sc.muv_fliprot_seams
            row.prop(sc, "muv_fliprot_seams", text="Seams")

        box = layout.box()
        box.prop(sc, "muv_mirroruv_enabled", text="Mirror UV")
        if sc.muv_mirroruv_enabled:
            row = box.row()
            ops = row.operator(mirror_uv.MUV_MirrorUV.bl_idname, text="Mirror")
            ops.axis = sc.muv_mirroruv_axis
            row.prop(sc, "muv_mirroruv_axis", text="")

        box = layout.box()
        box.prop(sc, "muv_mvuv_enabled", text="Move UV")
        if sc.muv_mvuv_enabled:
            col = box.column()
            if not move_uv.MUV_MVUV.is_running(context):
                col.operator(move_uv.MUV_MVUV.bl_idname, icon='PLAY',
                             text="Start")
            else:
                col.operator(move_uv.MUV_MVUV.bl_idname, icon='PAUSE',
                             text="Stop")

        box = layout.box()
        box.prop(sc, "muv_wsuv_enabled", text="World Scale UV")
        if sc.muv_wsuv_enabled:
            box.prop(sc, "muv_wsuv_mode", text="")

            if sc.muv_wsuv_mode == 'MANUAL':
                sp = box.split(percentage=0.5)
                col = sp.column()
                col.prop(sc, "muv_wsuv_tgt_texture_size", text="Texture Size")
                sp = sp.split(percentage=1.0)
                col = sp.column()
                col.label("Density:")
                col.prop(sc, "muv_wsuv_tgt_density", text="")
                box.prop(sc, "muv_wsuv_origin", text="Origin")
                ops = box.operator(world_scale_uv.MUV_WSUVApplyManual.bl_idname,
                                   text="Apply")
                ops.tgt_density = sc.muv_wsuv_tgt_density
                ops.tgt_texture_size = sc.muv_wsuv_tgt_texture_size
                ops.origin = sc.muv_wsuv_origin
                ops.show_dialog = False

            elif sc.muv_wsuv_mode == 'SAME_DENSITY':
                sp = box.split(percentage=0.4)
                col = sp.column(align=True)
                col.label("Source:")
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.operator(world_scale_uv.MUV_WSUVMeasure.bl_idname,
                             text="Measure")

                sp = box.split(percentage=0.7)
                col = sp.column(align=True)
                col.prop(sc, "muv_wsuv_src_density", text="Density")
                col.enabled = False
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.label("px2/cm2")

                box.separator()
                box.prop(sc, "muv_wsuv_origin", text="Origin")
                ops = box.operator(world_scale_uv.MUV_WSUVApplyScalingDensity.bl_idname,
                                   text="Apply")
                ops.src_density = sc.muv_wsuv_src_density
                ops.origin = sc.muv_wsuv_origin
                ops.same_density = True
                ops.show_dialog = False

            elif sc.muv_wsuv_mode == 'SCALING_DENSITY':
                sp = box.split(percentage=0.4)
                col = sp.column(align=True)
                col.label("Source:")
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.operator(world_scale_uv.MUV_WSUVMeasure.bl_idname,
                             text="Measure")

                sp = box.split(percentage=0.7)
                col = sp.column(align=True)
                col.prop(sc, "muv_wsuv_src_density", text="Density")
                col.enabled = False
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.label("px2/cm2")

                box.separator()
                box.prop(sc, "muv_wsuv_tgt_scaling_factor", text="Scaling Factor")
                box.prop(sc, "muv_wsuv_origin", text="Origin")
                ops = box.operator(world_scale_uv.MUV_WSUVApplyScalingDensity.bl_idname,
                                   text="Apply")
                ops.src_density = sc.muv_wsuv_src_density
                ops.origin = sc.muv_wsuv_origin
                ops.same_density = False
                ops.show_dialog = False
                ops.tgt_scaling_factor = sc.muv_wsuv_tgt_scaling_factor

            elif sc.muv_wsuv_mode == 'PROPORTIONAL_TO_MESH':
                sp = box.split(percentage=0.4)
                col = sp.column(align=True)
                col.label("Source:")
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.operator(world_scale_uv.MUV_WSUVMeasure.bl_idname,
                             text="Measure")

                sp = box.split(percentage=0.7)
                col = sp.column(align=True)
                col.prop(sc, "muv_wsuv_src_mesh_area", text="Mesh Area")
                col.prop(sc, "muv_wsuv_src_uv_area", text="UV Area")
                col.prop(sc, "muv_wsuv_src_density", text="Density")
                col.enabled = False
                sp = sp.split(percentage=1.0)
                col = sp.column(align=True)
                col.label("cm2")
                col.label("px2")
                col.label("px2/cm2")
                col.enabled = False

                box.separator()
                box.prop(sc, "muv_wsuv_origin", text="Origin")
                ops = box.operator(world_scale_uv.MUV_WSUVApplyProportionalToMesh.bl_idname,
                                   text="Apply")
                ops.src_density = sc.muv_wsuv_src_density
                ops.src_uv_area = sc.muv_wsuv_src_uv_area
                ops.src_mesh_area = sc.muv_wsuv_src_mesh_area
                ops.origin = sc.muv_wsuv_origin
                ops.show_dialog = False

        box = layout.box()
        box.prop(sc, "muv_preserve_uv_enabled", text="Preserve UV Aspect")
        if sc.muv_preserve_uv_enabled:
            row = box.row()
            ops = row.operator(
                preserve_uv_aspect.MUV_PreserveUVAspect.bl_idname,
                text="Change Image")
            ops.dest_img_name = sc.muv_preserve_uv_tex_image
            ops.origin = sc.muv_preserve_uv_origin
            row.prop(sc, "muv_preserve_uv_tex_image", text="")
            box.prop(sc, "muv_preserve_uv_origin", text="Origin")

        box = layout.box()
        box.prop(sc, "muv_texlock_enabled", text="Texture Lock")
        if sc.muv_texlock_enabled:
            row = box.row(align=True)
            col = row.column(align=True)
            col.label("Normal Mode:")
            col = row.column(align=True)
            col.operator(texture_lock.MUV_TexLockLock.bl_idname,
                         text="Lock" if not texture_lock.MUV_TexLockLock.is_ready(context) else "ReLock")
            ops = col.operator(texture_lock.MUV_TexLockUnlock.bl_idname,
                               text="Unlock")
            ops.connect = sc.muv_texlock_connect
            col.prop(sc, "muv_texlock_connect", text="Connect")

            row = box.row(align=True)
            row.label("Interactive Mode:")
            box.prop(sc, "muv_texlock_lock",
                     text="Unlock" if texture_lock.MUV_TexLockIntr.is_running(context) else "Lock",
                     icon='RESTRICT_VIEW_OFF' if texture_lock.MUV_TexLockIntr.is_running(context) else 'RESTRICT_VIEW_ON')

        box = layout.box()
        box.prop(sc, "muv_texwrap_enabled", text="Texture Wrap")
        if sc.muv_texwrap_enabled:
            row = box.row(align=True)
            row.operator(texture_wrap.MUV_TexWrapRefer.bl_idname, text="Refer")
            row.operator(texture_wrap.MUV_TexWrapSet.bl_idname, text="Set")
            box.prop(sc, "muv_texwrap_set_and_refer")
            box.prop(sc, "muv_texwrap_selseq")

        box = layout.box()
        box.prop(sc, "muv_uvsculpt_enabled", text="UV Sculpt")
        if sc.muv_uvsculpt_enabled:
            box.prop(sc, "muv_uvsculpt_enable",
                     text="Disable" if uv_sculpt.MUV_UVSculpt.is_running(context) else "Enable",
                     icon='RESTRICT_VIEW_OFF' if uv_sculpt.MUV_UVSculpt.is_running(context) else 'RESTRICT_VIEW_ON')
            col = box.column()
            col.label("Brush:")
            col.prop(sc, "muv_uvsculpt_radius")
            col.prop(sc, "muv_uvsculpt_strength")
            box.prop(sc, "muv_uvsculpt_tools")
            if sc.muv_uvsculpt_tools == 'PINCH':
                box.prop(sc, "muv_uvsculpt_pinch_invert")
            elif sc.muv_uvsculpt_tools == 'RELAX':
                box.prop(sc, "muv_uvsculpt_relax_method")
            box.prop(sc, "muv_uvsculpt_show_brush")
