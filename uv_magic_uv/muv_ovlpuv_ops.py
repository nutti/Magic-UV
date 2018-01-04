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

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.5"
__date__ = "19 Nov 2017"

import itertools

import bpy
import bmesh
import bgl

from . import muv_common


def is_face_overlapped(f1, f2, uv_layer):
    if len(f1.loops) != len(f2.loops):
        return False

    l2_list = [l2 for l2 in f2.loops]
    for l1 in f1.loops:
        for l2 in l2_list:
            diff = l2[uv_layer].uv - l1[uv_layer].uv
            if diff < 0.00000001:
                l2_list.remove(l2)
                break
        else:
            return False

    return True


def check_intersect(start1, end1, start2, end2):
    seg1 = end1 - start1
    seg2 = end2 - start2

    a1 = -seg1.y
    b1 = seg1.x
    d1 = -(a1 * start1.x + b1 * start1.y)

    a2 = -seg2.y
    b2 = seg2.x
    d2 = -(a2 * start2.x + b2 * start2.y)

    seg1_line2_start = a2 * start1.x + b2 * start1.y + d2
    seg1_line2_end = a2 * end1.x + b2 * end1.y + d2

    seg2_line1_start = a1 * start2.x + b1 * start2.y + d1
    seg2_line1_end = a1 * end2.x + b1 * end2.y + d1

    if (seg1_line2_start * seg1_line2_end >= 0) or (seg2_line1_start * seg2_line1_end >= 0):
        return False, None

    u = seg1_line2_start / (seg1_line2_start - seg1_line2_end)
    out = start1 + u * seg1

    return True, out


class RingBuffer:
    def __init__(self, arr):
        self.__buffer = arr.copy()
        self.__pointer = 0

    def __repr__(self):
        return repr(self.__buffer)

    def __len__(self):
        return len(self.__buffer)

    def insert(self, val, offset=0):
        self.__buffer.insert(self.__pointer + offset, val)

    def head(self):
        return self.__buffer[0]

    def tail(self):
        return self.__buffer[-1]

    def get(self, offset=0):
        size = len(self.__buffer)
        val = self.__buffer[(self.__pointer + offset) % size]
        return val

    def next(self):
        size = len(self.__buffer)
        self.__pointer = (self.__pointer + 1) % size

    def reset(self):
        self.__pointer = 0

    def find(self, obj):
        try:
            idx = self.__buffer.index(obj)
        except ValueError:
            return None
        return self.__buffer[idx]

    def find_and_next(self, obj):
        size = len(self.__buffer)
        idx = self.__buffer.index(obj)
        self.__pointer = (idx + 1) % size

    def as_list(self):
        return self.__buffer.copy()


