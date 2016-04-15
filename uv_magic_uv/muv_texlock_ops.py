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
from bpy.props import FloatProperty
from mathutils import Vector, Matrix
from math import sqrt, atan2
from bpy_extras import view3d_utils

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"


def redraw_all_areas():
    for area in bpy.context.screen.areas:
        area.tag_redraw()


def get_space(area_type, region_type, space_type):
    for area in bpy.context.screen.areas:
        if area.type == area_type:
            break
    for region in area.regions:
        if region.type == region_type:
            break
    for space in area.spaces:
        if space.type == space_type:
            break

    return (area, region, space)


# Texture lock
class MUV_TexLockRotation(bpy.types.Operator):
    """Lock texture.(Rotation)"""

    bl_idname = "uv.muv_texlock_rotation"
    bl_label = "Rotation"
    bl_description = "Lock Texture (Rotation)"
    bl_options = {'REGISTER', 'UNDO'}

    ini_mouse_x = 0.0
    ini_mouse_y = 0.0
    first_time = True
    ini_v = []
    ini_uv = []

    def modal(self, context, event):
        props = context.scene.muv_props.texlock
        redraw_all_areas()
        if event.type == 'MOUSEMOVE':
            mx, my = event.mouse_region_x, event.mouse_region_y
            area, region, space = get_space('VIEW_3D', 'WINDOW', 'VIEW_3D')
            obj = context.active_object
            world_mat = obj.matrix_world
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            # get UV layer
            if not bm.loops.layers.uv:
                self.report({'WARNING'}, "Object must have more than one UV map.")
                return {'CANCELLED'}
            uv_layer = bm.loops.layers.uv.verify()

            sel_face = None
            for f in bm.faces:
                if f.select:
                    sel_face = f
                    break
            else:
                return {'FINISHED'}

            if self.first_time is True:
                self.ini_mouse_x = mx
                self.ini_mouse_y = my
                self.ini_v = [l.vert.co.copy() for l in sel_face.loops]
                self.ini_uv = [l[uv_layer].uv.copy() for l in sel_face.loops]
                self.first_time = False

            for l, v, uv in zip(sel_face.loops, self.ini_v, self.ini_uv):
                l.vert.co = v
                l[uv_layer].uv = uv

            # transform 3d space to screen region
            v_ave = Vector((0.0, 0.0, 0.0))
            uv_ave = Vector((0.0, 0.0, 0.0))
            for l in sel_face.loops:
                v_ave = v_ave + l.vert.co
                uv_ave = uv_ave + Vector((l[uv_layer].uv.x, l[uv_layer].uv.y, 0.0))
            v_ave = v_ave / len(sel_face.loops)
            uv_ave = uv_ave / len(sel_face.loops)

            orig_2d = view3d_utils.location_3d_to_region_2d(
                region,
                space.region_3d,
                world_mat * v_ave
                )
            ix = self.ini_mouse_x - orig_2d.x
            iy = self.ini_mouse_y - orig_2d.y
            cx = mx - orig_2d.x
            cy = my - orig_2d.y
            iang = atan2(iy, ix)
            cang = atan2(cy, cx)
            dang = cang - iang
            
            mt = Matrix.Translation(-uv_ave)
            mr = Matrix.Rotation(dang, 4, 'Z')
            mti = mt.inverted()
            mat = mti * mr * mt
            for l in f.loops:
                uv = Vector((l[uv_layer].uv.x, l[uv_layer].uv.y, 0.0))
                uv = mat * uv
                l[uv_layer].uv = Vector((uv.x, uv.y))

            bpy.ops.transform.rotate(axis=f.normal, value=dang) 

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            self.first_time = True
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}



