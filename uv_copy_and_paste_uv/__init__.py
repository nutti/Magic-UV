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
__version__ = "3.0"
__date__ = "X XXXX 2015"

bl_info = {
    "name" : "Copy and Paste UV",
    "author" : "Nutti",
    "version" : (3,0),
    "blender" : (2, 7, 3),
    "location" : "UV Mapping > Copy and Paste UV",
    "description" : "Copy and Paste UV data",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UV"
}

if "bpy" in locals():
    import imp
    imp.reload(cpuv_menu)
    imp.reload(cpuv_common)
    imp.reload(cpuv_default_operation)
    imp.reload(cpuv_selseq_operation)
    imp.reload(cpuv_uvmap_operation)
    imp.reload(cpuv_fliprot_operation)
else:
    from . import cpuv_menu
    from . import cpuv_common
    from . import cpuv_default_operation
    from . import cpuv_selseq_operation
    from . import cpuv_uvmap_operation
    from . import cpuv_fliprot_operation

import bpy

# registration
def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(cpuv_menu.CPUVMenu.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)


if __name__ == "__main__":
    register()


