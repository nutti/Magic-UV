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


def redraw_all_areas():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


class MUV_UVBBCmd():
    op = 'NONE'
    def __init__(self):
        self.op = 'NONE'

    def to_matrix(self):
        mat = mathutils.Matrix()
        mat.identity()
        return mat


class MUV_UVBBTranslationCmd(MUV_UVBBCmd):
    __x = 0
    __y = 0
    __ox = 0
    __oy = 0
    def __init__(self, ox, oy):
        self.op = 'TRANSLATION'
        self.__x = ox
        self.__y = oy
        self.__ox = ox
        self.__oy = oy
    def to_matrix(self):
        dx = self.__x - self.__ox
        dy = self.__y - self.__oy
        return mathutils.Matrix.Translation((dx, dy, 0))
    def set(self, x, y):
        self.__x = x
        self.__y = y

class MUV_UVBBRotationCmd(MUV_UVBBCmd):
    __x = 0
    __y = 0
    __ox = 0
    __oy = 0
    __iangle = 0
    def __init__(self, ix, iy, ox, oy):
        self.op = 'ROTATION'
        self.__x = ix
        self.__y = iy
        self.__ox = ox
        self.__oy = oy
        dx = self.__x - self.__ox
        dy = self.__y - self.__oy
        self.__iangle = math.atan2(dy, dx)
    def to_matrix(self):
        dx = self.__x - self.__ox
        dy = self.__y - self.__oy
        angle = math.atan2(dy, dx) - self.__iangle
        mti = mathutils.Matrix.Translation((-self.__ox, -self.__oy, 0.0))
        mr = mathutils.Matrix.Rotation(angle, 4, 'Z')
        mt = mathutils.Matrix.Translation((self.__ox, self.__oy, 0.0))
        return mt * mr * mti
    def set(self, x, y):
        self.__x = x
        self.__y = y

class MUV_UVBBScalingCmd(MUV_UVBBCmd):
    __x = 0
    __y = 0
    __ix = 0
    __iy = 0
    __ox = 0
    __oy = 0
    __iox = 0
    __ioy = 0
    __dir_x = 0
    __dir_y = 0
    __mat = None
    def __init__(self, ix, iy, ox, oy, dir_x, dir_y, mat):
        self.op = 'SCALING'
        self.__ix = ix
        self.__iy = iy
        self.__x = ix
        self.__y = iy
        self.__ox = ox
        self.__oy = oy
        self.__dir_x = dir_x
        self.__dir_y = dir_y
        self.__mat = mat
        iov = mat * mathutils.Vector((ox, oy, 0.0))
        self.__iox = iov.x
        self.__ioy = iov.y
    def to_matrix(self):
        m = self.__mat
        mi = self.__mat.inverted()
        mt0i = mathutils.Matrix.Translation((-self.__iox, -self.__ioy, 0.0))
        mt0 = mathutils.Matrix.Translation((self.__iox, self.__ioy, 0.0))
        t = m * mathutils.Vector((self.__ix, self.__iy, 0.0))
        tix, tiy = t.x, t.y
        t = m * mathutils.Vector((self.__ox, self.__oy, 0.0))
        tox, toy = t.x, t.y
        t = m * mathutils.Vector((self.__x, self.__y, 0.0))
        tx, ty = t.x, t.y
        ms = mathutils.Matrix()
        ms.identity()
        if self.__dir_x == 1:
            ms[0][0] = (tx - tox) * self.__dir_x / (tix - tox)
        if self.__dir_y == 1:
            ms[1][1] = (ty - toy) * self.__dir_y / (tiy - toy)
        return mi * mt0 * ms * mt0i * m
    def set(self, x, y):
        self.__x = x
        self.__y = y


class MUV_UVBBCmdExecuter():
    __cmd_list = []
    __cmd_list_redo = []
    def __init__(self):
        self.__cmd_list = []
        self.__cmd_list_redo = []
    def execute(self, begin=0, end=-1):
        mat = mathutils.Matrix()
        mat.identity()
        for i, cmd in enumerate(self.__cmd_list):
            if begin <= i and (end == -1 or i <= end):
                mat = cmd.to_matrix() * mat
        return mat
    def undo_size(self):
        return len(self.__cmd_list)
    def top(self):
        if len(self.__cmd_list) <= 0:
            return None
        return self.__cmd_list[-1]
    def append(self, cmd):
        self.__cmd_list.append(cmd)
        self.__cmd_list_redo = []
    def undo(self):
        if len(self.__cmd_list) <= 0:
            return
        self.__cmd_list_redo.append(self.__cmd_list.pop())
    def redo(self):
        if len(self.__cmd_list_redo) <= 0:
            return
        self.__cmd_list.append(self.__cmd_list_redo.pop())


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
    __cmd_exec = None

    def __init__(self, cmd_exec):
        self.__cmd_exec = cmd_exec

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
    __cmd_exec = None
    def __init__(self, cmd_exec, mouse_view, ctrl_points):
        self.__cmd_exec = cmd_exec
        ox, oy = ctrl_points[0].x, ctrl_points[0].y
        self.__cmd_exec.append(MUV_UVBBTranslationCmd(ox, oy))

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            x, y = mouse_view.x, mouse_view.y
            self.__cmd_exec.top().set(x, y)
        return MUV_UVBBState.TRANSLATING