# Texture lock
class MUV_TexLockScale(bpy.types.Operator):
    """Lock texture.(Scale)"""

    bl_idname = "uv.muv_texlock_scale"
    bl_label = "Scale"
    bl_description = "Lock Texture (Scale)"
    bl_options = {'REGISTER', 'UNDO'}

    ini_mouse_x = 0.0
    ini_mouse_y = 0.0
    first_time = True
    ini_v = []
    ini_uv = []

    def modal(self, context, event):
        props = context.scene.muv_props.texlock
        redraw_all_areas()
        if event.type == 'MOUSEMOVE':
            mx, my = event.mouse_region_x, event.mouse_region_y
            area, region, space = get_space('VIEW_3D', 'WINDOW', 'VIEW_3D')
            obj = context.active_object
            world_mat = obj.matrix_world
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            # get UV layer
            if not bm.loops.layers.uv:
                self.report({'WARNING'}, "Object must have more than one UV map.")
                return {'CANCELLED'}
            uv_layer = bm.loops.layers.uv.verify()

            sel_face = None
            for f in bm.faces:
                if f.select:
                    sel_face = f
                    break
            else:
                return {'FINISHED'}

            if self.first_time is True:
                self.ini_mouse_x = mx
                self.ini_mouse_y = my
                self.ini_v = [l.vert.co.copy() for l in sel_face.loops]
                self.ini_uv = [l[uv_layer].uv.copy() for l in sel_face.loops]
                self.first_time = False

            for l, v, uv in zip(sel_face.loops, self.ini_v, self.ini_uv):
                l.vert.co = v
                l[uv_layer].uv = uv

            # transform 3d space to screen region
            v_ave = Vector((0.0, 0.0, 0.0))
            uv_ave = Vector((0.0, 0.0, 0.0))
            for l in sel_face.loops:
                v_ave = v_ave + l.vert.co
                uv_ave = uv_ave + Vector((l[uv_layer].uv.x, l[uv_layer].uv.y, 0.0))
            v_ave = v_ave / len(sel_face.loops)
            uv_ave = uv_ave / len(sel_face.loops)

            orig_2d = view3d_utils.location_3d_to_region_2d(
                region,
                space.region_3d,
                world_mat * v_ave
                )
            ix = self.ini_mouse_x - orig_2d.x
            iy = self.ini_mouse_y - orig_2d.y
            cx = mx - orig_2d.x
            cy = my - orig_2d.y
            il = sqrt(ix * ix + iy * iy)
            cl = sqrt(cx * cx + cy * cy)
            scale = cl / il

            mt = Matrix.Translation(-uv_ave)
            ms = Matrix.Scale(0.1, 4, (1.0, 1.0, 1.0))
            ms.identity()
            ms[0][0] = scale
            ms[1][1] = scale
            mti = mt.inverted()
            mat = mti * ms * mt
            for l in f.loops:
                uv = Vector((l[uv_layer].uv.x, l[uv_layer].uv.y, 0.0))
                uv = mat * uv
                l[uv_layer].uv = Vector((uv.x, uv.y))

            bpy.ops.transform.resize(value=(scale, scale, scale), constraint_orientation='NORMAL')

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            self.first_time = True
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


# Texture lock
class MUV_TexLockTranslation(bpy.types.Operator):
    """Lock texture.(Translation)"""

    bl_idname = "uv.muv_texlock_translation"
    bl_label = "Translation"
    bl_description = "Lock Texture (Translation)"
    bl_options = {'REGISTER', 'UNDO'}

    ini_mouse_x = 0.0
    ini_mouse_y = 0.0
    first_time = True
    ini_v = []
    ini_uv = []

    def modal(self, context, event):
        props = context.scene.muv_props.texlock
        redraw_all_areas()
        if event.type == 'MOUSEMOVE':
            mx, my = event.mouse_region_x, event.mouse_region_y
            area, region, space = get_space('VIEW_3D', 'WINDOW', 'VIEW_3D')
            obj = context.active_object
            world_mat = obj.matrix_world
            bm = bmesh.from_edit_mesh(obj.data)
            if muv_common.check_version(2, 73, 0) >= 0:
                bm.faces.ensure_lookup_table()
            # get UV layer
            if not bm.loops.layers.uv:
                self.report({'WARNING'}, "Object must have more than one UV map.")
                return {'CANCELLED'}
            uv_layer = bm.loops.layers.uv.verify()

            sel_face = None
            for f in bm.faces:
                if f.select:
                    sel_face = f
                    break
            else:
                return {'FINISHED'}

            if self.first_time is True:
                self.ini_mouse_x = mx
                self.ini_mouse_y = my
                self.ini_v = [l.vert.co.copy() for l in sel_face.loops]
                self.ini_uv = [l[uv_layer].uv.copy() for l in sel_face.loops]
                self.first_time = False

            for l, v, uv in zip(sel_face.loops, self.ini_v, self.ini_uv):
                l.vert.co = v
                l[uv_layer].uv = uv

            orig_center = sel_face.center.co
            orig_normal = sel_face.normal.co

            # make ray from mouse 2d
            view_vector = view3d_utils.region_2d_to_vector_3d(region, space.region_3d, Vector((mx, my, 0.0)))
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, space.region_3d, Vector((mx, my, 0.0)))

            # get intersection point on polygon
            #new_center = mathutils.geometry.intersect_line_plane(l1, l2, center, normal)

            # get translation amount
            #diff_center = new_center - orig_center

            # transform UV coordinate
            #mat = Matrix.Translate((diff_2d.x, diff_2d.y, 0.0))_
            #for l in f.loops:
            #    uv = Vector((l[uv_layer].uv.x, l[uv_layer].uv.y, 0.0))
            #    uv = mat * uv
            #    l[uv_layer].uv = Vector((uv.x, uv.y))

            # transform polygon
            #bpy.ops.transform.translate(diff, constraint_orientation='NORMAL')

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            self.first_time = True
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}

