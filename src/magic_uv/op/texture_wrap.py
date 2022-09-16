# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "6.6"
__date__ = "22 Apr 2022"

import math
import bpy
from bpy.props import (
    BoolProperty,
)
import bmesh
from mathutils import Vector, Matrix
from numpy.linalg import solve

from .. import common
from ..utils.bl_class_registry import BlClassRegistry
from ..utils.property_class_registry import PropertyClassRegistry


def _is_valid_context(context):
    # only 'VIEW_3D' space is allowed to execute
    if not common.is_valid_space(context, ['VIEW_3D']):
        return False

    # Multiple objects editing mode is not supported in this feature.
    objs = common.get_uv_editable_objects(context)
    if len(objs) != 1:
        return False

    # only edit mode is allowed to execute
    if context.object.mode != 'EDIT':
        return False

    return True


@PropertyClassRegistry()
class _Properties:
    idname = "texture_wrap"

    @classmethod
    def init_props(cls, scene):
        class Props():
            ref_face_index = -1
            ref_obj = None

        scene.muv_props.texture_wrap = Props()

        scene.muv_texture_wrap_enabled = BoolProperty(
            name="Texture Wrap",
            description="Texture Wrap is enabled",
            default=False
        )
        scene.muv_texture_wrap_set_and_refer = BoolProperty(
            name="Set and Refer",
            description="Refer and set UV",
            default=True
        )
        scene.muv_texture_wrap_selseq = BoolProperty(
            name="Selection Sequence",
            description="Set UV sequentially",
            default=False
        )

    @classmethod
    def del_props(cls, scene):
        del scene.muv_props.texture_wrap
        del scene.muv_texture_wrap_enabled
        del scene.muv_texture_wrap_set_and_refer
        del scene.muv_texture_wrap_selseq


@BlClassRegistry()
class MUV_OT_TextureWrap_Refer(bpy.types.Operator):
    """
    Operation class: Refer UV
    """

    bl_idname = "uv.muv_texture_wrap_refer"
    bl_label = "Refer"
    bl_description = "Refer UV"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # we can not get area/space/region from console
        if common.is_console_mode():
            return True
        return _is_valid_context(context)

    def execute(self, context):
        props = context.scene.muv_props.texture_wrap

        objs = common.get_uv_editable_objects(context)
        # poll() method ensures that only one object is selected.
        obj = objs[0]
        bm = bmesh.from_edit_mesh(obj.data)
        if common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()

        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map")
            return {'CANCELLED'}

        sel_faces = [f for f in bm.faces if f.select]
        if len(sel_faces) != 1:
            self.report({'WARNING'}, "Must select only one face")
            return {'CANCELLED'}

        props.ref_face_index = sel_faces[0].index
        props.ref_obj = obj

        return {'FINISHED'}


