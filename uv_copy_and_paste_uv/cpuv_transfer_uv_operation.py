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
from bpy.props import FloatProperty, EnumProperty
import copy
import math
import mathutils

from . import cpuv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "3.0"
__date__ = "15 Jun 2015"


def is_matched(diff, precise):
    r1 = math.fabs(diff.x) < precise
    r2 = math.fabs(diff.y) < precise
    r3 = math.fabs(diff.z) < precise
    return r1 and r2 and r3


# filter faces
def filter_faces(src, dest, precise, strategy):
    strategy_fn = None

    if strategy == "NONE":
        strategy_fn = (lambda s, d, precise:
                       True)
    elif strategy == "CENTER":
        strategy_fn = (lambda s, d, precise:
                       is_matched(s.center - d.center, precise))
    elif strategy == "NORMAL":
        strategy_fn = (lambda s, d, precise:
                       is_matched(s.normal - d.normal, precise))
    elif strategy == "INDEX":
        strategy_fn = (lambda s, d, precise:
                       s.indices == d.indices)

    return zip(*[(s, d)
                 for s, d in zip(src, dest)
                 if len(s.indices) == len(d.indices) and
                 strategy_fn(s, d, precise)
                 ])


def get_strategy(scene, context):
    items = []

    items.append(("NONE", "None", "No strategy."))
    items.append(("NORMAL", "Normal", "Normal."))
    items.append(("CENTER", "Center", "Center of face."))
    items.append(("INDEX", "Index", "Vertex Index."))

    return items


# transfer UV (copy)
class CPUVTransferUVCopy(bpy.types.Operator):
    """Transfer UV copy."""

    bl_idname = "uv.transfer_uv_copy"
    bl_label = "Transfer UV Copy"
    bl_description = "Transfer UV Copy."
    bl_options = {'REGISTER', 'UNDO'}

    src_obj_name = None
    src_face_indices = None

    def execute(self, context):
        props = context.scene.cpuv_props.transuv
        self.report({'INFO'}, "Transfer UV copy.")
        mem = cpuv_common.View3DModeMemory(context)
        cpuv_common.update_mesh()
        # get active object name
        props.src_obj_name = context.active_object.name
        # prepare for coping
        ret, src_obj = cpuv_common.prep_copy(context, self)
        if ret != 0:
            return {'CANCELLED'}
        # copy
        src_sel_face_info = cpuv_common.get_selected_faces_by_sel_seq(
            src_obj)
        props.src_faces = cpuv_common.get_selected_face_indices(
            context, src_obj)
        ret, props.src_uv_map = cpuv_common.copy_opt(
            self, "", src_obj, src_sel_face_info)
        if ret != 0:
            return {'CANCELLED'}
        # finish coping
        cpuv_common.fini_copy()
        # revert to original mode
        return {'FINISHED'}


# transfer UV (paste)
class CPUVTransferUVPaste(bpy.types.Operator):
    """Transfer UV paste."""

    bl_idname = "uv.transfer_uv_paste"
    bl_label = "Transfer UV Paste"
    bl_description = "Transfer UV Paste."
    bl_options = {'REGISTER', 'UNDO'}

    flip_copied_uv = False
    rotate_copied_uv = 0

    precise = FloatProperty(
        default=0.1,
        name="Precise",
        min=0.000001,
        max=1.0)

    strategy = EnumProperty(
        name="Strategy",
        description="Matching strategy",
        items=get_strategy)

    def execute(self, context):
        props = context.scene.cpuv_props.transuv
        self.report({'INFO'}, "Transfer UV paste.")
        mem = cpuv_common.View3DModeMemory(context)

        # get active object name
        dest_obj_name = context.active_object.name
        # get object from name
        src_obj = bpy.data.objects[props.src_obj_name]
        dest_obj = bpy.data.objects[dest_obj_name]

        # check if object has more than one UV map
        if len(src_obj.data.uv_textures.keys()) == 0:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        if len(dest_obj.data.uv_textures.keys()) == 0:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}

        # get first selected faces
        cpuv_common.update_mesh()
        src_face_indices = copy.copy(props.src_faces)
        ini_src_face_indices = copy.copy(src_face_indices)
        src_sel_face = cpuv_common.get_faces_from_indices(
            src_obj, src_face_indices)
        dest_face_indices = cpuv_common.get_selected_face_indices(
            context, dest_obj)
        ini_dest_face_indices = copy.copy(dest_face_indices)
        dest_sel_face = cpuv_common.get_faces_from_indices(
            src_obj, dest_face_indices)

        # store previous selected faces
        src_sel_face_prev = copy.deepcopy(src_sel_face)
        dest_sel_face_prev = copy.deepcopy(dest_sel_face)

        # get similar faces
        while True:
            #####################
            # source object
            #####################
            cpuv_common.change_active_object(context, dest_obj, src_obj)
            # reset selection
            cpuv_common.select_faces_by_indices(
                context, src_obj, src_face_indices)
            # change to 'EDIT' mode, in order to access internal data
            mem.change_mode('EDIT')
            # select more
            bpy.ops.mesh.select_more()
            cpuv_common.update_mesh()
            # get selected faces
            src_face_indices = cpuv_common.get_selected_face_indices(
                context, src_obj)
            src_sel_face = cpuv_common.get_faces_from_indices(
                src_obj, src_face_indices)
            # if there is no more selection, process is completed
            if len(src_sel_face) == len(src_sel_face_prev):
                break

            #####################
            # destination object
            #####################
            cpuv_common.change_active_object(context, src_obj, dest_obj)
            # reset selection
            cpuv_common.select_faces_by_indices(
                context, dest_obj, dest_face_indices)
            # change to 'EDIT' mode, in order to access internal data
            mem.change_mode('EDIT')
            # select more
            bpy.ops.mesh.select_more()
            cpuv_common.update_mesh()
            # get selected faces
            dest_face_indices = cpuv_common.get_selected_face_indices(
                context, dest_obj)
            dest_sel_face = cpuv_common.get_faces_from_indices(
                dest_obj, dest_face_indices)
            # if there is no more selection, process is completed
            if len(dest_sel_face) == len(dest_sel_face_prev):
                break
            # do not match between source and destination
            if len(src_sel_face) != len(dest_sel_face):
                break

            # add to history
            src_sel_face_prev = copy.deepcopy(src_sel_face)
            dest_sel_face_prev = copy.deepcopy(dest_sel_face)

        # sort array in order to match selected faces
        src_sel_face, dest_sel_face = filter_faces(
            src_sel_face_prev, dest_sel_face_prev,
            self.precise, self.strategy)

        mem.change_mode('OBJECT')

        # now, paste UV coordinate.
        ret = cpuv_common.paste_opt(
            context, self, "", src_obj, src_sel_face,
            props.src_uv_map, dest_obj, dest_sel_face)
        if ret != 0:
            cpuv_common.change_active_object(context, src_obj, dest_obj)
            cpuv_common.select_faces_by_indices(
                context, src_obj, ini_src_face_indices)
            cpuv_common.select_faces_by_indices(
                context, dest_obj, ini_dest_face_indices)
            return {'CANCELLED'}

        # revert to original mode
        cpuv_common.change_active_object(context, src_obj, dest_obj)
        cpuv_common.select_faces_by_indices(
            context, src_obj, ini_src_face_indices)
        cpuv_common.select_faces_by_indices(
            context, dest_obj, ini_dest_face_indices)
        return {'FINISHED'}
