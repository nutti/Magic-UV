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

from bpy.props import FloatProperty

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"


DEBUG = False

# Properties used in this add-on.
class MUV_Properties():
    cpuv = None
    cpuv_selseq = None
    transuv = None
    texwrap = None
    uvbb = None
    texlock = None

    def __init__(self):
        self.cpuv = MUV_CPUVProps()
        self.cpuv_selseq = MUV_CPUVSelSeqProps()
        self.transuv = MUV_TransUVProps()
        self.texwrap = MUV_TexWrapProps()
        self.uvbb = MUV_UVBBProps()
        self.texlock = MUV_TexLockProps()


class MUV_CPUVProps():
    src_uvs = []
    src_pin_uvs = []


class MUV_CPUVSelSeqProps():
    src_uvs = []
    src_pin_uvs = []


class MUV_TransUVProps():
    topology_copied = []


class MUV_TexWrapProps():
    src_vlist = []
    src_uvlist = []


class MUV_UVBBProps():
    uvs_ini = []
    ctrl_points_ini = []
    ctrl_points = []
    running = False


class MUV_TexLockProps():
    src_vlist = []
    src_uvlist = []
    intr_src_vlist = []
    intr_src_uvlist = []
    intr_running = False


def init_props(scene):
    scene.muv_props = MUV_Properties()
    scene.muv_uvbb_cp_size = FloatProperty(
        name="Size",
        description="Control Point Size",
        default=6.0,
        min=3.0,
        max=100.0)
    scene.muv_uvbb_cp_react_size = FloatProperty(
        name="React Size",
        description="Size event fired",
        default=10.0,
        min=3.0,
        max=100.0)


def clear_props(scene):
    del scene.muv_props
    del scene.muv_uvbb_cp_size
    del scene.muv_uvbb_cp_react_size

