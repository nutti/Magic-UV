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
from math import atan2, sqrt, fabs

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
    rx = 0
    ry = 0
    #for i in range(len(src_uvlist_2d)):
    #    for j in range(len(src_uvlist_2d)):
    #        if i != j:
    #            rx_new = (src_uvlist_2d[j].x - src_uvlist_2d[i].x) / (src_vlist_2d[j].x - src_vlist_2d[i].x)
    #            rx = max(rx, fabs(rx_new))
    #            ry_new = (src_uvlist_2d[j].y - src_uvlist_2d[i].y) / (src_vlist_2d[j].y - src_vlist_2d[i].y)
    #            ry = max(ry, fabs(ry_new))
    dx = src_vlist_2d[1].x - src_vlist_2d[0].x
    dy = src_vlist_2d[1].y - src_vlist_2d[0].y
    if dx > 0.0001:
        r = (src_uvlist_2d[1].x - src_uvlist_2d[0].x) / dx
    else:
        r = (src_uvlist_2d[1].y - src_uvlist_2d[0].y) / dy
    for sv, suv, dv in zip(src_vlist_2d, src_uvlist_2d, dest_vlist_2d):
        u = suv.x + (dv.x - sv.x) * r
        w = suv.y + (dv.y - sv.y) * r
        dest_uvlist_2d.append(Vector((u, w)))

    # reverse transform
    dest_uvlist_2d = [uv_rot_mat.transposed() * duv for duv in dest_uvlist_2d]
    dest_uvlist_2d = [duv + trans_uv for duv in dest_uvlist_2d]

    return dest_uvlist_2d


# Texture wrap (copy)
class MUV_TexWrapCopy(bpy.types.Operator):
    """."""

    bl_idname = "uv.muv_texwrap_copy"
    bl_label = "Texture Wrap Copy"
    bl_description = "Texture Wrap Copy"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texwrap
        self.report({'INFO'}, "Texture Wrap Copy.")
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()
        
        # get selected face
        props.src_face_index = -1
        for f in bm.faces:
            if f.select:
                props.src_face_index = f.index
                break
        else:
            self.report({'WARNING'}, "No faces are selected.")
            return {'CANCELLED'}

        return {'FINISHED'}


# Texture wrap (paste)
class MUV_TexWrapPaste(bpy.types.Operator):
    """Paste UV coordinate which is copied."""

    bl_idname = "uv.muv_texwrap_paste"
    bl_label = "Texture Wrap Paste"
    bl_description = "Texture Wrap Paste"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texwrap
        self.report({'INFO'}, "Texture Wrap Paste.")
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        src_face = bm.faces[props.src_face_index]
        dest_face = None
        for f in bm.faces:
            if f.select:
                dest_face = f
                break
        else:
            self.report({'WARNING'}, "No faces are selected.")
            return {'CANCELLED'}

        rot = dest_face.normal.rotation_difference(src_face.normal).to_matrix()
        pivot = list(set(src_face.edges[:]).intersection(set(dest_face.edges)))[0]
        pivot_coos = [obj.matrix_world * v.co for v in pivot.verts]
        pivot_vec = (pivot_coos[0] + pivot_coos[1]) / 2

        src_vlist = [l.vert.co.copy() for l in src_face.loops]
        src_uvlist = [l[uv_layer].uv.copy() for l in src_face.loops]
        dest_vlist_orig = [l.vert.co.copy() for l in dest_face.loops]
        dest_uvlist = [l[uv_layer].uv.copy() for l in dest_face.loops]
        dest_llist = [l for l in dest_face.loops]

        bmesh.ops.rotate(bm, cent=pivot_vec, matrix=rot, verts=dest_face.verts, space=obj.matrix_world)
        dest_vlist = [l.vert.co.copy() for l in dest_face.loops]

        dest_uvlist_2d = get_dest_uvlist(src_vlist, src_uvlist, dest_vlist)

        # update UV coordinate
        for uv, l, v in zip(dest_uvlist_2d, dest_llist, dest_vlist_orig):
            l[uv_layer].uv = uv.copy()
            l.vert.co = v

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()

        return {'FINISHED'}
