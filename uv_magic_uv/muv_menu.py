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
from . import muv_auvc_ops
from . import muv_uvbb_ops
from . import muv_packuv_ops
from . import muv_texproj_ops
from . import muv_fliprot_ops
from . import muv_mvuv_ops
from . import muv_mirroruv_ops
from . import muv_unwrapconst_ops
from . import muv_preserve_uv_aspect
from . import muv_uvinsp_ops
from . import muv_texwrap_ops
from . import muv_uvsculpt_ops


class OBJECT_PT_MUV_CPUVObj(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
    bl_category = "Magic UV"
    bl_context = 'objectmode'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row(align=True)
        row.menu(muv_cpuv_ops.MUV_CPUVObjCopyUVMenu.bl_idname, text="Copy")
        row.menu(muv_cpuv_ops.MUV_CPUVObjPasteUVMenu.bl_idname, text="Paste")
        layout.prop(sc, "muv_cpuv_copy_seams", text="Copy Seams")


class IMAGE_PT_MUV_CPUV(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, _):
        layout = self.layout

        row = layout.row(align=True)
        row.operator(muv_cpuv_ops.MUV_CPUVIECopyUV.bl_idname, text="Copy")
        row.operator(muv_cpuv_ops.MUV_CPUVIEPasteUV.bl_idname, text="Paste")


class IMAGE_PT_MUV_UVManip(bpy.types.Panel):
    """
    Panel class: UV Manipulation on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
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
        box.prop(sc, "muv_auv_enabled", text="Align UV")
        if sc.muv_auv_enabled:
            col = box.column()
            row = col.row(align=True)
            ops = row.operator(muv_auv_ops.MUV_AUVCircle.bl_idname,
                               text="Circle")
            ops.transmission = sc.muv_auv_transmission
            ops.select = sc.muv_auv_select
            ops = row.operator(muv_auv_ops.MUV_AUVStraighten.bl_idname,
                               text="Straighten")
            ops.transmission = sc.muv_auv_transmission
            ops.select = sc.muv_auv_select
            ops.vertical = sc.muv_auv_vertical
            ops.horizontal = sc.muv_auv_horizontal
            row = col.row()
            ops = row.operator(muv_auv_ops.MUV_AUVAxis.bl_idname,
                               text="XY-axis")
            ops.transmission = sc.muv_auv_transmission
            ops.select = sc.muv_auv_select
            ops.vertical = sc.muv_auv_vertical
            ops.horizontal = sc.muv_auv_horizontal
            ops.location = sc.muv_auv_location
            row.prop(sc, "muv_auv_location", text="")

            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(sc, "muv_auv_transmission", text="Transmission")
            row.prop(sc, "muv_auv_select", text="Select")
            row = col.row(align=True)
            row.prop(sc, "muv_auv_vertical", text="Vertical")
            row.prop(sc, "muv_auv_horizontal", text="Horizontal")

        box = layout.box()
        box.prop(sc, "muv_smuv_enabled", text="Smooth UV")
        if sc.muv_smuv_enabled:
            ops = box.operator(muv_auv_ops.MUV_AUVSmooth.bl_idname,
                               text="Smooth")
            ops.transmission = sc.muv_smuv_transmission
            ops.select = sc.muv_smuv_select
            ops.mesh_infl = sc.muv_smuv_mesh_infl
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(sc, "muv_smuv_transmission", text="Transmission")
            row.prop(sc, "muv_smuv_select", text="Select")
            col.prop(sc, "muv_smuv_mesh_infl", text="Mesh Influence")

        box = layout.box()
        box.prop(sc, "muv_seluv_enabled", text="Select UV")
        if sc.muv_seluv_enabled:
            row = box.row(align=True)
            row.operator(muv_uvinsp_ops.MUV_UVInspSelectOverlapped.bl_idname)
            row.operator(muv_uvinsp_ops.MUV_UVInspSelectFlipped.bl_idname)

        box = layout.box()
        box.prop(sc, "muv_packuv_enabled", text="Pack UV (Extension)")
        if sc.muv_packuv_enabled:
            ops = box.operator(muv_packuv_ops.MUV_PackUV.bl_idname,
                               text="Pack UV")
            ops.allowable_center_deviation = \
                sc.muv_packuv_allowable_center_deviation
            ops.allowable_size_deviation = \
                sc.muv_packuv_allowable_size_deviation
            box.label("Allowable Center Deviation:")
            box.prop(sc, "muv_packuv_allowable_center_deviation", text="")
            box.label("Allowable Size Deviation:")
            box.prop(sc, "muv_packuv_allowable_size_deviation", text="")


class IMAGE_PT_MUV_EE(bpy.types.Panel):
    """
    Panel class: UV/Image Editor Enhancement
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Editor Enhancement"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        layout = self.layout
        sc = context.scene
        props = sc.muv_props

        box = layout.box()
        box.prop(sc, "muv_auvc_enabled", text="Align UV Cursor")
        if sc.muv_auvc_enabled:
            box.prop(sc, "muv_auvc_align_menu", expand=True)

            col = box.column(align=True)

            row = col.row(align=True)
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Left Top")
            ops.position = 'LEFT_TOP'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Middle Top")
            ops.position = 'MIDDLE_TOP'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Right Top")
            ops.position = 'RIGHT_TOP'
            ops.base = sc.muv_auvc_align_menu

            row = col.row(align=True)
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Left Middle")
            ops.position = 'LEFT_MIDDLE'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Center")
            ops.position = 'CENTER'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Right Middle")
            ops.position = 'RIGHT_MIDDLE'
            ops.base = sc.muv_auvc_align_menu

            row = col.row(align=True)
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Left Bottom")
            ops.position = 'LEFT_BOTTOM'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Middle Bottom")
            ops.position = 'MIDDLE_BOTTOM'
            ops.base = sc.muv_auvc_align_menu
            ops = row.operator(muv_auvc_ops.MUV_AUVCAlignOps.bl_idname,
                               text="Right Bottom")
            ops.position = 'RIGHT_BOTTOM'
            ops.base = sc.muv_auvc_align_menu

        box = layout.box()
        box.prop(sc, "muv_uvcloc_enabled", text="UV Cursor Location")
        if sc.muv_uvcloc_enabled:
            box.prop(sc, "muv_auvc_cursor_loc", text="")

        box = layout.box()
        box.prop(sc, "muv_uvbb_enabled", text="UV Bounding Box")
        if sc.muv_uvbb_enabled:
            if props.uvbb.running is False:
                box.operator(muv_uvbb_ops.MUV_UVBBUpdater.bl_idname,
                             text="Display", icon='PLAY')
            else:
                box.operator(muv_uvbb_ops.MUV_UVBBUpdater.bl_idname,
                             text="Hide", icon='PAUSE')
            box.prop(sc, "muv_uvbb_uniform_scaling", text="Uniform Scaling")

        box = layout.box()
        box.prop(sc, "muv_uvinsp_enabled", text="UV Inspection")
        if sc.muv_uvinsp_enabled:
            row = box.row()
            if not sc.muv_props.uvinsp.display_running:
                row.operator(muv_uvinsp_ops.MUV_UVInspDisplay.bl_idname,
                             text="Display", icon='PLAY')
            else:
                row.operator(muv_uvinsp_ops.MUV_UVInspDisplay.bl_idname,
                             text="Hide", icon='PAUSE')
                row.operator(muv_uvinsp_ops.MUV_UVInspUpdate.bl_idname,
                             text="Update")
            row = box.row()
            row.prop(sc, "muv_uvinsp_show_overlapped")
            row.prop(sc, "muv_uvinsp_show_flipped")
            row = box.row()
            row.prop(sc, "muv_uvinsp_show_mode")


class OBJECT_PT_MUV_CPUV(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
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
        box.prop(sc, "muv_cpuv_enabled", text="Copy/Paste UV")
        if sc.muv_cpuv_enabled:
            row = box.row(align=True)
            if sc.muv_cpuv_mode == 'DEFAULT':
                row.menu(muv_cpuv_ops.MUV_CPUVCopyUVMenu.bl_idname,
                         text="Copy")
                row.menu(muv_cpuv_ops.MUV_CPUVPasteUVMenu.bl_idname,
                         text="Paste")
            elif sc.muv_cpuv_mode == 'SEL_SEQ':
                row.menu(
                    muv_cpuv_selseq_ops.MUV_CPUVSelSeqCopyUVMenu.bl_idname,
                    text="Copy")
                row.menu(
                    muv_cpuv_selseq_ops.MUV_CPUVSelSeqPasteUVMenu.bl_idname,
                    text="Paste")
            box.prop(sc, "muv_cpuv_mode", expand=True)
            box.prop(sc, "muv_cpuv_copy_seams", text="Seams")
            box.prop(sc, "muv_cpuv_strategy", text="Strategy")

        box = layout.box()
        box.prop(sc, "muv_transuv_enabled", text="Transfer UV")
        if sc.muv_transuv_enabled:
            row = box.row(align=True)
            row.operator(muv_transuv_ops.MUV_TransUVCopy.bl_idname,
                         text="Copy")
            ops = row.operator(muv_transuv_ops.MUV_TransUVPaste.bl_idname,
                               text="Paste")
            ops.invert_normals = sc.muv_transuv_invert_normals
            ops.copy_seams = sc.muv_transuv_copy_seams
            row = box.row()
            row.prop(sc, "muv_transuv_invert_normals", text="Invert Normals")
            row.prop(sc, "muv_transuv_copy_seams", text="Seams")


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
        props = sc.muv_props
        layout = self.layout

        box = layout.box()
        box.prop(sc, "muv_fliprot_enabled", text="Flip/Rotate UV")
        if sc.muv_fliprot_enabled:
            row = box.row()
            ops = row.operator(muv_fliprot_ops.MUV_FlipRot.bl_idname,
                               text="Flip/Rotate")
            ops.seams = sc.muv_fliprot_seams
            row.prop(sc, "muv_fliprot_seams", text="Seams")

        box = layout.box()
        box.prop(sc, "muv_mirroruv_enabled", text="Mirror UV")
        if sc.muv_mirroruv_enabled:
            row = box.row()
            ops = row.operator(muv_mirroruv_ops.MUV_MirrorUV.bl_idname,
                               text="Mirror")
            ops.axis = sc.muv_mirroruv_axis
            row.prop(sc, "muv_mirroruv_axis", text="")

        box = layout.box()
        box.prop(sc, "muv_mvuv_enabled", text="Move UV")
        if sc.muv_mvuv_enabled:
            col = box.column()
            col.operator(muv_mvuv_ops.MUV_MVUV.bl_idname, icon='PLAY',
                         text="Start")
            if props.mvuv.running:
                col.enabled = False
            else:
                col.enabled = True

        box = layout.box()
        box.prop(sc, "muv_wsuv_enabled", text="World Scale UV")
        if sc.muv_wsuv_enabled:
            row = box.row(align=True)
            row.operator(muv_wsuv_ops.MUV_WSUVMeasure.bl_idname,
                         text="Measure")
            ops = row.operator(muv_wsuv_ops.MUV_WSUVApply.bl_idname,
                               text="Apply")
            ops.origin = sc.muv_wsuv_origin
            box.label("Source:")
            sp = box.split(percentage=0.7)
            col = sp.column(align=True)
            col.prop(sc, "muv_wsuv_src_mesh_area", text="Mesh Area")
            col.prop(sc, "muv_wsuv_src_uv_area", text="UV Area")
            col.prop(sc, "muv_wsuv_src_density", text="Density")
            col.enabled = False
            sp = sp.split(percentage=1.0)
            col = sp.column(align=True)
            col.label("cm x cm")
            col.label("px x px")
            col.label("px/cm")
            col.enabled = False
            sp = box.split(percentage=0.3)
            sp.label("Mode:")
            sp = sp.split(percentage=1.0)
            col = sp.column()
            col.prop(sc, "muv_wsuv_mode", text="")
            if sc.muv_wsuv_mode == 'USER':
                col.prop(sc, "muv_wsuv_tgt_density", text="Density")
            if sc.muv_wsuv_mode == 'SCALING':
                col.prop(sc, "muv_wsuv_scaling_factor", text="Scaling Factor")
            box.prop(sc, "muv_wsuv_origin", text="Origin")

        box = layout.box()
        box.prop(sc, "muv_preserve_uv_enabled", text="Preserve UV Aspect")
        if sc.muv_preserve_uv_enabled:
            row = box.row()
            ops = row.operator(
                muv_preserve_uv_aspect.MUV_PreserveUVAspect.bl_idname,
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
            col.operator(muv_texlock_ops.MUV_TexLockStart.bl_idname,
                         text="Lock")
            ops = col.operator(muv_texlock_ops.MUV_TexLockStop.bl_idname,
                               text="Unlock")
            ops.connect = sc.muv_texlock_connect
            col.prop(sc, "muv_texlock_connect", text="Connect")

            row = box.row(align=True)
            row.label("Interactive Mode:")
            if not props.texlock.intr_running:
                row.operator(muv_texlock_ops.MUV_TexLockIntrStart.bl_idname,
                             icon='PLAY', text="Start")
            else:
                row.operator(muv_texlock_ops.MUV_TexLockIntrStop.bl_idname,
                             icon="PAUSE", text="Stop")

        box = layout.box()
        box.prop(sc, "muv_texwrap_enabled", text="Texture Wrap")
        if sc.muv_texwrap_enabled:
            row = box.row(align=True)
            row.operator(muv_texwrap_ops.MUV_TexWrapRefer.bl_idname,
                         text="Refer")
            row.operator(muv_texwrap_ops.MUV_TexWrapSet.bl_idname, text="Set")
            box.prop(sc, "muv_texwrap_set_and_refer")
            box.prop(sc, "muv_texwrap_selseq")

        box = layout.box()
        box.prop(sc, "muv_uvsculpt_enabled", text="UV Sculpt")
        if sc.muv_uvsculpt_enabled:
            if not props.uvsculpt.running:
                box.operator(muv_uvsculpt_ops.MUV_UVSculptOps.bl_idname,
                             icon='PLAY', text="Start")
            else:
                box.operator(muv_uvsculpt_ops.MUV_UVSculptOps.bl_idname,
                             icon='PAUSE', text="Stop")
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


class OBJECT_PT_MUV_UVMapping(bpy.types.Panel):
    """
    Panel class: UV Mapping on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "UV Mapping"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        props = sc.muv_props
        layout = self.layout

        box = layout.box()
        box.prop(sc, "muv_unwrapconst_enabled", text="Unwrap Constraint")
        if sc.muv_unwrapconst_enabled:
            ops = box.operator(
                muv_unwrapconst_ops.MUV_UnwrapConstraint.bl_idname,
                text="Unwrap")
            ops.u_const = sc.muv_unwrapconst_u_const
            ops.v_const = sc.muv_unwrapconst_v_const
            row = box.row(align=True)
            row.prop(sc, "muv_unwrapconst_u_const", text="U-Constraint")
            row.prop(sc, "muv_unwrapconst_v_const", text="V-Constraint")

        box = layout.box()
        box.prop(sc, "muv_texproj_enabled", text="Texture Projection")
        if sc.muv_texproj_enabled:
            row = box.row()
            if not props.texproj.running:
                row.operator(muv_texproj_ops.MUV_TexProjStart.bl_idname,
                             text="Start", icon='PLAY')
            else:
                row.operator(muv_texproj_ops.MUV_TexProjStop.bl_idname,
                             text="Stop", icon='PAUSE')
            row.prop(sc, "muv_texproj_tex_image", text="")
            box.prop(sc, "muv_texproj_tex_transparency", text="Transparency")
            col = box.column(align=True)
            row = col.row()
            row.prop(sc, "muv_texproj_adjust_window", text="Adjust Window")
            if not sc.muv_texproj_adjust_window:
                row.prop(sc, "muv_texproj_tex_magnitude", text="Magnitude")
            col.prop(sc, "muv_texproj_apply_tex_aspect",
                     text="Texture Aspect Ratio")
            col.prop(sc, "muv_texproj_assign_uvmap", text="Assign UVMap")
            if props.texproj.running:
                box.operator(muv_texproj_ops.MUV_TexProjProject.bl_idname,
                             text="Project")

        box = layout.box()
        box.prop(sc, "muv_uvw_enabled", text="UVW")
        if sc.muv_uvw_enabled:
            row = box.row(align=True)
            ops = row.operator(muv_uvw_ops.MUV_UVWBoxMap.bl_idname, text="Box")
            ops.assign_uvmap = sc.muv_uvw_assign_uvmap
            ops = row.operator(muv_uvw_ops.MUV_UVWBestPlanerMap.bl_idname,
                               text="Best Planner")
            ops.assign_uvmap = sc.muv_uvw_assign_uvmap
            box.prop(sc, "muv_uvw_assign_uvmap", text="Assign UVMap")
