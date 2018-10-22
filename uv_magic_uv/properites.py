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
__version__ = "5.1"
__date__ = "24 Feb 2018"

import bpy
from bpy.props import (
    FloatProperty,
    EnumProperty,
    BoolProperty,
    FloatVectorProperty,
    IntVectorProperty,
)
from mathutils import Vector

from . import common

from .op import (
    copy_paste_uv,
    copy_paste_uv_object,
    copy_paste_uv_uvedit,
    uv_bounding_box,
    uv_inspection,
    uv_sculpt,
    texture_lock,
    texture_projection,
    world_scale_uv,
)


__all__ = [
    'get_loaded_texture_name',
    'MUV_Properties',
    'init_props',
    'clear_props',
]


def get_loaded_texture_name(_, __):
    items = [(key, key, "") for key in bpy.data.images.keys()]
    items.append(("None", "None", ""))
    return items


# Properties used in this add-on.
class MUV_Properties():

    def __init__(self):
        self.prefs = MUV_Prefs()
        self.transuv = MUV_TransUVProps()
        self.uvbb = MUV_UVBBProps()
        self.texlock = MUV_TexLockProps()
        self.texwrap = MUV_TexWrapProps()
        self.uvinsp = MUV_UVInspProps()


class MUV_Prefs():
    expanded = {
        "info_desc": False,
        "info_loc": False,
        "conf_uvsculpt": False,
        "conf_uvinsp": False,
        "conf_texproj": False,
        "conf_uvbb": False
    }


class MUV_TransUVProps():
    topology_copied = None


class MUV_UVBBProps():
    uv_info_ini = []
    ctrl_points_ini = []
    ctrl_points = []


class MUV_TexLockProps():
    verts_orig = None


class MUV_TexWrapProps():
    ref_face_index = -1
    ref_obj = None


class MUV_UVInspProps():
    overlapped_info = []
    flipped_info = []


