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

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "XX XXX 2015"

from . import muv_cpuv_ops
from . import muv_cpuv_selseq_ops
from . import muv_fliprot_ops
from . import muv_transuv_ops
from . import muv_texwrap_ops
from . import muv_texlock_ops
from . import muv_texproj_ops


# Copy/Paste UV master menu
class MUV_CPUVMenu(bpy.types.Menu):
    bl_idname = "uv.muv_cpuv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV Menu"

    def draw(self, context):
        self.layout.menu(muv_cpuv_ops.MUV_CPUVCopyUVMenu.bl_idname, icon="PLUGIN")
        self.layout.menu(muv_cpuv_ops.MUV_CPUVPasteUVMenu.bl_idname, icon="PLUGIN")
        self.layout.menu(muv_cpuv_selseq_ops.MUV_CPUVSelSeqCopyUVMenu.bl_idname, icon="PLUGIN")
        self.layout.menu(muv_cpuv_selseq_ops.MUV_CPUVSelSeqPasteUVMenu.bl_idname, icon="PLUGIN")


# Transfer UV master menu
class MUV_TransUVMenu(bpy.types.Menu):
    bl_idname = "uv.muv_transuv_menu"
    bl_label = "Transfer UV"
    bl_description = "Transfer UV Menu"

    def draw(self, context):
        self.layout.operator(muv_transuv_ops.MUV_TransUVCopy.bl_idname, icon="PLUGIN")
        self.layout.operator(muv_transuv_ops.MUV_TransUVPaste.bl_idname, icon="PLUGIN")


# Texture Wrap master menu
class MUV_TexWrapMenu(bpy.types.Menu):
    bl_idname = "uv.muv_texwrap_menu"
    bl_label = "Texture Wrap"
    bl_description = "Texture Wrap Menu"

    def draw(self, context):
        self.layout.operator(muv_texwrap_ops.MUV_TexWrapCopy.bl_idname, icon="PLUGIN")
        self.layout.operator(muv_texwrap_ops.MUV_TexWrapPaste.bl_idname, icon="PLUGIN")

# Texture Lock master menu
class MUV_TexLockMenu(bpy.types.Menu):
    bl_idname = "uv.muv_texlock_menu"
    bl_label = "Texture Lock"
    bl_description = "Texture Lock Menu"

    def draw(self, context):
        self.layout.operator(muv_texlock_ops.MUV_TexLockScale.bl_idname, icon="PLUGIN")
        self.layout.operator(muv_texlock_ops.MUV_TexLockRotation.bl_idname, icon="PLUGIN")

# Texture Projection master menu
class MUV_TexProjMenu(bpy.types.Menu):
    bl_idname = "uv.muv_texproj_menu"
    bl_label = "Texture Projection"
    bl_description = "Project texture menu"

    def draw(self, context):
        self.layout.operator(muv_texproj_ops.TPStartTextureProjection.bl_idname)
        self.layout.operator(muv_texproj_ops.TPProjectTexture.bl_idname)
        self.layout.operator(muv_texproj_ops.TPStopTextureProjection.bl_idname)


