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


addon_keymaps = []

class MUV_PieMenu(bpy.types.Menu):
    bl_idname = "pie.muv_cpuv"
    bl_label = "Magic UV"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("uv.muv_cpuv_copy_uv", text="Copy UV")
        pie.operator("uv.muv_cpuv_paste_uv", text="Paste UV")
        pie.operator("uv.muv_cpuv_selseq_copy_uv", text="Copy UV (Selection Sequence)")
        pie.operator("uv.muv_cpuv_selseq_paste_uv", text="Paste UV (Selection Sequence)")
        pie.operator("uv.muv_fliprot", text="Flip/Rotate UV")
        pie.operator("uv.muv_transuv_copy", text="Transfer UV Copy")
        pie.operator("uv.muv_transuv_paste", text="Transfer UV Paste")


def register():
    bpy.utils.register_module(__name__)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu_pie', 'U', 'PRESS', ctrl=True, alt=False, shift=False)
        kmi.properties.name = MUV_PieMenu.bl_idname
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_module(__name__)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
