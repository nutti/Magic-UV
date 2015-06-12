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


__author__ = "Nutti, Mifth"
__status__ = "production"
__version__ = "3.0"
__date__ = "XXX"

copied = None

class CPUVCopiedStuff():

    # class constructor
    def __init__(self, obj_name):
        self.obj_name = obj_name
        self.faces = []


# Topology UV (copy)
class CPUVTopoCopy(bpy.types.Operator):
    """Topology UV copy."""

    bl_idname = "uv.topology_uv_copy"
    bl_label = "Topology UV Copy"
    bl_description = "Topology UV Copy."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj = context.scene.objects.active
        bm = bmesh.from_edit_mesh(active_obj.data)

        active_face = bm.faces.active
        sel_faces = [face for face in bm.faces if face.select]
        #sel_edges = [edge for edge in bm.edges if edge.select]
        #sel_verts = [vert for vert in bm.verts if vert.select]

        cross_edge = None
        act_face_verts = []
        act_face_edges = []
        uv_layer = bm.loops.layers.uv.active
        for edge in active_face.edges:
            if edge in sel_faces[0].edges and edge in sel_faces[1].edges:
                cross_edge = edge
                dn = active_face.normal.copy().normalized()
                dv_1 = (edge.verts[0].co - edge.verts[1].co).normalized()
                dv_2 = (edge.verts[1].co - edge.verts[0].co).normalized()

                if dn.cross(dv_1).dot(dn) > 0:
                    act_face_verts.append(edge.verts[0])
                    act_face_verts.append(edge.verts[1])
                else:
                    act_face_verts.append(edge.verts[1])
                    act_face_verts.append(edge.verts[0])

                act_face_edges.append(edge)
                get_other_verts_edges(active_face, act_face_verts, act_face_edges)
                break

        #for loop in act_face_verts[0].link_loops:
            #print(loop[uv_layer])

        return {'FINISHED'}


def get_other_verts_edges(face, face_verts, face_edges):
    other_edges = [edge for edge in face.edges if edge not in face_edges]

    for i in range(len(other_edges)):
        found_edge = None

        for edge in other_edges:
            if face_verts[-1] in edge.verts:
                if face_verts[-1] is edge.verts[0]:
                    if edge.verts[1] not in face_verts:
                        face_verts.append(edge.verts[1])
                elif face_verts[-1] is edge.verts[1]:
                    if edge.verts[0] not in face_verts:
                        face_verts.append(edge.verts[0])

                found_edge = edge
                face_edges.append(edge)
                break

        other_edges.remove(found_edge)


