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


class OBJECT_PT_MUV_CPUVObj(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
    bl_category = "Magic UV"
    bl_context = 'objectmode'

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


class IMAGE_PT_MUV_AUV(bpy.types.Panel):
    """
    Panel class: Align UV on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Align UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        col = layout.column()
        row = col.row(align=True)
        ops = row.operator(muv_auv_ops.MUV_AUVCircle.bl_idname, text="Circle")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select
        ops = row.operator(muv_auv_ops.MUV_AUVStraighten.bl_idname,
                           text="Straighten")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select
        ops.vertical = sc.muv_auv_vertical
        ops.horizontal = sc.muv_auv_horizontal
        row = col.row()
        ops = row.operator(muv_auv_ops.MUV_AUVAxis.bl_idname, text="XY-axis")
        ops.transmission = sc.muv_auv_transmission
        ops.select = sc.muv_auv_select
        ops.vertical = sc.muv_auv_vertical
        ops.horizontal = sc.muv_auv_horizontal
        ops.location = sc.muv_auv_location
        row.prop(sc, "muv_auv_location", text="")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(sc, "muv_auv_transmission", text="Transmission")
        row.prop(sc, "muv_auv_select", text="Select")
        row = col.row(align=True)
        row.prop(sc, "muv_auv_vertical", text="Vertical")
        row.prop(sc, "muv_auv_horizontal", text="Horizontal")


class IMAGE_PT_MUV_SMUV(bpy.types.Panel):
    """
    Panel class: Smooth UV on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Smooth UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        ops = layout.operator(muv_auv_ops.MUV_AUVSmooth.bl_idname,
                              text="Smooth")
        ops.transmission = sc.muv_smuv_transmission
        ops.select = sc.muv_smuv_select
        ops.mesh_infl = sc.muv_smuv_mesh_infl
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(sc, "muv_smuv_transmission", text="Transmission")
        row.prop(sc, "muv_smuv_select", text="Select")
        col.prop(sc, "muv_smuv_mesh_infl", text="Mesh Influence")


class IMAGE_PT_MUV_CPUV(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, _):
        layout = self.layout

        row = layout.row(align=True)
        row.operator(muv_cpuv_ops.MUV_CPUVIECopyUV.bl_idname, text="Copy")
        row.operator(muv_cpuv_ops.MUV_CPUVIEPasteUV.bl_idname, text="Paste")


class IMAGE_PT_MUV_AUVC(bpy.types.Panel):
    """
    Panel class: Align UV Cursor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Align UV Cursor"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.prop(sc, "muv_auvc_align_menu", expand=True)

        col = layout.column(align=True)

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

        layout.label("UV Cursor Location:")
        layout.prop(sc, "muv_auvc_cursor_loc", text="")


class IMAGE_PT_MUV_UVBB(bpy.types.Panel):
    """
    Panel class: UV Bounding Box Menu on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "UV Bounding Box"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        props = sc.muv_props.uvbb
        layout = self.layout
        if props.running is False:
            layout.operator(muv_uvbb_ops.MUV_UVBBUpdater.bl_idname,
                            text="Display", icon='PLAY')
        else:
            layout.operator(muv_uvbb_ops.MUV_UVBBUpdater.bl_idname,
                            text="Hide", icon='PAUSE')
        layout.prop(sc, "muv_uvbb_uniform_scaling", text="Uniform Scaling")


class IMAGE_PT_MUV_PackUV(bpy.types.Panel):
    """
    Panel class: Pack UV (Extension) on Property Panel on UV/ImageEditor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_label = "Pack UV (Extension)"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        ops = layout.operator(muv_packuv_ops.MUV_PackUV.bl_idname,
                              text="Pack UV")
        ops.allowable_center_deviation = sc.muv_packuv_allowable_center_deviation
        ops.allowable_size_deviation = sc.muv_packuv_allowable_size_deviation
        layout.label("Allowable Center Deviation:")
        layout.prop(sc, "muv_packuv_allowable_center_deviation", text="")
        layout.label("Allowable Size Deviation:")
        layout.prop(sc, "muv_packuv_allowable_size_deviation", text="")


class OBJECT_PT_MUV_CPUV(bpy.types.Panel):
    """
    Panel class: Copy/Paste UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Copy/Paste UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        layout.prop(sc, "muv_cpuv_mode", expand=True)
        row = layout.row(align=True)

        if sc.muv_cpuv_mode == 'DEFAULT':
            row.menu(muv_cpuv_ops.MUV_CPUVCopyUVMenu.bl_idname, text="Copy")
            row.menu(muv_cpuv_ops.MUV_CPUVPasteUVMenu.bl_idname, text="Paste")
        elif sc.muv_cpuv_mode == 'SEL_SEQ':
            row.menu(muv_cpuv_selseq_ops.MUV_CPUVSelSeqCopyUVMenu.bl_idname,
                     text="Copy")
            row.menu(muv_cpuv_selseq_ops.MUV_CPUVSelSeqPasteUVMenu.bl_idname,
                     text="Paste")

        layout.prop(sc, "muv_cpuv_copy_seams", text="Seams")
        layout.prop(sc, "muv_cpuv_strategy", text="Strategy")


class OBJECT_PT_MUV_TransUV(bpy.types.Panel):
    """
    Panel class: Transfer UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Transfer UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row(align=True)
        row.operator(muv_transuv_ops.MUV_TransUVCopy.bl_idname, text="Copy")
        ops = row.operator(muv_transuv_ops.MUV_TransUVPaste.bl_idname,
                           text="Paste")
        ops.invert_normals = sc.muv_transuv_invert_normals
        ops.copy_seams = sc.muv_transuv_copy_seams

        row = layout.row()
        row.prop(sc, "muv_transuv_invert_normals", text="Invert Normals")
        row.prop(sc, "muv_transuv_copy_seams", text="Seams")


class OBJECT_PT_MUV_FlipRot(bpy.types.Panel):
    """
    Panel class: Flip/Rotate UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Flip/Rotate"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row()
        ops = row.operator(muv_fliprot_ops.MUV_FlipRot.bl_idname,
                           text="Flip/Rotate")
        ops.seams = sc.muv_fliprot_seams
        row.prop(sc, "muv_fliprot_seams", text="Seams")


class OBJECT_PT_MUV_MirrorUV(bpy.types.Panel):
    """
    Panel class: Mirror UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Mirror UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row()
        ops = row.operator(muv_mirroruv_ops.MUV_MirrorUV.bl_idname,
                              text="Mirror")
        ops.axis = sc.muv_mirroruv_axis
        row.prop(sc, "muv_mirroruv_axis", text="")


class OBJECT_PT_MUV_MVUV(bpy.types.Panel):
    """
    Panel class: Move UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Move UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        props = sc.muv_props
        layout = self.layout

        col = layout.column()
        col.operator(muv_mvuv_ops.MUV_MVUV.bl_idname, icon='PLAY',
                        text="Start")
        if props.mvuv.running:
            col.enabled = False
        else:
            col.enabled = True


class OBJECT_PT_MUV_WSUV(bpy.types.Panel):
    """
    Panel class: World Scale UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "World Scale UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row(align=True)
        row.operator(muv_wsuv_ops.MUV_WSUVMeasure.bl_idname, text="Measure")
        ops = row.operator(muv_wsuv_ops.MUV_WSUVApply.bl_idname, text="Apply")
        ops.proportional_scaling = sc.muv_wsuv_proportional_scaling
        ops.scaling_factor = sc.muv_wsuv_scaling_factor
        ops.origin = sc.muv_wsuv_origin
        layout.prop(sc, "muv_wsuv_proportional_scaling",
                    text="Proportional Scaling")
        if not sc.muv_wsuv_proportional_scaling:
            layout.prop(sc, "muv_wsuv_scaling_factor", text="Scaling Factor")
        layout.prop(sc, "muv_wsuv_origin", text="Origin")


class OBJECT_PT_MUV_PreserveUV(bpy.types.Panel):
    """
    Panel class: Preserve UV on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Preserve UV"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row()
        ops = row.operator(muv_preserve_uv_aspect.MUV_PreserveUVAspect.bl_idname,
                           text="Change Image")
        ops.dest_img_name = sc.muv_preserve_uv_tex_image
        ops.origin = sc.muv_preserve_uv_origin
        row.prop(sc, "muv_preserve_uv_tex_image", text="")
        layout.prop(sc, "muv_preserve_uv_origin", text="Origin")


class OBJECT_PT_MUV_UnwrapConst(bpy.types.Panel):
    """
    Panel class: Unwrap Constraint on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Unwrap Constraint"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        ops = layout.operator(muv_unwrapconst_ops.MUV_UnwrapConstraint.bl_idname,
                           text="Unwrap")
        ops.u_const = sc.muv_unwrapconst_u_const
        ops.v_const = sc.muv_unwrapconst_v_const
        row = layout.row(align=True)
        row.prop(sc, "muv_unwrapconst_u_const", text="U-Constraint")
        row.prop(sc, "muv_unwrapconst_v_const", text="V-Constraint")


class OBJECT_PT_MUV_TexProj(bpy.types.Panel):
    """
    Panel class: Texture Projection on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Texture Projection"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        props = sc.muv_props
        layout = self.layout

        layout.label("Texture Projection:")
        row = layout.row()
        if not props.texproj.running:
            row.operator(muv_texproj_ops.MUV_TexProjStart.bl_idname,
                            text="Start", icon='PLAY')
        else:
            row.operator(muv_texproj_ops.MUV_TexProjStop.bl_idname,
                            text="Stop", icon='PAUSE')
        row.prop(sc, "muv_texproj_tex_image", text="")
        layout.prop(sc, "muv_texproj_tex_transparency", text="Transparency")
        col = layout.column(align=True)
        row = col.row()
        row.prop(sc, "muv_texproj_adjust_window", text="Adjust Window")
        if not sc.muv_texproj_adjust_window:
            row.prop(sc, "muv_texproj_tex_magnitude", text="Magnitude")
        row = col.row()
        row.prop(sc, "muv_texproj_apply_tex_aspect",
                 text="Texture Aspect Ratio")
        if props.texproj.running:
            layout.operator(muv_texproj_ops.MUV_TexProjProject.bl_idname,
                            text="Project")


class OBJECT_PT_MUV_UVW(bpy.types.Panel):
    """
    Panel class: UVW on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "UVW"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        layout = self.layout

        row = layout.row(align=True)
        row.operator(muv_uvw_ops.MUV_UVWBoxMap.bl_idname, text="Box")
        row.operator(muv_uvw_ops.MUV_UVWBestPlanerMap.bl_idname,
                     text="Best Planner")


class OBJECT_PT_MUV_TexLock(bpy.types.Panel):
    """
    Panel class: Texture Lock on Property Panel on View3D
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Texture Lock"
    bl_category = "Magic UV"
    bl_context = 'mesh_edit'

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        sc = context.scene
        props = sc.muv_props
        layout = self.layout

        row = layout.row(align=True)
        col = row.column(align=True)
        col.label("Normal Mode:")
        col = row.column(align=True)
        col.operator(muv_texlock_ops.MUV_TexLockStart.bl_idname, text="Lock")
        ops = col.operator(muv_texlock_ops.MUV_TexLockStop.bl_idname,
                           text="Unlock")
        ops.connect = sc.muv_texlock_connect
        col.prop(sc, "muv_texlock_connect", text="Connect")

        row = layout.row(align=True)
        row.label("Interactive Mode:")
        if not props.texlock.intr_running:
            row.operator(muv_texlock_ops.MUV_TexLockIntrStart.bl_idname,
                         icon='PLAY', text="Start")
        else:
            row.operator(muv_texlock_ops.MUV_TexLockIntrStop.bl_idname,
                         icon="PAUSE", text="Stop")
