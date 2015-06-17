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
import bgl
import mathutils
import bmesh
import copy
from enum import Enum
import math

from . import muv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"


# UV Bounding box renderer
class MUV_UVBBRenderer(bpy.types.Operator):
    """."""

    bl_idname = "uv.muv_uvbb_renderer"
    bl_label = "UV Bounding Box Renderer"
    bl_description = "Bounding Box Renderer about UV in Image Editor"
    
    __handle = None
    __timer = None
    __ctrl_points = []

    @staticmethod
    def handle_add(self, context):
        if MUV_UVBBRenderer.__handle is None:
            MUV_UVBBRenderer.__handle = bpy.types.SpaceImageEditor.draw_handler_add(
                MUV_UVBBRenderer.draw_bb,
                (self, context), "WINDOW", "POST_PIXEL")
        if MUV_UVBBRenderer.__timer is None:
            MUV_UVBBRenderer.__timer = context.window_manager.event_timer_add(0.10, context.window)
            context.window_manager.modal_handler_add(self)

    @staticmethod
    def handle_remove(self, context):
        if MUV_UVBBRenderer.__handle is not None:
            bpy.types.SpaceImageEditor.draw_handler_remove(
                MUV_UVBBRenderer.__handle, "WINDOW")
            MUV_UVBBRenderer.__handle = None
        if MUV_UVBBRenderer.__timer is not None:
            context.window_manager.event_timer_remove(MUV_UVBBRenderer.__timer)
            MUV_UVBBRenderer.__timer = None

    @staticmethod
    def __draw_ctrl_point(self, context, pos):
        cp_size = context.scene.muv_uvbb_cp_size
        offset = cp_size / 2
        verts = [
            [pos.x - offset, pos.y - offset],
            [pos.x - offset, pos.y + offset],
            [pos.x + offset, pos.y + offset],
            [pos.x + offset, pos.y - offset]
            ]
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        for (x, y) in verts:
            bgl.glVertex2f(x, y)
        bgl.glEnd()

    @staticmethod
    def draw_bb(self, context):
        props = context.scene.muv_props.uvbb
        for i, cp in enumerate(props.ctrl_points):
            MUV_UVBBRenderer.__draw_ctrl_point(self, context, mathutils.Vector(context.region.view2d.view_to_region(cp.x, cp.y)))


class MUV_UVBBState(Enum):
    NONE = 0
    TRANSLATING = 1
    SCALING_1 = 2
    SCALING_2 = 3
    SCALING_3 = 4
    SCALING_4 = 5
    SCALING_5 = 6
    SCALING_6 = 7
    SCALING_7 = 8
    SCALING_8 = 9
    ROTATING = 10


class MUV_UVBBStateBase():
    def __init__(self):
        raise NotImplementedError
    def update(self, context, event, ctrl_points, mouse_view):
        raise NotImplementedError


def get_region(context, area, region):
   for area in context.screen.areas:
       if area.type == 'IMAGE_EDITOR':
           break
   else:
       return None 
   for region in area.regions:
       if region.type == 'WINDOW':
           break
   else:
       return None

   return region


class MUV_UVBBStateNone(MUV_UVBBStateBase):
    def __init__(self):
        pass

    def update(self, context, event, ctrl_points, mouse_view):
        cp_react_size = context.scene.muv_uvbb_cp_react_size
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                x, y = context.region.view2d.view_to_region(mouse_view.x, mouse_view.y)
                for i, p in enumerate(ctrl_points):
                    px, py = context.region.view2d.view_to_region(p.x, p.y)
                    if px + cp_react_size > x and px - cp_react_size < x and py + cp_react_size > y and py - cp_react_size < y:
                        if i == 0:
                            return MUV_UVBBState.TRANSLATING
                        elif i == 1:
                            return MUV_UVBBState.SCALING_1
                        elif i == 2:
                            return MUV_UVBBState.SCALING_2
                        elif i == 3:
                            return MUV_UVBBState.SCALING_3
                        elif i == 4:
                            return MUV_UVBBState.SCALING_4
                        elif i == 5:
                            return MUV_UVBBState.SCALING_5
                        elif i == 6:
                            return MUV_UVBBState.SCALING_6
                        elif i == 7:
                            return MUV_UVBBState.SCALING_7
                        elif i == 8:
                            return MUV_UVBBState.SCALING_8
                        elif i == 9:
                            return MUV_UVBBState.ROTATING

        return MUV_UVBBState.NONE
 

