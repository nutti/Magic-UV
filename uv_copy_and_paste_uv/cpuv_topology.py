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

        uv_layer = bm.loops.layers.uv.active
        #uv_layer = bm.loops.layers.uv.verify()
        all_sorted_faces = {}  # This is the main stuff

        used_verts = set()
        used_edges = set()

        active_face = bm.faces.active
        sel_faces = [face for face in bm.faces if face.select]
        faces_to_parse = []

        if len(sel_faces) != 2 and active_face and active_face in sel_faces:
            self.report({'WARNING'}, "Two faces should be selected and active!!")
            return {'CANCELLED'}

        # get first grow of two faces
        for edge in active_face.edges:
            if edge in sel_faces[0].edges and edge in sel_faces[1].edges:
                cross_edge = edge
                vert1 = None
                vert2 = None

                dot_n = active_face.normal.copy().normalized()
                dot_v_1 = (edge.verts[0].co - edge.verts[1].co).normalized()
                dot_v_2 = (edge.verts[1].co - edge.verts[0].co).normalized()

                if dot_n.cross(dot_v_1).dot(dot_n) > 0:
                    vert1 = edge.verts[0]
                    vert2 = edge.verts[1]
                else:
                    vert1 = edge.verts[1]
                    vert2 = edge.verts[0]

                # get active face stuff and uvs
                face_stuff = get_other_verts_edges(active_face, vert1, vert2, cross_edge, uv_layer)
                all_sorted_faces[active_face] = face_stuff
                used_verts.update(active_face.verts)
                used_edges.update(active_face.edges)

                # get first selected face stuff and uvs as they share cross_edge
                second_face = sel_faces[0]
                if second_face is active_face:
                    second_face = sel_faces[1]
                face_stuff = get_other_verts_edges(second_face, vert1, vert2, cross_edge, uv_layer)
                all_sorted_faces[second_face] = face_stuff
                used_verts.update(second_face.verts)
                used_edges.update(second_face.edges)

                # first Grow
                faces_to_parse.append(active_face)
                faces_to_parse.append(second_face)

                break

        ## get all connected stuff
        #grow_list_faces = sel_faces.copy()
        #grow_used_verts = used_verts.copy()

        #while True:
            #new_grow = grow_selection(grow_used_verts, grow_list_faces, bm)
            ##print(new_grow)
            #if not new_grow[0]:
                #break

            #grow_list_faces += new_grow[0]
            #grow_used_verts.update(new_grow[1])

        # parse all faces
        while True:
            new_parsed_faces = []

            if not faces_to_parse:
                break

            for face in faces_to_parse:
                face_stuff = all_sorted_faces.get(face)
                new_faces = parse_faces(face, face_stuff, used_verts, used_edges, all_sorted_faces, uv_layer, self)
                new_parsed_faces += new_faces

            faces_to_parse.clear()
            faces_to_parse = new_parsed_faces

        bmesh.update_edit_mesh(active_obj.data)

        return {'FINISHED'}


# recurse faces around the new_grow only
def parse_faces(check_face, face_stuff, used_verts, used_edges, all_sorted_faces, uv_layer, self):
    new_shared_faces = []

    for sorted_edge in face_stuff[1]:
        shared_faces = sorted_edge.link_faces

        if shared_faces:

            if len(shared_faces) > 2:
                bpy.ops.mesh.select_all(action='DESELECT')
                for face_sel in shared_faces:
                    face_sel.select = True

                self.report({'WARNING'}, str(len(shared_faces)) + " faces share edge!!")
                break
                return {'CANCELLED'}

            clear_shared_faces = get_new_shared_faces(check_face, sorted_edge, shared_faces, all_sorted_faces.keys())

            if clear_shared_faces:
                shared_face = clear_shared_faces[0]
                #if check_face is shared_face:
                    #shared_face = clear_shared_faces[1]

                # get verts of the edge
                vert1 = sorted_edge.verts[0]
                vert2 = sorted_edge.verts[1]

                #print(face_stuff[0], vert1, vert2)
                if face_stuff[0].index(vert1) > face_stuff[0].index(vert2):
                    vert1 = sorted_edge.verts[1]
                    vert2 = sorted_edge.verts[0]

                #print(shared_face.verts, vert1, vert2)
                new_face_stuff = get_other_verts_edges(shared_face, vert1, vert2, sorted_edge, uv_layer)
                all_sorted_faces[shared_face] = new_face_stuff
                used_verts.update(shared_face.verts)
                used_edges.update(shared_face.edges)

                shared_face.select = True  # test

                ## recurse this methdwith shared face
                #parse_faces(shared_face, new_face_stuff, used_verts, used_edges, all_sorted_faces, uv_layer, self, grow_list_faces)

                new_shared_faces.append(shared_face)

    return new_shared_faces

def get_new_shared_faces(orig_face, shared_edge, check_faces, used_faces):
    shared_faces = []

    for face in check_faces:
        if shared_edge in face.edges and face not in used_faces and face is not orig_face:
            shared_faces.append(face)

    return shared_faces


#def grow_selection(used_verts, used_faces, bm):
    #growed_faces = []
    #growed_verts = []

    #for face in bm.faces:
        #if face not in used_faces:
            #for vert in face.verts: 
                #if vert in used_verts:
                    #growed_faces.append(face)
                    #growed_verts += [vert2 for vert2 in face.verts]
                    #break

    #return [growed_faces, growed_verts]


def get_other_verts_edges(face, vert1, vert2, first_edge, uv_layer):
    face_edges = [first_edge]
    face_verts = [vert1, vert2]
    face_uvs = []

    other_edges = [edge for edge in face.edges if edge not in face_edges]

    for i in range(len(other_edges)):
        found_edge = None

        # get sorted verts and edges
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

    # get sorted uvs
    for vert in face_verts:
        for loop in face.loops:
            if loop.vert == vert:
                face_uvs.append(loop[uv_layer].uv.copy())
                break

    return [face_verts, face_edges, face_uvs]

