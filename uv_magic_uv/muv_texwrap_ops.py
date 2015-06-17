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
        props.src_vlist = []
        props.src_uvlist = []
        selected_face = None
        for f in bm.faces:
            if f.select:
                for l in f.loops:
                    props.src_vlist.append(l.vert.co.copy())
                    props.src_uvlist.append(l[uv_layer].uv.copy())
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

        dest_vlist = []
        dest_uvlist = []
        dest_llist = []
        for f in bm.faces:
            if f.select:
                for l in f.loops:
                    dest_vlist.append(l.vert.co.copy())
                    dest_uvlist.append(l[uv_layer].uv.copy())
                    dest_llist.append(l)
        if len(dest_llist) < 1:
            self.report({'WARNING'}, "Number of faces must be more 1")
            return {'CANCELLED'}

        # transform 3D coord to 2D coord about verticies
        v = props.src_vlist[0:3]
        trans_mat = Matrix.Translation(-v[0])
        src_vlist_2d = [trans_mat * sv for sv in props.src_vlist]
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
        trans_uv = props.src_uvlist[0].copy()
        src_uvlist_2d = [suv - trans_uv for suv in props.src_uvlist]
        uv = src_uvlist_2d[1].copy()
        uv_rot_mat = Matrix.Rotation(atan2(uv.y, uv.x), 2, 'Z')
        src_uvlist_2d = [uv_rot_mat * suv for suv in src_uvlist_2d]

        # calculate destination UV coordinate
        dest_uvlist_2d = []
        ov = src_vlist_2d[0].copy()
        ouv = src_uvlist_2d[0].copy()
        r = (src_uvlist_2d[1].x - src_uvlist_2d[0].x) / (src_vlist_2d[1].x - src_vlist_2d[0].x)
        nsv = len(src_uvlist_2d)
        for i, dv in enumerate(dest_vlist_2d):
            idx = i % nsv
            u = src_uvlist_2d[idx].x + (dv.x - src_vlist_2d[idx].x) * r
            w = src_uvlist_2d[idx].y + (dv.y - src_vlist_2d[idx].y) * r
            dest_uvlist_2d.append(Vector((u, w)))

        # reverse transform
        dest_uvlist_2d = [uv_rot_mat.transposed() * duv for duv in dest_uvlist_2d]
        dest_uvlist_2d = [duv + trans_uv for duv in dest_uvlist_2d]

        # update UV coordinate
        for uv, l in zip(dest_uvlist_2d, dest_llist):
            l[uv_layer].uv = uv.copy()

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()

        return {'FINISHED'}