@BlClassRegistry()
class MUV_OT_TextureWrap_Set(bpy.types.Operator):
    """
    Operation class: Set UV
    """

    bl_idname = "uv.muv_texture_wrap_set"
    bl_label = "Set"
    bl_description = "Set UV"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # we can not get area/space/region from console
        if common.is_console_mode():
            return True
        sc = context.scene
        props = sc.muv_props.texture_wrap
        if not props.ref_obj:
            return False
        return _is_valid_context(context)

    def execute(self, context):
        sc = context.scene
        props = sc.muv_props.texture_wrap

        objs = common.get_uv_editable_objects(context)
        # poll() method ensures that only one object is selected.
        obj = objs[0]
        bm = bmesh.from_edit_mesh(obj.data)
        if common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()

        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        if sc.muv_texture_wrap_selseq:
            sel_faces = []
            for hist in bm.select_history:
                if isinstance(hist, bmesh.types.BMFace) and hist.select:
                    sel_faces.append(hist)
            if not sel_faces:
                self.report({'WARNING'}, "Must select more than one face")
                return {'CANCELLED'}
        else:
            sel_faces = [f for f in bm.faces if f.select]
            if len(sel_faces) != 1:
                self.report({'WARNING'}, "Must select only one face")
                return {'CANCELLED'}

        ref_face_index = props.ref_face_index
        for face in sel_faces:
            tgt_face_index = face.index
            if ref_face_index == tgt_face_index:
                self.report({'WARNING'}, "Must select different face")
                return {'CANCELLED'}

            if props.ref_obj != obj:
                self.report({'WARNING'}, "Object must be same")
                return {'CANCELLED'}

            ref_face = bm.faces[ref_face_index]
            tgt_face = bm.faces[tgt_face_index]

            # get common vertices info
            common_verts = []
            for sl in ref_face.loops:
                for dl in tgt_face.loops:
                    if sl.vert == dl.vert:
                        info = {"vert": sl.vert, "ref_loop": sl,
                                "tgt_loop": dl}
                        common_verts.append(info)
                        break

            if len(common_verts) != 2:
                self.report({'WARNING'},
                            "2 vertices must be shared among faces")
                return {'CANCELLED'}

            # get reference other vertices info
            ref_other_verts = []
            for sl in ref_face.loops:
                for ci in common_verts:
                    if sl.vert == ci["vert"]:
                        break
                else:
                    info = {"vert": sl.vert, "loop": sl}
                    ref_other_verts.append(info)

            if not ref_other_verts:
                self.report({'WARNING'}, "More than 1 vertex must be unshared")
                return {'CANCELLED'}

            # get target other vertices info
            tgt_other_verts = []
            for dl in tgt_face.loops:
                for ci in common_verts:
                    if dl.vert == ci["vert"]:
                        break
                else:
                    info = {"vert": dl.vert, "loop": dl}
                    tgt_other_verts.append(info)

            if not tgt_other_verts:
                self.report({'WARNING'}, "More than 1 vertex must be unshared")
                return {'CANCELLED'}

            tform_mtx = None
            for other_vert in ref_other_verts:
                # get reference info
                a_3d = common_verts[0]["vert"].co
                b_3d = common_verts[1]["vert"].co
                c_3d = other_vert["vert"].co
                a_uv = common_verts[0]["ref_loop"][uv_layer].uv
                b_uv = common_verts[1]["ref_loop"][uv_layer].uv
                c_uv = other_vert["loop"][uv_layer].uv

                # AB = shared edge, C = third vert of ref face
                # set up a 2D coordinate system with coordinates relative to AB
                # X = C projected onto AB, XC/AX = perpendicular/parallel to AB
                xc_3d, x_3d = common.diff_point_to_segment(a_3d, b_3d, c_3d)
                ax_3d = x_3d - a_3d
                ab_2d = Vector((0.0, (b_3d - a_3d).length))
                ac_2d = Vector((xc_3d.length,
                        math.copysign(ax_3d.length, ax_3d.dot(b_3d - a_3d))))
                ab_uv = b_uv - a_uv
                ac_uv = c_uv - a_uv

                # check for collinear verts
                if xc_3d.length < 1e-5:
                    continue

                # find affine transformation from this 2D system to UV
                #  [u] = [m11 m12] @ [x]
                #  [v]   [m21 m22]   [y]       [u1]   [x1 y1 0  0 ]   [m11]
                #                              [v1] = [0  0  x1 y1] @ [m12]
                #  u = m11*x + m12*y           [u2]   [x1 y1 0  0 ]   [m21]
                #  v = m21*x + m22*y           [v2]   [0  0  x1 y1]   [m22]
                vector_uv = Vector((ab_uv.x, ab_uv.y, ac_uv.x, ac_uv.y))
                matrix_2d = Matrix(((ab_2d.x, ab_2d.y, 0,       0      ),
                                    (0,       0,       ab_2d.x, ab_2d.y),
                                    (ac_2d.x, ac_2d.y, 0,       0      ),
                                    (0,       0,       ac_2d.x, ac_2d.y)))
                try:
                    m_coeffs = solve(matrix_2d, vector_uv)
                    tform_mtx = Matrix(((m_coeffs[0], m_coeffs[1]),
                                        (m_coeffs[2], m_coeffs[3])))
                    break
                except:
                    pass # loop and try a different C

            if tform_mtx is None:
                self.report({'WARNING'}, "Invalid reference face")
                return {'CANCELLED'}

            # find UVs for target vertices
            for info in tgt_other_verts:
                d_3d = info["vert"].co
                zd_3d, z_3d = common.diff_point_to_segment(a_3d, b_3d, d_3d)
                az_3d = z_3d - a_3d
                ad_2d = Vector((-zd_3d.length,
                        math.copysign(az_3d.length, az_3d.dot(b_3d - a_3d))))
                ad_uv = tform_mtx @ ad_2d
                d_uv = ad_uv + a_uv
                info["target_uv"] = d_uv

            # apply to common UVs
            for info in common_verts:
                info["tgt_loop"][uv_layer].uv = \
                    info["ref_loop"][uv_layer].uv.copy()
            # apply to other UVs
            for info in tgt_other_verts:
                info["loop"][uv_layer].uv = info["target_uv"]

            common.debug_print("===== Target Other Vertices =====")
            common.debug_print(tgt_other_verts)

            bmesh.update_edit_mesh(obj.data)

            ref_face_index = tgt_face_index

        if sc.muv_texture_wrap_set_and_refer:
            props.ref_face_index = tgt_face_index

        return {'FINISHED'}