class MUV_UVBBStateTranslating(MUV_UVBBStateBase):
    __prev_mouse_view = mathutils.Vector((0.0, 0.0))
    def __init__(self, mouse_view):
        self.__prev_mouse_view = mouse_view.copy()

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            if not bm.loops.layers.uv:
                return MUV_UVBBState.NONE
            uv_layer = bm.loops.layers.uv.verify()
            x, y = mouse_view.x, mouse_view.y
            px, py = self.__prev_mouse_view.x, self.__prev_mouse_view.y
            dx, dy = x - px, y - py
            for f in bm.faces:
                if f.select:
                    for l in f.loops:
                        l[uv_layer].uv.x = l[uv_layer].uv.x + dx
                        l[uv_layer].uv.y = l[uv_layer].uv.y + dy
            self.__prev_mouse_view = mathutils.Vector((x, y))
        return MUV_UVBBState.TRANSLATING


class MUV_UVBBStateScaling(MUV_UVBBStateBase):
    __prev_mouse_view = mathutils.Vector((0.0, 0.0))
    __state = None

    def __init__(self, mouse_view, state):
        self.__prev_mouse_view = mouse_view.copy()
        self.__state = state

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            if not bm.loops.layers.uv:
                return MUV_UVBBState.NONE
            uv_layer = bm.loops.layers.uv.verify()
            x, y = mouse_view.x, mouse_view.y
            px, py = self.__prev_mouse_view.x, self.__prev_mouse_view.y
            dx, dy = x - px, y - py
            if self.__state == MUV_UVBBState.SCALING_1:
                ox, oy = ctrl_points[8].x, ctrl_points[8].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 - dx)
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 + dy) 
            elif self.__state == MUV_UVBBState.SCALING_2:
                ox, oy = ctrl_points[7].x, ctrl_points[7].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 - dx)
            elif self.__state == MUV_UVBBState.SCALING_3:
                ox, oy = ctrl_points[6].x, ctrl_points[6].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 - dx)
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 - dy) 
            elif self.__state == MUV_UVBBState.SCALING_4:
                ox, oy = ctrl_points[5].x, ctrl_points[5].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 + dy) 
            elif self.__state == MUV_UVBBState.SCALING_5:
                ox, oy = ctrl_points[4].x, ctrl_points[4].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 - dy) 
            elif self.__state == MUV_UVBBState.SCALING_6:
                ox, oy = ctrl_points[3].x, ctrl_points[3].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 + dx)
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 + dy) 
            elif self.__state == MUV_UVBBState.SCALING_7:
                ox, oy = ctrl_points[2].x, ctrl_points[2].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 + dx)
            elif self.__state == MUV_UVBBState.SCALING_8:
                ox, oy = ctrl_points[1].x, ctrl_points[1].y
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            l[uv_layer].uv.x = ox + (l[uv_layer].uv.x - ox) * (1 + dx)
                            l[uv_layer].uv.y = oy + (l[uv_layer].uv.y - oy) * (1 - dy) 
            self.__prev_mouse_view = mathutils.Vector((x, y))
        return self.__state 
 

class MUV_UVBBStateRotating(MUV_UVBBStateBase):
    __prev_mouse_view = mathutils.Vector((0.0, 0.0))
    def __init__(self, mouse_view):
        self.__prev_mouse_view = mouse_view.copy()

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            if not bm.loops.layers.uv:
                return MUV_UVBBState.NONE
            uv_layer = bm.loops.layers.uv.verify()
            x, y = mouse_view.x, mouse_view.y
            px, py = self.__prev_mouse_view.x, self.__prev_mouse_view.y
            ox, oy = ctrl_points[0].x, ctrl_points[0].y
            ang = math.atan2(y - oy, x - ox)
            pang = math.atan2(py - oy, px - ox)
            diff = ang - pang
            for f in bm.faces:
                if f.select:
                    for l in f.loops:
                        dx = l[uv_layer].uv.x - ox
                        dy = l[uv_layer].uv.y - oy
                        r = math.sqrt(dx * dx + dy * dy)
                        oang = math.atan2(dy, dx)
                        l[uv_layer].uv.x = ox + r * math.cos(diff + oang)
                        l[uv_layer].uv.y = oy + r * math.sin(diff + oang)
            self.__prev_mouse_view = mathutils.Vector((x, y))
        return MUV_UVBBState.ROTATING



