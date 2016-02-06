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
__version__ = "4.0"
__date__ = "XX XXX 2015"

bl_info = {
    "name": "Magic UV",
    "author": "Nutti",
    "version": (4, 0),
    "blender": (2, 73, 0),
    "location": "UV Mapping > Magic UV",
    "description": "UV Tools",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/UV/Copy_Paste_UVs",
    "tracker_url": "https://github.com/nutti/Copy-And-Paste-UV",
    "category": "UV"
}

if "bpy" in locals():
    import imp
    imp.reload(muv_preferences)
    imp.reload(muv_menu)
    imp.reload(muv_common)
    imp.reload(muv_props)
    imp.reload(muv_cpuv_ops)
    imp.reload(muv_cpuv_selseq_ops)
    imp.reload(muv_fliprot_ops)
    imp.reload(muv_transuv_ops)
    imp.reload(muv_texwrap_ops)
    imp.reload(muv_texproj_face_ops)
    imp.reload(muv_texlock_ops)
    imp.reload(muv_uvbb_ops)
else:
    from . import muv_preferences
    from . import muv_menu
    from . import muv_common
    from . import muv_props
    from . import muv_cpuv_ops
    from . import muv_cpuv_selseq_ops
    from . import muv_fliprot_ops
    from . import muv_transuv_ops
    from . import muv_texwrap_ops
    from . import muv_texproj_face_ops
    from . import muv_texlock_ops
    from . import muv_uvbb_ops

import bpy

# registration
def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(muv_menu.MUV_CPUVMenu.bl_idname, icon="PLUGIN")
    self.layout.operator(muv_fliprot_ops.MUV_FlipRot.bl_idname, icon="PLUGIN")
    self.layout.menu(muv_menu.MUV_TransUVMenu.bl_idname, icon="PLUGIN")
    self.layout.menu(muv_menu.MUV_TexWrapMenu.bl_idname, icon="PLUGIN")
    self.layout.menu(muv_menu.MUV_TexProjFaceMenu.bl_idname, icon="PLUGIN")
    self.layout.menu(muv_menu.MUV_TexLockMenu.bl_idname, icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_fn)
    muv_props.init_props(bpy.types.Scene)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_fn)
    muv_props.clear_props(bpy.types.Scene)


if __name__ == "__main__":
    register()

