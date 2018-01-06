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

__author__ = "McBuff, Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.5"
__date__ = "19 Nov 2017"


from math import fabs, sqrt

import bpy
import bmesh
from mathutils import Vector
from bpy.props import (
    FloatProperty,
    BoolProperty,
    EnumProperty
)
from . import muv_common


def calc_edge_scale(uv_layer, loop0, loop1):
    v0 = loop0.vert.co
    v1 = loop1.vert.co
    uv0 = loop0[uv_layer].uv.copy()
    uv1 = loop1[uv_layer].uv.copy()

    dv = v1 - v0
    duv = uv1 - uv0

    scale = 0.0
    if dv.magnitude > 0.00000001:
        scale = duv.magnitude / dv.magnitude

    return scale


def calc_face_scale(uv_layer, face):
    es = 0.0
    for i, l in enumerate(face.loops[1:]):
        es = es + calc_edge_scale(uv_layer, face.loops[i], l)

    return es


def calc_polygon_2d_area(points):
    area = 0.0
    for i, p1 in enumerate(points):
        p2 = points[(i + 1) % len(points)]
        a = p1.x * p2.y - p1.y * p2.x
        area = area + a

    return fabs(0.5 * area)


def calc_polygon_3d_area(points):
    area = 0.0
    for i, p1 in enumerate(points):
        p2 = points[(i + 1) % len(points)]
        cx = p1.y * p2.z - p1.z * p2.y
        cy = p1.z * p2.x - p1.x * p2.z
        cz = p1.x * p2.y - p1.y * p2.x
        a = sqrt(cx * cx + cy * cy + cz * cz)
        area = area + a

    return 0.5 * area


