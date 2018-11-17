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
__version__ = "5.2"
__date__ = "17 Nov 2018"


from .op import (
    align_uv,
    align_uv_cursor,
    copy_paste_uv,
    copy_paste_uv_object,
    copy_paste_uv_uvedit,
    flip_rotate_uv,
    mirror_uv,
    move_uv,
    pack_uv,
    preserve_uv_aspect,
    select_uv,
    smooth_uv,
    texture_lock,
    texture_projection,
    texture_wrap,
    transfer_uv,
    unwrap_constraint,
    uv_bounding_box,
    uv_inspection,
    uv_sculpt,
    uvw,
    world_scale_uv,
)


__all__ = [
    'MUV_Properties',
    'init_props',
    'clear_props',
]


# Properties used in this add-on.
# pylint: disable=W0612
class MUV_Properties():
    def __init__(self):
        self.prefs = MUV_Prefs()


class MUV_Prefs():
    expanded = {
        "info_desc": False,
        "info_loc": False,
        "conf_uvsculpt": False,
        "conf_uvinsp": False,
        "conf_texproj": False,
        "conf_uvbb": False
    }


def init_props(scene):
    scene.muv_props = MUV_Properties()

    align_uv.Properties.init_props(scene)
    align_uv_cursor.Properties.init_props(scene)
    copy_paste_uv.Properties.init_props(scene)
    copy_paste_uv_object.Properties.init_props(scene)
    copy_paste_uv_uvedit.Properties.init_props(scene)
    flip_rotate_uv.Properties.init_props(scene)
    mirror_uv.Properties.init_props(scene)
    move_uv.Properties.init_props(scene)
    pack_uv.Properties.init_props(scene)
    preserve_uv_aspect.Properties.init_props(scene)
    select_uv.Properties.init_props(scene)
    smooth_uv.Properties.init_props(scene)
    texture_lock.Properties.init_props(scene)
    texture_projection.Properties.init_props(scene)
    texture_wrap.Properties.init_props(scene)
    transfer_uv.Properties.init_props(scene)
    unwrap_constraint.Properties.init_props(scene)
    uv_bounding_box.Properties.init_props(scene)
    uv_inspection.Properties.init_props(scene)
    uv_sculpt.Properties.init_props(scene)
    uvw.Properties.init_props(scene)
    world_scale_uv.Properties.init_props(scene)


def clear_props(scene):
    align_uv.Properties.del_props(scene)
    align_uv_cursor.Properties.del_props(scene)
    copy_paste_uv.Properties.del_props(scene)
    copy_paste_uv_object.Properties.del_props(scene)
    copy_paste_uv_uvedit.Properties.del_props(scene)
    flip_rotate_uv.Properties.del_props(scene)
    mirror_uv.Properties.del_props(scene)
    move_uv.Properties.del_props(scene)
    pack_uv.Properties.del_props(scene)
    preserve_uv_aspect.Properties.del_props(scene)
    select_uv.Properties.del_props(scene)
    smooth_uv.Properties.del_props(scene)
    texture_lock.Properties.del_props(scene)
    texture_projection.Properties.del_props(scene)
    texture_wrap.Properties.del_props(scene)
    transfer_uv.Properties.del_props(scene)
    unwrap_constraint.Properties.del_props(scene)
    uv_bounding_box.Properties.del_props(scene)
    uv_inspection.Properties.del_props(scene)
    uv_sculpt.Properties.del_props(scene)
    uvw.Properties.del_props(scene)
    world_scale_uv.Properties.del_props(scene)

    del scene.muv_props
