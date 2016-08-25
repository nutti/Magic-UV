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
from math import atan2, sqrt, fabs, sin, cos, acos

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"

def planarize(faces):
    # get common verticies among two faces
    common_verts = []
    for l0 in faces[0].loops:
        for l1 in faces[1].loops: 
            if l0.vert == l1.vert:
                common_verts.append(l0.vert)

    # get rotation axis
    axis = common_verts[1].co - common_verts[0].co
    
    # get rotation angle
    angle_verts = [None, None]
    for e in common_verts[0].link_edges:
        ov = e.other_vert(common_verts[0])
        if ov != common_verts[1] and faces[0] in ov.link_faces:
            angle_verts[0] = ov
        elif ov != common_verts[1] and faces[1] in ov.link_faces:
            angle_verts[1] = ov
    v0 = angle_verts[0].co - common_verts[0].co
    v1 = common_verts[0].co - angle_verts[1].co
    theta = acos(v0.dot(v1) / (v0.magnitude * v1.magnitude))
    
    # 1st trial
    # make transform matrix
    axis.normalize()
    mi = Matrix.Identity(3)
    mr = Matrix((
            (0, -axis[2], axis[1]),
            (axis[2], 0, -axis[0]),
            (-axis[1], axis[0], 0)
            ))
    mat = mi + sin(theta) * mr + (1 - cos(theta)) * mr * mr
    mat = mat.to_4x4()
    mat[3][3] = 1
    
    # transform
    other_verts = [l1.vert for l1 in faces[1].loops if not l1.vert in common_verts]
    old_vco = [ov.co.copy() for ov in other_verts]
    for v in other_verts:
        new = (v.co - common_verts[0].co) * mat + common_verts[0].co
        v.co = new.copy()

    # 2nd trial if rotation dirction is incorrect
    v0 = angle_verts[0].co - common_verts[0].co
    v1 = common_verts[0].co - angle_verts[1].co
    phi = acos(v0.dot(v1) / (v0.magnitude * v1.magnitude))
    if fabs(phi) > 0.0001: 
        for v, co in zip(other_verts, old_vco):
            v.co = co.copy()
        # 2nd trial
        theta = -theta
        mat = mi + sin(theta) * mr + (1 - cos(theta)) * mr * mr
        mat = mat.to_4x4()
        mat[3][3] = 1
        # transform
        other_verts = [l1.vert for l1 in faces[1].loops if not l1.vert in common_verts]
        for v in other_verts:
            new = (v.co - common_verts[0].co) * mat + common_verts[0].co
            v.co = new

    # get ratio
    ratio = Vector((0.0, 0.0))
    dv = common_verts[0].co - angle_verts[0].co
    ratio.x = dv.magnitude
    dv = common_verts[1].co - common_verts[0].co
    ratio.y = dv.magnitude
    
    return ratio


def redraw_all_areas():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


def get_dest_uvlist(src_vlist, src_uvlist, dest_vlist, ratio):
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

    dv = src_vlist_2d[1] - src_vlist_2d[0]
    duv = src_uvlist_2d[1] - src_uvlist_2d[0]
    duv3 = Vector((duv.x, duv.y, 0.0))

    dv_duv_angle = dv.dot(duv3)/(dv.magnitude * duv3.magnitude)
    dv_duv_angle = min(1, max(dv_duv_angle, -1))
    print(dv_duv_angle)
    print(acos(dv_duv_angle))

    rx = (src_uvlist_2d[1].x - src_uvlist_2d[0].x) / ratio.x
    ry = (src_uvlist_2d[1].y - src_uvlist_2d[0].y) / ratio.y
    for sv, suv, dv in zip(src_vlist_2d, src_uvlist_2d, dest_vlist_2d):
        u = suv.x + (dv.x - sv.x) * rx
        w = suv.y + (dv.y - sv.y) * ry
        dest_uvlist_2d.append(Vector((u, w)))

    # reverse transform
    dest_uvlist_2d = [uv_rot_mat.transposed() * duv for duv in dest_uvlist_2d]
    dest_uvlist_2d = [duv + trans_uv for duv in dest_uvlist_2d]

    return src_vlist_2d, src_uvlist_2d, dest_vlist_2d, dest_uvlist_2d


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

        src_llist = [l for l in src_face.loops]
        dest_llist = [l for l in dest_face.loops]
        src_vlist_orig = [l.vert.co.copy() for l in src_face.loops]
        dest_vlist_orig = [l.vert.co.copy() for l in dest_face.loops]
        
        ratio = planarize([src_face, dest_face])
        
        src_vlist = [l.vert.co.copy() for l in src_face.loops]
        src_uvlist = [l[uv_layer].uv.copy() for l in src_face.loops]
        dest_vlist = [l.vert.co.copy() for l in dest_face.loops]
        src_vlist_2d, src_uvlist_2d, dest_vlist_2d, dest_uvlist_2d = get_dest_uvlist(src_vlist, src_uvlist, dest_vlist, ratio)

        # update UV coordinate
        for uv, sl, dl, sv, dv in zip(dest_uvlist_2d, src_llist, dest_llist, src_vlist_2d, dest_vlist_2d):
        #for uv, sl, dl, sv, dv in zip(dest_uvlist_2d, src_llist, dest_llist, src_vlist_orig, dest_vlist_orig):
            dl[uv_layer].uv = uv.copy()
            sl.vert.co = sv
            dl.vert.co = dv

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()

        return {'FINISHED'}
