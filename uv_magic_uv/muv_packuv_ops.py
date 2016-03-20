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
from bpy.props import FloatProperty
from mathutils import Vector
from math import fabs
from collections import defaultdict
from . import muv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"


# pack UV
class MUV_PackUV(bpy.types.Operator):
    bl_idname = "uv.muv_packuv"
    bl_label = "Pack UV"
    bl_description = "Pack UV (Same UV Islands are integrated)"
    bl_options = {'REGISTER', 'UNDO'}

    __face_to_verts = defaultdict(set)
    __vert_to_faces = defaultdict(set)

    pack_margin = FloatProperty(
        name="Pack Margin",
        description="Margin used by default pack UV function",
        min=0,
        max=1,
        default=0.272269)

    def execute(self, context):
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        island_info = []
        uv_island_lists = []

        for f in bm.faces:
            for l in f.loops:
                id = l[uv_layer].uv.to_tuple(5), l.vert.index
                self.__face_to_verts[f.index].add(id)
                self.__vert_to_faces[id].add(f.index)

        uv_island_lists = self.__get_island(bm, uv_layer)

        # get information about each island
        for island in uv_island_lists:
            info = {}
            max = Vector((-10000000.0, -10000000.0))
            min = Vector((10000000.0, 10000000.0))
            ave = Vector((0.0, 0.0))
            num = 0
            for face in island:
                for l in face['loops']:
                    uv = l['uv']
                    if uv.x > max.x:
                        max.x = uv.x
                    if uv.y > max.y:
                        max.y = uv.y
                    if uv.x < min.x:
                        min.x = uv.x
                    if uv.y < min.y:
                        min.y = uv.y
                    ave = ave + uv
                    num = num + 1
            ave = ave / num

            info['center'] = ave
            info['size'] = max - min
            info['num_uv'] = num
            info['group'] = -1
            info['faces'] = island

            island_info.append(info)

        # check if there is same island
        num_group = 0
        while True:
            for isl in island_info:
                if isl['group'] == -1:
                    break
            else:
                break
            isl['group'] = num_group
            for isl_2 in island_info:
                if isl_2['group'] == -1:
                    center_x_matched = (fabs(isl_2['center'].x - isl['center'].x) < 0.001)
                    center_y_matched = (fabs(isl_2['center'].y - isl['center'].y) < 0.001)
                    size_x_matched = (fabs(isl_2['size'].x - isl['size'].x) < 0.001)
                    size_y_matched = (fabs(isl_2['size'].y - isl['size'].y) < 0.001)
                    center_matched = center_x_matched and center_y_matched
                    size_matched = size_x_matched and size_y_matched
                    num_uv_matched = (isl_2['num_uv'] == isl['num_uv'])
                    if center_matched and size_matched and num_uv_matched:
                        isl_2['group'] = num_group
                        # find two same UV pair for transfering UV
                        face_pair_1 = isl['faces'][0:2]
                        face_pair_2 = []
                        
                        face_sorted_1 = isl['faces']
                        face_sorted_2 = []
                        for f1 in face_sorted_1:
                            for f2 in isl_2['faces']:
                                if len(f1['loops']) != len(f2['loops']):
                                    continue
                                matched = True
                                for l1, l2 in zip(f1['loops'], f2['loops']):
                                    if (fabs(l1['uv'].x - l2['uv'].x) > 0.001) or (fabs(l1['uv'].y - l2['uv'].y) > 0.001):
                                        matched = False
                                if not matched:
                                    continue
                                face_sorted_2.append(f2)
                                break
                            else:
                                self.report({'WARNING'}, "Internal Error")
                                return {'CANCELLED'}
                        isl['sorted'] = face_sorted_1
                        isl_2['sorted'] = face_sorted_2
            num_group = num_group + 1

        loop_lists = [l for f in bm.faces for l in f.loops]

        bpy.ops.mesh.select_all(action='DESELECT')

        # pack UV
        for gidx in range(num_group):
            group = list(filter(lambda i:i['group']==gidx, island_info))
            for f in group[0]['faces']:
                bm.faces[f['face_idx']].select = True


        bmesh.update_edit_mesh(obj.data)

        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(margin=self.pack_margin)

        # copy/paste UV among same island
        for gidx in range(num_group):
            group = list(filter(lambda i:i['group']==gidx, island_info))
            if len(group) <= 1:
                continue
            for g in group[1:]:
                for (src_face, dest_face) in zip(group[0]['sorted'], g['sorted']):
                    for (src_loop, dest_loop) in zip(src_face['loops'], dest_face['loops']):
                        loop_lists[dest_loop['loop_idx']][uv_layer].uv = loop_lists[src_loop['loop_idx']][uv_layer].uv

        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}


    def __parse_island(self, bm, uv_layer, face_idx, faces_left, island):
        if face_idx in faces_left:
            faces_left.remove(face_idx)
            current_face = {'face_idx': face_idx, 'loops': []}
            for l in bm.faces[face_idx].loops:
                current_face['loops'].append({'uv': l[uv_layer].uv, 'loop_idx': l.index})
            island.append(current_face)
            for v in self.__face_to_verts[face_idx]:
                connected_faces = self.__vert_to_faces[v]
                if connected_faces:
                    for cf in connected_faces:
                        self.__parse_island(bm, uv_layer, cf, faces_left, island)

    def __get_island(self, bm, uv_layer):
        uv_island_lists = []
        faces_left = set(self.__face_to_verts.keys())
        while len(faces_left) > 0:
            current_island = []
            face_idx = list(faces_left)[0]
            self.__parse_island(bm, uv_layer, face_idx, faces_left, current_island)
            uv_island_lists.append(current_island)
        return uv_island_lists


