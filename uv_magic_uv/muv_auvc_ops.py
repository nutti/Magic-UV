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


import bpy
from mathutils import Vector

from . import muv_common


class MUV_AUVCUVICOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_c"
    bl_label = "Center"
    bl_description = "Align cursor to the center of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['center'][0] * tex_size[0]
            cy = isl['center'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVILTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_lt"
    bl_label = "Left Top"
    bl_description = "Align cursor to the left top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['min'][0] * tex_size[0]
            cy = isl['max'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVILMOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_lm"
    bl_label = "Left Middle"
    bl_description = "Align cursor to the left middle of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['min'][0] * tex_size[0]
            cy = isl['center'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVILBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_lb"
    bl_label = "Left Bottom"
    bl_description = "Align cursor to the left bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['min'][0] * tex_size[0]
            cy = isl['min'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVIMTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_mt"
    bl_label = "Middle Top"
    bl_description = "Align cursor to the middle top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['center'][0] * tex_size[0]
            cy = isl['max'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVIMBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_mb"
    bl_label = "Middle Bottom"
    bl_description = "Align cursor to the middle bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['center'][0] * tex_size[0]
            cy = isl['min'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVIRTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_rt"
    bl_label = "Right Top"
    bl_description = "Align cursor to the right top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['max'][0] * tex_size[0]
            cy = isl['max'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVIRMOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_rm"
    bl_label = "Right Middle"
    bl_description = "Align cursor to the right middle of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['max'][0] * tex_size[0]
            cy = isl['center'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCUVIRBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_rb"
    bl_label = "Right Bottom"
    bl_description = "Align cursor to the right bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['max'][0] * tex_size[0]
            cy = isl['min'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCCOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_uvi_c"
    bl_label = "Center"
    bl_description = "Align cursor to the center of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        island_info = muv_common.get_island_info(context.active_object)

        for isl in island_info:
            area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                                  'IMAGE_EDITOR')
            tex_size = area.spaces.active.image.size
            cx = isl['center'][0] * tex_size[0]
            cy = isl['center'][1] * tex_size[1]
            space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexLTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_lt"
    bl_label = "Left Top"
    bl_description = "Align cursor to the left top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = 0
        cy = tex_size[1]
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexLMOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_lm"
    bl_label = "Left Middle"
    bl_description = "Align cursor to the left middle of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = 0
        cy = tex_size[1] / 2.0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexLBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_lb"
    bl_label = "Left Bottom"
    bl_description = "Align cursor to the left bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        cx = 0
        cy = 0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexMTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_mt"
    bl_label = "Middle Top"
    bl_description = "Align cursor to the middle top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0] / 2.0
        cy = tex_size[1]
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexCOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_c"
    bl_label = "Center"
    bl_description = "Align cursor to the center of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0] / 2.0
        cy = tex_size[1] / 2.0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexMBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_mb"
    bl_label = "Middle Bottom"
    bl_description = "Align cursor to the middle bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0] / 2.0
        cy = 0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexRTOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_rt"
    bl_label = "Right Top"
    bl_description = "Align cursor to the right top of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0]
        cy = tex_size[1]
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexRMOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_rm"
    bl_label = "Right Middle"
    bl_description = "Align cursor to the right middle of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0]
        cy = tex_size[1] / 2.0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class MUV_AUVCTexRBOps(bpy.types.Operator):

    bl_idname = "uv.muv_auvc_tex_rb"
    bl_label = "Right Bottom"
    bl_description = "Align cursor to the right bottom of UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0]
        cy = 0
        space.cursor_location = Vector((cx, cy))

        return {'FINISHED'}


class IMAGE_PT_MUV_AUVC(bpy.types.Panel):
    """
    Panel class: Align UV Cursor
    """

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Align UV Cursor"
    bl_context = 'mesh_edit'

    @classmethod
    def poll(cls, context):
        prefs = context.user_preferences.addons["uv_magic_uv"].preferences
        return prefs.enable_auvc

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='IMAGE_COL')

    def draw(self, context):
        layout = self.layout
        sc = context.scene

        layout.label("UV Island:")
        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator(MUV_AUVCUVILTOps.bl_idname, text="Left Top")
        row.operator(MUV_AUVCUVIMTOps.bl_idname, text="Middle Top")
        row.operator(MUV_AUVCUVIRTOps.bl_idname, text="Right Top")

        row = col.row(align=True)
        row.operator(MUV_AUVCUVILMOps.bl_idname, text="Left Middle")
        row.operator(MUV_AUVCUVICOps.bl_idname, text="Center")
        row.operator(MUV_AUVCUVIRMOps.bl_idname, text="Right Middle")

        row = col.row(align=True)
        row.operator(MUV_AUVCUVILBOps.bl_idname, text="Left Bottom")
        row.operator(MUV_AUVCUVIMBOps.bl_idname, text="Middle Bottom")
        row.operator(MUV_AUVCUVIRBOps.bl_idname, text="Right Bottom")

        layout.label("Texture:")
        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator(MUV_AUVCTexLTOps.bl_idname, text="Left Top")
        row.operator(MUV_AUVCTexMTOps.bl_idname, text="Middle Top")
        row.operator(MUV_AUVCTexRTOps.bl_idname, text="Right Top")

        row = col.row(align=True)
        row.operator(MUV_AUVCTexLMOps.bl_idname, text="Left Middle")
        row.operator(MUV_AUVCTexCOps.bl_idname, text="Center")
        row.operator(MUV_AUVCTexRMOps.bl_idname, text="Right Middle")

        row = col.row(align=True)
        row.operator(MUV_AUVCTexLBOps.bl_idname, text="Left Bottom")
        row.operator(MUV_AUVCTexMBOps.bl_idname, text="Middle Bottom")
        row.operator(MUV_AUVCTexRBOps.bl_idname, text="Right Bottom")

        layout.label("UV Cursor Location:")
        layout.prop(sc, "muv_auvc_cursor_loc", text="")
