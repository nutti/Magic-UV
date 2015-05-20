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
from bpy.props import *
from . import cpuv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "3.0"
__date__ = "X XXXX 2015"


# copy UV (by selection sequence)
class CPUVSelSeqCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object by selection sequence."""

    bl_idname = "uv.cpuv_selseq_copy_uv"
    bl_label = "Copy UV (Selection Sequence)"
    bl_description = "Copy UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = bpy.context.scene.cpuv_props.selseq
        self.report({'INFO'}, "Copy UV coordinate. (sequence)")
        mem = cpuv_common.View3DModeMemory()

        try:
            # prepare for coping
            props.src_obj = cpuv_common.prep_copy(self)
            # copy
            props.src_faces = cpuv_common.get_selected_faces_by_sel_seq(
                props.src_obj)
            props.src_uv_map = cpuv_common.copy_opt(
                self, "", props.src_obj, props.src_faces)
            # finish coping
            cpuv_common.fini_copy()
        except cpuv_common.CPUVError as e:
            e.report(self)
            return {'CANCELLED'}

        return {'FINISHED'}


# paste UV (by selection sequence)
class CPUVSelSeqPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied by selection sequence."""

    bl_idname = "uv.cpuv_selseq_paste_uv"
    bl_label = "Paste UV (Selection Sequence)"
    bl_description = "Paste UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    flip_copied_uv = BoolProperty(
        name="Flip Copied UV",
        description="Flip Copied UV...",
        default=False)

    rotate_copied_uv = IntProperty(
        default=0,
        name="Rotate Copied UV",
        min=0,
        max=30)

    def execute(self, context):
        props = bpy.context.scene.cpuv_props.selseq
        self.report({'INFO'}, "Paste UV coordinate. (sequence)")
        mem = cpuv_common.View3DModeMemory()

        try:
            # prepare for pasting
            dest_obj = cpuv_common.prep_paste(
                self, props.src_obj, props.src_faces)
            # paste
            dest_faces = cpuv_common.get_selected_faces_by_sel_seq(dest_obj)
            cpuv_common.paste_opt(
                self, "", props.src_obj, props.src_faces,
                props.src_uv_map, dest_obj, dest_faces)
            # finish pasting
            cpuv_common.fini_paste()
        except cpuv_common.CPUVError as e:
            e.report(self)
            return {'CANCELLED'}

        return {'FINISHED'}
