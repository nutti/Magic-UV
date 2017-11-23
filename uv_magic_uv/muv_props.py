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
from bpy.props import (
    FloatProperty,
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
)
from mathutils import Vector


DEBUG = False


def get_loaded_texture_name(_, __):
    items = [(key, key, "") for key in bpy.data.images.keys()]
    items.append(("None", "None", ""))
    return items


# Properties used in this add-on.
class MUV_Properties():
    cpuv = None
    cpuv_obj = None
    cpuv_selseq = None
    transuv = None
    uvbb = None
    texproj = None
    texlock = None
    texwrap = None
    wsuv = None

    def __init__(self):
        self.cpuv = MUV_CPUVProps()
        self.cpuv_obj = MUV_CPUVProps()
        self.cpuv_selseq = MUV_CPUVSelSeqProps()
        self.transuv = MUV_TransUVProps()
        self.uvbb = MUV_UVBBProps()
        self.texproj = MUV_TexProjProps()
        self.texlock = MUV_TexLockProps()
        self.texwrap = MUV_TexWrapProps()
        self.wsuv = MUV_WSUVProps()


class MUV_CPUVProps():
    src_uvs = []
    src_pin_uvs = []
    src_seams = []


class MUV_CPUVSelSeqProps():
    src_uvs = []
    src_pin_uvs = []
    src_seams = []


class MUV_TransUVProps():
    topology_copied = []


class MUV_UVBBProps():
    uv_info_ini = []
    ctrl_points_ini = []
    ctrl_points = []
    running = False


class MUV_TexProjProps():
    running = False


class MUV_TexLockProps():
    verts_orig = None
    intr_verts_orig = None
    intr_running = False


class MUV_TexWrapProps():
    src_face_index = -1


class MUV_WSUVProps():
    ref_sv = None
    ref_suv = None


def init_props(scene):
    scene.muv_props = MUV_Properties()
    scene.muv_uvbb_uniform_scaling = BoolProperty(
        name="Uniform Scaling",
        description="Enable Uniform Scaling",
        default=False)
    scene.muv_texproj_tex_magnitude = FloatProperty(
        name="Magnitude",
        description="Texture Magnitude",
        default=0.5,
        min=0.0,
        max=100.0)
    scene.muv_texproj_tex_image = EnumProperty(
        name="Image",
        description="Texture Image",
        items=get_loaded_texture_name)
    scene.muv_texproj_tex_transparency = FloatProperty(
        name="Transparency",
        description="Texture Transparency",
        default=0.2,
        min=0.0,
        max=1.0)
    scene.muv_texproj_adjust_window = BoolProperty(
        name="Adjust Window",
        description="Size of renderered texture is fitted to window",
        default=True)
    scene.muv_texproj_apply_tex_aspect = BoolProperty(
        name="Texture Aspect Ratio",
        description="Apply Texture Aspect ratio to displayed texture",
        default=True)

    def auvc_get_cursor_loc(self):
        from . import muv_common
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        loc = space.cursor_location
        cx = loc[0] / tex_size[0]
        cy = loc[1] / tex_size[1]
        self['muv_auvc_cursor_loc'] = Vector((cx, cy))
        return self.get('muv_auvc_cursor_loc', (0.0, 0.0))

    def auvc_set_cursor_loc(self, value):
        from . import muv_common
        self['muv_auvc_cursor_loc'] = value
        area, _, space = muv_common.get_space('IMAGE_EDITOR', 'WINDOW',
                                              'IMAGE_EDITOR')
        tex_size = area.spaces.active.image.size
        cx = tex_size[0] * value[0]
        cy = tex_size[1] * value[1]
        space.cursor_location = Vector((cx, cy))

    scene.muv_auvc_cursor_loc = FloatVectorProperty(
        name="UV Cursor Location",
        size=2,
        precision=4,
        soft_min=-1.0,
        soft_max=1.0,
        step=1,
        default=(0.000, 0.000),
        get=auvc_get_cursor_loc,
        set=auvc_set_cursor_loc)


def clear_props(scene):
    del scene.muv_props
    del scene.muv_uvbb_uniform_scaling
    del scene.muv_texproj_tex_magnitude
    del scene.muv_texproj_tex_image
    del scene.muv_texproj_tex_transparency
    del scene.muv_texproj_adjust_window
    del scene.muv_texproj_apply_tex_aspect
    del scene.muv_auvc_cursor_loc