def measure_wsuv_info(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    if muv_common.check_version(2, 73, 0) >= 0:
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

    if not bm.loops.layers.uv:
        return None, None, None
    uv_layer = bm.loops.layers.uv.verify()

    tex_layer = None
    if bm.faces.layers.tex:
        tex_layer = bm.faces.layers.tex.verify()

    sel_faces = [f for f in bm.faces if f.select]

    # measure average face size
    uv_area = 0.0
    mesh_area = 0.0
    for f in sel_faces:
        uvs = [l[uv_layer].uv for l in f.loops]
        verts = [l.vert.co for l in f.loops]
        uv_area = uv_area + calc_polygon_2d_area(uvs)
        if tex_layer:
            img = f[tex_layer].image
            uv_area = uv_area * img.size[0] * img.size[1]
        mesh_area = mesh_area + calc_polygon_3d_area(verts)
    if mesh_area == 0.0:
        density = 0.0
    else:
        density = sqrt(uv_area / mesh_area)

    return uv_area, mesh_area, density


class MUV_WSUVMeasure(bpy.types.Operator):
    """
    Operation class: Measure face size
    """

    bl_idname = "uv.muv_wsuv_measure"
    bl_label = "Measure"
    bl_description = "Measure face size for scale calculation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sc = context.scene
        obj = context.active_object

        uv_area, mesh_area, density = measure_wsuv_info(obj)

        sc.muv_wsuv_src_uv_area = uv_area
        sc.muv_wsuv_src_mesh_area = mesh_area
        sc.muv_wsuv_src_density = density

        self.report({'INFO'},
                    "UV Area: {0}, Mesh Area: {1}, Texel Density: {2}"
                    .format(uv_area, mesh_area, density))

        return {'FINISHED'}


class MUV_WSUVApply(bpy.types.Operator):
    """
    Operation class: Apply scaled UV
    """

    bl_idname = "uv.muv_wsuv_apply"
    bl_label = "Apply"
    bl_description = "Apply scaled UV based on scale calculation"
    bl_options = {'REGISTER', 'UNDO'}

    proportional_scaling = BoolProperty(
        name="Proportional Scaling",
        default=True
    )
    scaling_factor = FloatProperty(
        name="Scaling Factor",
        default=1.0,
        max=1000.0,
        min=0.00001
    )
    origin = EnumProperty(
        name="Origin",
        description="Aspect Origin",
        items=[
            ('CENTER', 'Center', 'Center'),
            ('LEFT_TOP', 'Left Top', 'Left Bottom'),
            ('LEFT_CENTER', 'Left Center', 'Left Center'),
            ('LEFT_BOTTOM', 'Left Bottom', 'Left Bottom'),
            ('CENTER_TOP', 'Center Top', 'Center Top'),
            ('CENTER_BOTTOM', 'Center Bottom', 'Center Bottom'),
            ('RIGHT_TOP', 'Right Top', 'Right Top'),
            ('RIGHT_CENTER', 'Right Center', 'Right Center'),
            ('RIGHT_BOTTOM', 'Right Bottom', 'Right Bottom')

        ],
        default="CENTER"
    )

    def draw(self, _):
        layout = self.layout

        layout.prop(self, "proportional_scaling")
        if not self.proportional_scaling:
            layout.prop(self, "scaling_factor")
        layout.prop(self, "origin")

    def execute(self, context):
        sc = context.scene
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()

        if not bm.loops.layers.uv:
            self.report(
                {'WARNING'}, "Object must have more than one UV map")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        sel_faces = [f for f in bm.faces if f.select]

        factor = sc.muv_wsuv_src_density / sc.muv_wsuv_tgt_density

        # calculate origin
        if self.origin == 'CENTER':
            origin = Vector((0.0, 0.0))
            num = 0
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin = origin + uv
                    num = num + 1
            origin = origin / num
        elif self.origin == 'LEFT_TOP':
            origin = Vector((100000.0, -100000.0))
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = min(origin.x, uv.x)
                    origin.y = max(origin.y, uv.y)
        elif self.origin == 'LEFT_CENTER':
            origin = Vector((100000.0, 0.0))
            num = 0
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = min(origin.x, uv.x)
                    origin.y = origin.y + uv.y
                    num = num + 1
            origin.y = origin.y / num
        elif self.origin == 'LEFT_BOTTOM':
            origin = Vector((100000.0, 100000.0))
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = min(origin.x, uv.x)
                    origin.y = min(origin.y, uv.y)
        elif self.origin == 'CENTER_TOP':
            origin = Vector((0.0, -100000.0))
            num = 0
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = origin.x + uv.x
                    origin.y = max(origin.y, uv.y)
                    num = num + 1
            origin.x = origin.x / num
        elif self.origin == 'CENTER_BOTTOM':
            origin = Vector((0.0, 100000.0))
            num = 0
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = origin.x + uv.x
                    origin.y = min(origin.y, uv.y)
                    num = num + 1
            origin.x = origin.x / num
        elif self.origin == 'RIGHT_TOP':
            origin = Vector((-100000.0, -100000.0))
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = max(origin.x, uv.x)
                    origin.y = max(origin.y, uv.y)
        elif self.origin == 'RIGHT_CENTER':
            origin = Vector((-100000.0, 0.0))
            num = 0
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = max(origin.x, uv.x)
                    origin.y = origin.y + uv.y
                    num = num + 1
            origin.y = origin.y / num
        elif self.origin == 'RIGHT_BOTTOM':
            origin = Vector((-100000.0, 100000.0))
            for f in sel_faces:
                for l in f.loops:
                    uv = l[uv_layer].uv
                    origin.x = max(origin.x, uv.x)
                    origin.y = min(origin.y, uv.y)

        # update UV coordinate
        for f in sel_faces:
            for l in f.loops:
                uv = l[uv_layer].uv
                diff = uv - origin
                l[uv_layer].uv = origin + diff * factor

        bmesh.update_edit_mesh(obj.data)

        self.report({'INFO'}, "Scaling factor: {0}".format(factor))

        return {'FINISHED'}