class MUV_UVBBStateScaling(MUV_UVBBStateBase):
    __state = None
    __cmd_exec = None

    def __init__(self, cmd_exec, mouse_view, state, ctrl_points):
        self.__state = state
        self.__cmd_exec = cmd_exec
        if state == MUV_UVBBState.SCALING_1:
            ix, iy = ctrl_points[1].x, ctrl_points[1].y
            ox, oy = ctrl_points[8].x, ctrl_points[8].y
            dir_x, dir_y = 1, 1
        elif state == MUV_UVBBState.SCALING_2:
            ix, iy = ctrl_points[2].x, ctrl_points[2].y
            ox, oy = ctrl_points[7].x, ctrl_points[7].y
            dir_x, dir_y = 1, 0
        elif state == MUV_UVBBState.SCALING_3:
            ix, iy = ctrl_points[3].x, ctrl_points[3].y
            ox, oy = ctrl_points[6].x, ctrl_points[6].y
            dir_x, dir_y = 1, 1
        elif state == MUV_UVBBState.SCALING_4:
            ix, iy = ctrl_points[4].x, ctrl_points[4].y
            ox, oy = ctrl_points[5].x, ctrl_points[5].y
            dir_x, dir_y = 0, 1
        elif state == MUV_UVBBState.SCALING_5:
            ix, iy = ctrl_points[5].x, ctrl_points[5].y
            ox, oy = ctrl_points[4].x, ctrl_points[4].y
            dir_x, dir_y = 0, 1
        elif state == MUV_UVBBState.SCALING_6:
            ix, iy = ctrl_points[6].x, ctrl_points[6].y
            ox, oy = ctrl_points[3].x, ctrl_points[3].y
            dir_x, dir_y = 1, 1
        elif state == MUV_UVBBState.SCALING_7:
            ix, iy = ctrl_points[7].x, ctrl_points[7].y
            ox, oy = ctrl_points[2].x, ctrl_points[2].y
            dir_x, dir_y = 1, 0
        elif state == MUV_UVBBState.SCALING_8:
            ix, iy = ctrl_points[8].x, ctrl_points[8].y
            ox, oy = ctrl_points[1].x, ctrl_points[1].y
            dir_x, dir_y = 1, 1
        mat = self.__cmd_exec.execute(end=self.__cmd_exec.undo_size())
        self.__cmd_exec.append(MUV_UVBBScalingCmd(ix, iy, ox, oy, dir_x, dir_y, mat.inverted()))

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            x, y = mouse_view.x, mouse_view.y
            self.__cmd_exec.top().set(x, y)
        return self.__state


class MUV_UVBBStateRotating(MUV_UVBBStateBase):
    __cmd_exec = None
    def __init__(self, cmd_exec, mouse_view, ctrl_points):
        self.__cmd_exec = cmd_exec
        ix, iy = ctrl_points[9].x, ctrl_points[9].y
        ox, oy = ctrl_points[0].x, ctrl_points[0].y
        self.__cmd_exec.append(MUV_UVBBRotationCmd(ix, iy, ox, oy))

    def update(self, context, event, ctrl_points, mouse_view):
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                return MUV_UVBBState.NONE
        if event.type == 'MOUSEMOVE':
            x, y = mouse_view.x, mouse_view.y
            self.__cmd_exec.top().set(x, y)
        return MUV_UVBBState.ROTATING