def do_weiler_atherton_cliping(clip, subject, uv_layer):

    # check if clip and subject is overlapped completely
    if is_face_overlapped(clip, subject, uv_layer):
        polygons = [subject]
        muv_common.debug_print("===== Polygons Overlapped Completely =====")
        muv_common.debug_print(polygons)
        return polygons

    # check if clip and subject is overlapped partially
    clip_uvs = RingBuffer([l[uv_layer].uv for l in clip.loops])
    subject_uvs = RingBuffer([l[uv_layer].uv for l in subject.loops])
    intersections = []
    while True:
        subject_uvs.reset()
        while True:
            uv_start1 = clip_uvs.get()
            uv_end1 = clip_uvs.get(1)
            uv_start2 = subject_uvs.get()
            uv_end2 = subject_uvs.get(1)
            intersected, point = check_intersect(uv_start1, uv_end1, uv_start2,
                                                 uv_end2)
            if intersected:
                clip_uvs.insert(point, 1)
                subject_uvs.insert(point, 1)
                intersections.append([point, [clip_uvs.get(), clip_uvs.get(1)]])
            subject_uvs.next()
            if subject_uvs.get() == subject_uvs.head():
                break
        clip_uvs.next()
        if clip_uvs.get() == clip_uvs.head():
            break

    muv_common.debug_print("===== Intersection List =====")
    muv_common.debug_print(intersections)

    def get_intersection_pair(intersections, key):
        for sect in intersections:
            if sect[0] == key:
                return sect[1]

        return None

    # make enter/exit pair
    subject_uvs.reset()
    entering = []
    exiting = []
    intersect_uv_list = []
    while True:
        pair = get_intersection_pair(intersections, subject_uvs.get())
        if pair:
            sub = subject_uvs.get(1) - subject_uvs.get(-1)
            inter = pair[1] - pair[0]
            cross = sub.x * inter.y - inter.x * sub.y
            if cross < 0:
                entering.append(subject_uvs.get())
            else:
                exiting.append(subject_uvs.get())
            intersect_uv_list.append(subject_uvs.get())

        subject_uvs.next()
        if subject_uvs.get() == subject_uvs.head():
            break

    muv_common.debug_print("===== Enter List =====")
    muv_common.debug_print(entering)
    muv_common.debug_print("===== Exit List =====")
    muv_common.debug_print(exiting)


    def Traverse(current_list, intersect_list, intersect_parsed_list, poly,
                 current, start, other_list):
        result = current_list.find(current)
        if not result:
            return None
        if result != current:
            print("Internal Error")
            return None

        # enter
        poly.append(current.copy())
        if intersect_list.count(current) >= 1:
            intersect_parsed_list.append(current)

        current_list.find_and_next(current)
        current = current_list.get()
        if current == start:
            return None

        while intersect_list.count(current) == 0:
            poly.append(current.copy())
            current_list.find_and_next(current)
            current = current_list.get()
            if current == start:
                return None

        # exit
        poly.append(current.copy())
        intersect_parsed_list.append(current)

        other_list.find_and_next(current)
        return other_list.get()

    # Traverse
    polygons = []
    current_uv_list = subject_uvs
    other_uv_list = clip_uvs
    intersect_uv_parsed_list = []
    while len(intersect_uv_parsed_list) != len(intersect_uv_list):
        poly = []
        start_uv = entering[0]
        count = 0
        current_uv = entering[0]

        while current_uv and \
                ((count == 0) or (count > 0 and start_uv != current_uv)):
            current_uv = Traverse(current_uv_list, intersect_uv_list,
                                  intersect_uv_parsed_list, poly,
                                  current_uv, start_uv, other_uv_list)

            if current_uv_list == subject_uvs:
                current_uv_list = clip_uvs
                other_uv_list = subject_uvs
            else:
                current_uv_list = subject_uvs
                other_uv_list = clip_uvs
            count = count + 1

        polygons.append(poly)

    muv_common.debug_print("===== Polygons Overlapped Partially =====")
    muv_common.debug_print(polygons)

    return polygons


class MUV_OVLPUVRenderer(bpy.types.Operator):
    """
    Operation class: Render overlapped UVs
    No operation (only rendering texture)
    """

    bl_idname = "uv.muv_ovlpuv_renderer"
    bl_description = "Render overlapped UVs"
    bl_label = "Overlapped UV renderer"

    __handle = None

    @staticmethod
    def handle_add(obj, context):
        MUV_OVLPUVRenderer.__handle = bpy.types.SpaceImageEditor.draw_handler_add(
            MUV_OVLPUVRenderer.draw, (obj, context), 'WINDOW', 'POST_PIXEL')

    @staticmethod
    def handle_remove():
        if MUV_OVLPUVRenderer.__handle is not None:
            bpy.types.SpaceImageEditor.draw_handler_remove(
                MUV_OVLPUVRenderer.__handle, 'WINDOW')
            MUV_OVLPUVRenderer.__handle = None

    @staticmethod
    def draw(_, context):
        sc = context.scene
        props = sc.muv_props.ovlpuv
        prefs = context.user_preferences.addons["uv_magic_uv"].preferences

        # OpenGL configuration
        bgl.glEnable(bgl.GL_BLEND)

        # render
        color = prefs.ovlpuv_overlapped_color
        for poly in props.overlapped_uvs:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            bgl.glColor4f(color[0], color[1], color[2], color[3])
            for uv in poly:
                x, y = context.region.view2d.view_to_region(uv.x, uv.y)
                bgl.glVertex2f(x, y)
            bgl.glEnd()