class MUV_UVBBStateMgr():
    __state = MUV_UVBBState.NONE
    __state_obj = MUV_UVBBStateNone()

    def __init__(self):
        self.__state = MUV_UVBBState.NONE
        self.__state_obj = MUV_UVBBStateNone()

    def __update_state(self, next_state, mouse_view):
        if next_state == self.__state:
            return
        if next_state == MUV_UVBBState.TRANSLATING:
            self.__state_obj = MUV_UVBBStateTranslating(mouse_view)
        elif next_state == MUV_UVBBState.SCALING_1 or next_state == MUV_UVBBState.SCALING_2 or next_state == MUV_UVBBState.SCALING_3 or next_state == MUV_UVBBState.SCALING_4 or next_state == MUV_UVBBState.SCALING_5 or next_state == MUV_UVBBState.SCALING_6 or next_state == MUV_UVBBState.SCALING_7 or next_state == MUV_UVBBState.SCALING_8:
            self.__state_obj = MUV_UVBBStateScaling(mouse_view, next_state)
        elif next_state == MUV_UVBBState.ROTATING:
            self.__state_obj = MUV_UVBBStateRotating(mouse_view)
        elif next_state == MUV_UVBBState.NONE:
            self.__state_obj = MUV_UVBBStateNone()

        self.__state = next_state


    def update(self, context, ctrl_points, event):
        mouse_region = mathutils.Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_view = mathutils.Vector((context.region.view2d.region_to_view(mouse_region.x, mouse_region.y)))
        next_state = self.__state_obj.update(context, event, ctrl_points, mouse_view)
        self.__update_state(next_state, mouse_view)





class MUV_UVBBUpdater(bpy.types.Operator):
    bl_idname = "uv.muv_uvbb_updater"
    bl_label = "UV Bounding Box Updater"
    bl_description = "Update UV Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    __state_mgr = None

    def __init__(self):
        self.__state_mgr = MUV_UVBBStateMgr()

    def __get_uv_coords(self, context):
        obj = context.active_object
        uvs = []
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        if not bm.loops.layers.uv:
            return None
        uv_layer = bm.loops.layers.uv.verify()
        for f in bm.faces:
            if f.select:
                for l in f.loops:
                    uvs.append(l[uv_layer].uv.copy())
        if len(uvs) == 0:
            return None
        return uvs

    def __get_ctrl_point(self, context, uvs):
        MAX_VALUE = 100000.0
        left = MAX_VALUE
        right = -MAX_VALUE
        top = -MAX_VALUE
        bottom = MAX_VALUE

        for uv in uvs:
            if uv.x < left:
                left = uv.x
            if uv.x > right:
                right = uv.x
            if uv.y < bottom:
                bottom = uv.y
            if uv.y > top:
                top = uv.y

        points = [
                mathutils.Vector(((left + right) * 0.5, (top + bottom) * 0.5)),
                mathutils.Vector((left, top)),
                mathutils.Vector((left, (top + bottom) * 0.5)),
                mathutils.Vector((left, bottom)),
                mathutils.Vector(((left + right) * 0.5, top)),
                mathutils.Vector(((left + right) * 0.5, bottom)),
                mathutils.Vector((right, top)),
                mathutils.Vector((right, (top + bottom) * 0.5)),
                mathutils.Vector((right, bottom)),
                mathutils.Vector(((left + right) * 0.5, top + 0.1))
                ]

        return points


    def modal(self, context, event):
        props = context.scene.muv_props.uvbb
        if context.area:
            context.area.tag_redraw()
        if props.running is False:
            return {'FINISHED'}
        if event.type == 'TIMER':
            uvs = self.__get_uv_coords(context)
            if uvs == None:
                return {'PASS_THROUGH'}
            props.ctrl_points = self.__get_ctrl_point(context, uvs)

        self.__state_mgr.update(context, props.ctrl_points, event)

        return {'PASS_THROUGH'}


    def execute(self, context):
        props = context.scene.muv_props.uvbb
        if props.running == False:
            MUV_UVBBRenderer.handle_add(self, context)
            props.running = True
        else:
            MUV_UVBBRenderer.handle_remove(self, context)
            props.running = False
        if context.area:
            context.area.tag_redraw()

        return {'FINISHED'}


# UI view
class IMAGE_PT_MUV_UVBB(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_label = 'UV Bounding Box'

    def draw(self, context):
        prefs = context.user_preferences.addons["uv_magic_uv"].preferences
        if prefs.enable_uvbb is False:
            return
        sc = context.scene
        props = sc.muv_props.uvbb
        layout = self.layout
        layout.label(text="", icon='PLUGIN')
        if props.running == False:
            layout.operator(MUV_UVBBUpdater.bl_idname, text="Display UV Bounding Box", icon='PLAY')
        else:
            layout.operator(MUV_UVBBUpdater.bl_idname, text="Hide UV Bounding Box", icon='PAUSE')
            layout.label(text="Control Point")
            layout.prop(sc, "muv_uvbb_cp_size", text="Size")
            layout.prop(sc, "muv_uvbb_cp_react_size", text="React Size")

