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


import bpy


def check_version(major, minor, _):
    """
    Check blender version
    """

    if bpy.app.version[0] == major and bpy.app.version[1] == minor:
        return 0
    if bpy.app.version[0] > major:
        return 1
    if bpy.app.version[1] > minor:
        return 1
    return -1


def make_annotations(cls):
    if check_version(2, 80, 0) < 0:
        return cls

    # make annotation from attributes
    props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in props.items():
            annotations[k] = v
            delattr(cls, k)

    return cls


def matmul(m1, m2):
    if check_version(2, 80, 0) < 0:
        return m1 * m2

    return m1 @ m2


def layout_split(layout, factor=0.0, align=False):
    if check_version(2, 80, 0) < 0:
        return layout.split(percentage=factor, align=align)

    return layout.split(factor=factor, align=align)


def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_prefereneces

    return context.preferences