class MUV_UVBBStateMgr():
    __state = MUV_UVBBState.NONE
    __cmd_exec = None

    def __init__(self, cmd_exec):
        self.__cmd_exec = cmd_exec
        self.__state = MUV_UVBBState.NONE
        self.__state_obj = MUV_UVBBStateNone(self.__cmd_exec)

    def __update_state(self, next_state, mouse_view, ctrl_points):
        if next_state == self.__state:
            return
        if next_state == MUV_UVBBState.TRANSLATING:
            self.__state_obj = MUV_UVBBStateTranslating(self.__cmd_exec, mouse_view, ctrl_points)
        elif next_state == MUV_UVBBState.SCALING_1 or next_state == MUV_UVBBState.SCALING_2 or next_state == MUV_UVBBState.SCALING_3 or next_state == MUV_UVBBState.SCALING_4 or next_state == MUV_UVBBState.SCALING_5 or next_state == MUV_UVBBState.SCALING_6 or next_state == MUV_UVBBState.SCALING_7 or next_state == MUV_UVBBState.SCALING_8:
            self.__state_obj = MUV_UVBBStateScaling(self.__cmd_exec, mouse_view, next_state, ctrl_points)
        elif next_state == MUV_UVBBState.ROTATING:
            self.__state_obj = MUV_UVBBStateRotating(self.__cmd_exec, mouse_view, ctrl_points)
        elif next_state == MUV_UVBBState.NONE:
            self.__state_obj = MUV_UVBBStateNone(self.__cmd_exec)

        self.__state = next_state


    def update(self, context, ctrl_points, event):
        mouse_region = mathutils.Vector((event.mouse_region_x, event.mouse_region_y))
        mouse_view = mathutils.Vector((context.region.view2d.region_to_view(mouse_region.x, mouse_region.y)))
        next_state = self.__state_obj.update(context, event, ctrl_points, mouse_view)
        self.__update_state(next_state, mouse_view, ctrl_points)




class MUV_UVBBUpdater(bpy.types.Operator):
    bl_idname = "uv.muv_uvbb_updater"
    bl_label = "UV Bounding Box Updater"
    bl_description = "Update UV Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    __state_mgr = None
    __cmd_exec = MUV_UVBBCmdExecuter()

    def __init__(self):
        self.__cmd_exec = MUV_UVBBCmdExecuter()
        self.__state_mgr = MUV_UVBBStateMgr(self.__cmd_exec)

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
                for i, l in enumerate(f.loops):
                    uvs.append((f.index, i, l[uv_layer].uv.copy()))
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
            if uv[2].x < left:
                left = uv[2].x
            if uv[2].x > right:
                right = uv[2].x
            if uv[2].y < bottom:
                bottom = uv[2].y
            if uv[2].y > top:
                top = uv[2].y

        points = [
                mathutils.Vector(((left + right) * 0.5, (top + bottom) * 0.5, 0.0)),
                mathutils.Vector((left, top, 0.0)),
                mathutils.Vector((left, (top + bottom) * 0.5, 0.0)),
                mathutils.Vector((left, bottom, 0.0)),
                mathutils.Vector(((left + right) * 0.5, top, 0.0)),
                mathutils.Vector(((left + right) * 0.5, bottom, 0.0)),
                mathutils.Vector((right, top, 0.0)),
                mathutils.Vector((right, (top + bottom) * 0.5, 0.0)),
                mathutils.Vector((right, bottom, 0.0)),
                mathutils.Vector(((left + right) * 0.5, top + 0.03, 0.0))
                ]

        return points

    def __update_uvs(self, context, uvs_ini, trans_mat):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        if not bm.loops.layers.uv:
            return
        uv_layer = bm.loops.layers.uv.verify()
        for uv in uvs_ini:
            v = mathutils.Vector((uv[2].x, uv[2].y, 0.0))
            av = trans_mat * v
            bm.faces[uv[0]].loops[uv[1]][uv_layer].uv = mathutils.Vector((av.x, av.y))


    def __update_ctrl_point(self, context, ctrl_points_ini, trans_mat):
        return [trans_mat * cp for cp in ctrl_points_ini]


    def modal(self, context, event):
        props = context.scene.muv_props.uvbb
        redraw_all_areas()
        if props.running is False:
            return {'FINISHED'}
        if event.type == 'TIMER':
            trans_mat = self.__cmd_exec.execute()
            self.__update_uvs(context, props.uvs_ini, trans_mat)
            props.ctrl_points = self.__update_ctrl_point(context, props.ctrl_points_ini, trans_mat)

        self.__state_mgr.update(context, props.ctrl_points, event)

        return {'PASS_THROUGH'}


    def execute(self, context):
        props = context.scene.muv_props.uvbb
        if props.running == False:
            props.uvs_ini = self.__get_uv_coords(context)
            if props.uvs_ini == None:
                return {'CANCELLED'}
            props.ctrl_points_ini = self.__get_ctrl_point(context, props.uvs_ini)
            trans_mat = self.__cmd_exec.execute()
            self.__update_uvs(context, props.uvs_ini, trans_mat)
            props.ctrl_points = self.__update_ctrl_point(context, props.ctrl_points_ini, trans_mat)
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