def init_props(scene):
    scene.muv_props = MUV_Properties()

    # Texture Wrap
    scene.muv_texwrap_enabled = BoolProperty(
        name="Texture Wrap",
        description="Texture Wrap is enabled",
        default=False
    )
    scene.muv_texwrap_set_and_refer = BoolProperty(
        name="Set and Refer",
        description="Refer and set UV",
        default=True
    )
    scene.muv_texwrap_selseq = BoolProperty(
        name="Selection Sequence",
        description="Set UV sequentially",
        default=False
    )

    # Select UV
    scene.muv_seluv_enabled = BoolProperty(
        name="Select UV Enabled",
        description="Select UV is enabled",
        default=False
    )

    # Align UV
    scene.muv_auv_enabled = BoolProperty(
        name="Aline UV Enabled",
        description="Align UV is enabled",
        default=False
    )
    scene.muv_auv_transmission = BoolProperty(
        name="Transmission",
        description="Align linked UVs",
        default=False
    )
    scene.muv_auv_select = BoolProperty(
        name="Select",
        description="Select UVs which are aligned",
        default=False
    )
    scene.muv_auv_vertical = BoolProperty(
        name="Vert-Infl (Vertical)",
        description="Align vertical direction influenced "
                    "by mesh vertex proportion",
        default=False
    )
    scene.muv_auv_horizontal = BoolProperty(
        name="Vert-Infl (Horizontal)",
        description="Align horizontal direction influenced "
                    "by mesh vertex proportion",
        default=False
    )
    scene.muv_auv_mesh_infl = FloatProperty(
        name="Mesh Influence",
        description="Influence rate of mesh vertex",
        min=0.0,
        max=1.0,
        default=0.0
    )
    scene.muv_auv_location = EnumProperty(
        name="Location",
        description="Align location",
        items=[
            ('LEFT_TOP', "Left/Top", "Align to Left or Top"),
            ('MIDDLE', "Middle", "Align to middle"),
            ('RIGHT_BOTTOM', "Right/Bottom", "Align to Right or Bottom")
        ],
        default='MIDDLE'
    )

    # Smooth UV
    scene.muv_smuv_enabled = BoolProperty(
        name="Smooth UV Enabled",
        description="Smooth UV is enabled",
        default=False
    )
    scene.muv_smuv_transmission = BoolProperty(
        name="Transmission",
        description="Smooth linked UVs",
        default=False
    )
    scene.muv_smuv_mesh_infl = FloatProperty(
        name="Mesh Influence",
        description="Influence rate of mesh vertex",
        min=0.0,
        max=1.0,
        default=0.0
    )
    scene.muv_smuv_select = BoolProperty(
        name="Select",
        description="Select UVs which are smoothed",
        default=False
    )



    # Pack UV
    scene.muv_packuv_enabled = BoolProperty(
        name="Pack UV Enabled",
        description="Pack UV is enabled",
        default=False
    )
    scene.muv_packuv_allowable_center_deviation = FloatVectorProperty(
        name="Allowable Center Deviation",
        description="Allowable center deviation to judge same UV island",
        min=0.000001,
        max=0.1,
        default=(0.001, 0.001),
        size=2
    )
    scene.muv_packuv_allowable_size_deviation = FloatVectorProperty(
        name="Allowable Size Deviation",
        description="Allowable sizse deviation to judge same UV island",
        min=0.000001,
        max=0.1,
        default=(0.001, 0.001),
        size=2
    )

    # Move UV
    scene.muv_mvuv_enabled = BoolProperty(
        name="Move UV Enabled",
        description="Move UV is enabled",
        default=False
    )

    # UVW
    scene.muv_uvw_enabled = BoolProperty(
        name="UVW Enabled",
        description="UVW is enabled",
        default=False
    )
    scene.muv_uvw_assign_uvmap = BoolProperty(
        name="Assign UVMap",
        description="Assign UVMap when no UVmaps are available",
        default=True
    )

    # Unwrap Constraint
    scene.muv_unwrapconst_enabled = BoolProperty(
        name="Unwrap Constraint Enabled",
        description="Unwrap Constraint is enabled",
        default=False
    )
    scene.muv_unwrapconst_u_const = BoolProperty(
        name="U-Constraint",
        description="Keep UV U-axis coordinate",
        default=False
    )
    scene.muv_unwrapconst_v_const = BoolProperty(
        name="V-Constraint",
        description="Keep UV V-axis coordinate",
        default=False
    )

    # Preserve UV Aspect
    scene.muv_preserve_uv_enabled = BoolProperty(
        name="Preserve UV Aspect Enabled",
        description="Preserve UV Aspect is enabled",
        default=False
    )
    scene.muv_preserve_uv_tex_image = EnumProperty(
        name="Image",
        description="Texture Image",
        items=get_loaded_texture_name
    )
    scene.muv_preserve_uv_origin = EnumProperty(
        name="Origin",
        description="Aspect Origin",
        items=[
            ('CENTER', 'Center', 'Center'),
            ('LEFT_TOP', 'Left Top', 'Left Bottom'),
            ('LEFT_CENTER', 'Left Center', 'Left Center'),
            ('LEFT_BOTTOM', 'Left Bottom', 'Left Bottom'),
            ('CENTER_TOP', 'Center Top', 'Center Top'),
            ('CENTER_BOTTOM', 'Center Bottom', 'Center Bottom'),
            ('RIGHT_TOP', 'Right Top', 'Right Top'),
            ('RIGHT_CENTER', 'Right Center', 'Right Center'),
            ('RIGHT_BOTTOM', 'Right Bottom', 'Right Bottom')

        ],
        default="CENTER"
    )

    # Flip/Rotate UV
    scene.muv_fliprot_enabled = BoolProperty(
        name="Flip/Rotate UV Enabled",
        description="Flip/Rotate UV is enabled",
        default=False
    )
    scene.muv_fliprot_seams = BoolProperty(
        name="Seams",
        description="Seams",
        default=True
    )

    # Mirror UV
    scene.muv_mirroruv_enabled = BoolProperty(
        name="Mirror UV Enabled",
        description="Mirror UV is enabled",
        default=False
    )
    scene.muv_mirroruv_axis = EnumProperty(
        items=[
            ('X', "X", "Mirror Along X axis"),
            ('Y', "Y", "Mirror Along Y axis"),
            ('Z', "Z", "Mirror Along Z axis")
        ],
        name="Axis",
        description="Mirror Axis",
        default='X'
    )

    # Transfer UV
    scene.muv_transuv_enabled = BoolProperty(
        name="Transfer UV Enabled",
        description="Transfer UV is enabled",
        default=False
    )
    scene.muv_transuv_invert_normals = BoolProperty(
        name="Invert Normals",
        description="Invert Normals",
        default=False
    )
    scene.muv_transuv_copy_seams = BoolProperty(
        name="Copy Seams",
        description="Copy Seams",
        default=True
    )

    # Align UV Cursor
    def auvc_get_cursor_loc(self):
        area, _, space = common.get_space('IMAGE_EDITOR', 'WINDOW',
                                          'IMAGE_EDITOR')
        bd_size = common.get_uvimg_editor_board_size(area)
        loc = space.cursor_location
        if bd_size[0] < 0.000001:
            cx = 0.0
        else:
            cx = loc[0] / bd_size[0]
        if bd_size[1] < 0.000001:
            cy = 0.0
        else:
            cy = loc[1] / bd_size[1]
        self['muv_auvc_cursor_loc'] = Vector((cx, cy))
        return self.get('muv_auvc_cursor_loc', (0.0, 0.0))

    def auvc_set_cursor_loc(self, value):
        self['muv_auvc_cursor_loc'] = value
        area, _, space = common.get_space('IMAGE_EDITOR', 'WINDOW',
                                          'IMAGE_EDITOR')
        bd_size = common.get_uvimg_editor_board_size(area)
        cx = bd_size[0] * value[0]
        cy = bd_size[1] * value[1]
        space.cursor_location = Vector((cx, cy))

    scene.muv_auvc_enabled = BoolProperty(
        name="Align UV Cursor Enabled",
        description="Align UV Cursor is enabled",
        default=False
    )
    scene.muv_auvc_cursor_loc = FloatVectorProperty(
        name="UV Cursor Location",
        size=2,
        precision=4,
        soft_min=-1.0,
        soft_max=1.0,
        step=1,
        default=(0.000, 0.000),
        get=auvc_get_cursor_loc,
        set=auvc_set_cursor_loc
    )
    scene.muv_auvc_align_menu = EnumProperty(
        name="Align Method",
        description="Align Method",
        default='TEXTURE',
        items=[
            ('TEXTURE', "Texture", "Align to texture"),
            ('UV', "UV", "Align to UV"),
            ('UV_SEL', "UV (Selected)", "Align to Selected UV")
        ]
    )

    # UV Cursor Location
    scene.muv_uvcloc_enabled = BoolProperty(
        name="UV Cursor Location Enabled",
        description="UV Cursor Location is enabled",
        default=False
    )

    copy_paste_uv.MUV_CPUV.init_props(scene)
    copy_paste_uv_object.MUV_CPUVObj.init_props(scene)
    copy_paste_uv_uvedit.MUV_CPUVIE.init_props(scene)
    uv_bounding_box.MUV_UVBB.init_props(scene)
    uv_inspection.MUV_UVInsp.init_props(scene)
    uv_sculpt.MUV_UVSculpt.init_props(scene)
    texture_lock.MUV_TexLockIntr.init_props(scene)
    texture_projection.MUV_TexProj.init_props(scene)
    world_scale_uv.MUV_WSUV.init_props(scene)


