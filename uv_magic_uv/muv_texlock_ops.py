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


def get_dest_uvlist(src_vlists, src_uvlists, dest_vlists):
    dest_uvlists_2d = []
    for svls, suvls, dvls in zip(src_vlists, src_uvlists, dest_vlists):
        src_vlist = svls[1]
        src_uvlist = suvls[1]
        dest_vlist = dvls[1]
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
        r = (src_uvlist_2d[1].x - src_uvlist_2d[0].x) / (src_vlist_2d[1].x - src_vlist_2d[0].x)
        for sv, suv, dv in zip(src_vlist_2d, src_uvlist_2d, dest_vlist_2d):
            u = suv.x + (dv.x - sv.x) * r
            w = suv.y + (dv.y - sv.y) * r
            dest_uvlist_2d.append(Vector((u, w)))

        # reverse transform
        dest_uvlist_2d = [uv_rot_mat.transposed() * duv for duv in dest_uvlist_2d]
        dest_uvlist_2d = [duv + trans_uv for duv in dest_uvlist_2d]

        dest_uvlists_2d.append([svls[0], dest_uvlist_2d])

    return dest_uvlists_2d


class MUV_TexLockTimer(bpy.types.Operator):
    """Texture locking timer."""

    bl_idname = "uv.muv_texlock_timer"
    bl_label = "Texture Lock Timer"
    bl_description = "Texture Lock Timer"

    __timer = None

    @staticmethod
    def handle_add(self, context):
        if MUV_TexLockTimer.__timer is None:
            MUV_TexLockTimer.__timer = context.window_manager.event_timer_add(0.10, context.window)
            context.window_manager.modal_handler_add(self)

    @staticmethod
    def handle_remove(self, context):
        if MUV_TexLockTimer.__timer is not None:
            context.window_manager.event_timer_remove(MUV_TexLockTimer.__timer)
            MUV_TexLockTimer.__timer = None


class MUV_TexLockUpdater(bpy.types.Operator):
    """Texture locking updater."""

    bl_idname = "uv.muv_texlock_updater"
    bl_label = "Texture Lock Updater"
    bl_description = "Texture Lock Updater"

    __timer = None

    def __update_uv(self, context):
        props = context.scene.muv_props.texlock
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
             return
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        dest_vlist = []
        dest_llist = []
        for sv in props.intr_src_vlist:
            f = bm.faces[sv[0]]
            dest_vlist.append([f.index, [l.vert.co.copy() for l in f.loops]])
            dest_llist.append([f.index, [l for l in f.loops]])

        dest_uvlists_2d = get_dest_uvlist(props.intr_src_vlist, props.intr_src_uvlist, dest_vlist)

        # update UV coordinate
        for uvs, ls in zip(dest_uvlists_2d, dest_llist):
            for uv, l in zip(uvs[1], ls[1]):
                l[uv_layer].uv = uv.copy()

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()


    def modal(self, context, event):
        props = context.scene.muv_props.texlock
        if context.area:
            context.area.tag_redraw()
        if props.intr_running is False:
            return {'FINISHED'}
        if event.type == 'TIMER':
            self.__update_uv(context)

        return {'PASS_THROUGH'}

    def handle_add(self, context):
        if self.__timer is None:
            self.__timer = context.window_manager.event_timer_add(0.10, context.window)
            context.window_manager.modal_handler_add(self)

    def handle_remove(self, context):
        if self.__timer is not None:
            context.window_manager.event_timer_remove(self.__timer)
            self.__timer = None

    def execute(self, context):
        props = context.scene.muv_props.texlock
        if props.intr_running == False:
            self.handle_add(context)
            props.intr_running = True
            return {'RUNNING_MODAL'}
        else:
            self.handle_remove(context)
            props.intr_running = False
        if context.area:
            context.area.tag_redraw()

        return {'FINISHED'}


# Texture lock (Start, Interactive mode)
class MUV_TexLockIntrStart(bpy.types.Operator):
    """Start texture locking. (Interactive mode)"""

    bl_idname = "uv.muv_texlock_intr_start"
    bl_label = "Texture Lock Start (Interactive mode)"
    bl_description = "Texture Lock Start (Realtime UV update)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texlock
        if props.intr_running is True:
            return {'CANCELLED'}
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        props.intr_src_vlist = []
        props.intr_src_uvlist = []
        for f in bm.faces:
            if f.select:
                props.intr_src_vlist.append([f.index, [l.vert.co.copy() for l in f.loops]])
                props.intr_src_uvlist.append([f.index, [l[uv_layer].uv.copy() for l in f.loops]])
        if len(props.intr_src_vlist) < 1:
            self.report({'WARNING'}, "No faces are selected.")
            return {'CANCELLED'}

        bpy.ops.uv.muv_texlock_updater()

        return {'FINISHED'}

# Texture lock (Stop, Interactive mode)
class MUV_TexLockIntrStop(bpy.types.Operator):
    """Stop texture locking. (interactive mode)"""

    bl_idname = "uv.muv_texlock_intr_stop"
    bl_label = "Texture Lock Stop (Interactive mode)"
    bl_description = "Texture Lock Stop (Realtime UV update)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
       props = context.scene.muv_props.texlock
       if props.intr_running is False:
           return {'CANCELLED'}

       bpy.ops.uv.muv_texlock_updater()

       return {'FINISHED'}


# Texture lock (Start)
class MUV_TexLockStart(bpy.types.Operator):
    """Start texture locking."""

    bl_idname = "uv.muv_texlock_start"
    bl_label = "Texture Lock Start"
    bl_description = "Texture Lock Start"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texlock
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        props.src_vlist = []
        props.src_uvlist = []
        for f in bm.faces:
            if f.select:
                props.src_vlist.append([f.index, [l.vert.co.copy() for l in f.loops]])
                props.src_uvlist.append([f.index, [l[uv_layer].uv.copy() for l in f.loops]])
        if len(props.src_vlist) <= 0:
            self.report({'WARNING'}, "No faces are selected.")
            return {'CANCELLED'}

        return {'FINISHED'}


# Texture lock (Stop)
class MUV_TexLockStop(bpy.types.Operator):
    """Stop texture locking."""

    bl_idname = "uv.muv_texlock_stop"
    bl_label = "Texture Lock Stop"
    bl_description = "Texture Lock Stop"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.muv_props.texlock
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        # get UV layer
        if not bm.loops.layers.uv:
            self.report({'WARNING'}, "Object must have more than one UV map.")
            return {'CANCELLED'}
        uv_layer = bm.loops.layers.uv.verify()

        # get vertex/UV list
        dest_vlist = []
        dest_llist = []
        for sv in props.src_vlist:
            f = bm.faces[sv[0]]
            dest_vlist.append([f.index, [l.vert.co.copy() for l in f.loops]])
            dest_llist.append([f.index, [l for l in f.loops]])

        dest_uvlists_2d = get_dest_uvlist(props.src_vlist, props.src_uvlist, dest_vlist)

        # update UV coordinate
        for uvs, ls in zip(dest_uvlists_2d, dest_llist):
            for uv, l in zip(uvs[1], ls[1]):
                l[uv_layer].uv = uv.copy()

        bmesh.update_edit_mesh(obj.data)
        redraw_all_areas()

        return {'FINISHED'}
