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
import bmesh
from . import muv_common
from mathutils import Vector, Matrix
from math import atan2, sqrt

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"


def redraw_all_areas():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


def get_dest_uvlist(src_vlist, src_uvlist, dest_vlist):
    # transform 3D coord to 2D coord about verticies
    v = src_vlist[0:3]
    trans_mat = Matrix.Translation(-v[0])
    src_vlist_2d = [trans_mat * sv for sv in src_vlist]
    v = src_vlist_2d[0:3]
    rotz_mat = Matrix.Rotation(-atan2(v[1].y, v[1].x), 3, 'Z')
    src_vlist_2d = [rotz_mat * sv for sv in src_vlist_2d]
    v = src_vlist_2d[0:3]
    roty_mat = Matrix.Rotation(atan2(v[1].z, sqrt(v[1].x * v[1].x + v[1].y * v[1].y)), 3, 'Y')
    src_vlist_2d = [roty_mat * sv for sv in src_vlist_2d]
    v = src_vlist_2d[0:3]
    rotx_mat = Matrix.Rotation(-atan2(v[2].z, v[2].y), 3, 'X')
    src_vlist_2d = [rotx_mat * sv for sv in src_vlist_2d]
    for sv in src_vlist_2d:
        sv.z = 0.0
    dest_vlist_2d = [trans_mat * dv for dv in dest_vlist]
    dest_vlist_2d = [rotz_mat * dv for dv in dest_vlist_2d]
    dest_vlist_2d = [roty_mat * dv for dv in dest_vlist_2d]
    dest_vlist_2d = [rotx_mat * dv for dv in dest_vlist_2d]
    for dv in dest_vlist_2d:
        dv.z = 0.0

    # transform UV coordinate for calculation
    trans_uv = src_uvlist[0].copy()
    src_uvlist_2d = [suv - trans_uv for suv in src_uvlist]
    uv = src_uvlist_2d[1].copy()
    uv_rot_mat = Matrix.Rotation(atan2(uv.y, uv.x), 2, 'Z')
    src_uvlist_2d = [uv_rot_mat * suv for suv in src_uvlist_2d]

    # calculate destination UV coordinate
    dest_uvlist_2d = []
    ov = src_vlist_2d[0].copy()
    ouv = src_uvlist_2d[0].copy()
    r = (src_uvlist_2d[1].x - src_uvlist_2d[0].x) / (src_vlist_2d[1].x - src_vlist_2d[0].x)
    for sv, suv, dv in zip(src_vlist_2d, src_uvlist_2d, dest_vlist_2d):
        u = suv.x + (dv.x - sv.x) * r
        w = suv.y + (dv.y - sv.y) * r
        dest_uvlist_2d.append(Vector((u, w)))

    # reverse transform
    dest_uvlist_2d = [uv_rot_mat.transposed() * duv for duv in dest_uvlist_2d]
    dest_uvlist_2d = [duv + trans_uv for duv in dest_uvlist_2d]

    return dest_uvlist_2d


# Project texture along the face (Set)
class MUV_TexProjFaceSet(bpy.types.Operator):
    """Set texture to be projected."""

    bl_idname = "uv.muv_texproj_face_set"
    bl_label = "Set"
    bl_description = "Set texture to be projected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texproj_face
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        props.src_vlist = []
        props.src_uvlist = []
        selected = 0
        for f in bm.faces:
            if f.select:
                props.src_vlist = [l.vert.co.copy() for l in f.loops]
                props.src_uvlist = [l[uv_layer].uv.copy() for l in f.loops]
                selected = selected + 1
        if selected != 1:
            self.report({'WARNING'}, "Number of selected face must be one")
            return {'CANCELLED'}

        return {'FINISHED'}


# Project texture along the face (Project)
class MUV_TexProjFaceProject(bpy.types.Operator):
    """Set texture to be projected."""

    bl_idname = "uv.muv_texproj_face_proj"
    bl_label = "Project"
    bl_description = "Project texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texproj_face
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        dest_vlists = []
        dest_llists = []
        for f in bm.faces:
            if f.select:
                dest_vlists.append([l.vert.co.copy() for l in f.loops])
                dest_llists.append([l for l in f.loops])
        if len(dest_vlists) <= 0:
            self.report({'WARNING'}, "No face is selected")
            return {'CANCELLED'}

        for dest_vlist, dest_llist in zip(dest_vlists, dest_llists):
            dest_uvlist_2d = get_dest_uvlist(props.src_vlist, props.src_uvlist, dest_vlist)
            # update UV coordinate
            for uv, l in zip(dest_uvlist_2d, dest_llist):
                l[uv_layer].uv = uv.copy()

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()

        return {'FINISHED'}