def clear_props(scene):
    # Texture Wrap
    del scene.muv_texwrap_enabled
    del scene.muv_texwrap_set_and_refer
    del scene.muv_texwrap_selseq

    # Select UV
    del scene.muv_seluv_enabled

    # Align UV
    del scene.muv_auv_enabled
    del scene.muv_auv_transmission
    del scene.muv_auv_select
    del scene.muv_auv_vertical
    del scene.muv_auv_horizontal
    del scene.muv_auv_location

    # Smooth UV
    del scene.muv_smuv_enabled
    del scene.muv_smuv_transmission
    del scene.muv_smuv_mesh_infl
    del scene.muv_smuv_select

    # Pack UV
    del scene.muv_packuv_enabled
    del scene.muv_packuv_allowable_center_deviation
    del scene.muv_packuv_allowable_size_deviation

    # Move UV
    del scene.muv_mvuv_enabled

    # UVW
    del scene.muv_uvw_enabled
    del scene.muv_uvw_assign_uvmap

    # Unwrap Constraint
    del scene.muv_unwrapconst_enabled
    del scene.muv_unwrapconst_u_const
    del scene.muv_unwrapconst_v_const

    # Preserve UV Aspect
    del scene.muv_preserve_uv_enabled
    del scene.muv_preserve_uv_tex_image
    del scene.muv_preserve_uv_origin

    # Flip/Rotate UV
    del scene.muv_fliprot_enabled
    del scene.muv_fliprot_seams

    # Mirror UV
    del scene.muv_mirroruv_enabled
    del scene.muv_mirroruv_axis

    # Transfer UV
    del scene.muv_transuv_enabled
    del scene.muv_transuv_invert_normals
    del scene.muv_transuv_copy_seams

    # Align UV Cursor
    del scene.muv_auvc_enabled
    del scene.muv_auvc_cursor_loc
    del scene.muv_auvc_align_menu

    # UV Cursor Location
    del scene.muv_uvcloc_enabled

    copy_paste_uv.MUV_CPUV.del_props(scene)
    copy_paste_uv_object.MUV_CPUVObj.del_props(scene)
    copy_paste_uv_uvedit.MUV_CPUVIE.del_props(scene)
    uv_bounding_box.MUV_UVBB.del_props(scene)
    uv_inspection.MUV_UVInsp.del_props(scene)
    uv_sculpt.MUV_UVSculpt.del_props(scene)
    texture_lock.MUV_TexLockIntr.del_props(scene)
    texture_projection.MUV_TexProj.del_props(scene)

    del scene.muv_props