class MUV_OVLPUVOps(bpy.types.Operator):
    """
    Operation class: Emphasize Overlapped UV
    """

    bl_idname = "uv.muv_ovlpuv_ops"
    bl_label = "Overlapped UV"
    bl_description = "Overlapped UV launcher"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.ovlpuv
        if not props.running:
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()

            sel_faces = [f for f in bm.faces if f.select]
            overlapped_uvs = []
            for i, f_clip in enumerate(sel_faces):
                for f_subject in sel_faces[i + 1:]:
                    result = do_weiler_atherton_cliping(f_clip, f_subject,
                                                        uv_layer)
                    overlapped_uvs.extend(result)
            props.overlapped_uvs = overlapped_uvs

            MUV_OVLPUVRenderer.handle_add(self, context)
            props.running = True
        else:
            MUV_OVLPUVRenderer.handle_remove()
            props.running = False
        if context.area:
            context.area.tag_redraw()

        return {'FINISHED'}


class MUV_FLPUVRenderer(bpy.types.Operator):
    """
    Operation class: Render flipped UVs
    No operation (only rendering texture)
    """

    bl_idname = "uv.muv_flpuv_renderer"
    bl_description = "Render flipped UVs"
    bl_label = "Flipped UV renderer"

    __handle = None

    @staticmethod
    def handle_add(obj, context):
        MUV_FLPUVRenderer.__handle = bpy.types.SpaceImageEditor.draw_handler_add(
            MUV_FLPUVRenderer.draw, (obj, context), 'WINDOW', 'POST_PIXEL')

    @staticmethod
    def handle_remove():
        if MUV_FLPUVRenderer.__handle is not None:
            bpy.types.SpaceImageEditor.draw_handler_remove(
                MUV_FLPUVRenderer.__handle, 'WINDOW')
            MUV_FLPUVRenderer.__handle = None

    @staticmethod
    def draw(_, context):
        sc = context.scene
        props = sc.muv_props.flpuv
        prefs = context.user_preferences.addons["uv_magic_uv"].preferences

        # OpenGL configuration
        bgl.glEnable(bgl.GL_BLEND)

        # render
        color = prefs.flpuv_flipped_color
        for poly in props.flipped_uvs:
            bgl.glBegin(bgl.GL_TRIANGLE_FAN)
            bgl.glColor4f(color[0], color[1], color[2], color[3])
            for uv in poly:
                x, y = context.region.view2d.view_to_region(uv.x, uv.y)
                bgl.glVertex2f(x, y)
            bgl.glEnd()


class MUV_FLPUVOps(bpy.types.Operator):
    """
    Operation class: Emphasize Fliped UV
    """

    bl_idname = "uv.muv_flpuv_ops"
    bl_label = "Fliped UV"
    bl_description = "Fliped UV launcher"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.flpuv
        if not props.running:
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()

            sel_faces = [f for f in bm.faces if f.select]
            flipped_uvs = []
            for f in sel_faces:
                area = 0.0
                uvs = RingBuffer([l[uv_layer].uv.copy() for l in f.loops])
                for i in range(len(uvs)):
                    uv1 = uvs.get(i)
                    uv2 = uvs.get(i + 1)
                    a = uv1.x * uv2.y - uv1.y * uv2.x
                    area = area + a
                if area < 0:
                    # clock-wise
                    flipped_uvs.append(uvs.as_list())

            props.flipped_uvs = flipped_uvs

            MUV_FLPUVRenderer.handle_add(self, context)
            props.running = True
        else:
            MUV_FLPUVRenderer.handle_remove()
            props.running = False
        if context.area:
            context.area.tag_redraw()

        return {'FINISHED'}
