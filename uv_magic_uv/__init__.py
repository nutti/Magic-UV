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


bl_info = {
    "name": "Magic UV",
    "author": "Nutti, Mifth, Jace Priester, kgeogeo, mem, imdjs"
              "Keith (Wahooney) Boshoff, McBuff, MaxRobinot, Alexander Milovsky",
    "version": (5, 2, 0),
    "blender": (2, 79, 0),
    "location": "See Add-ons Preferences",
    "description": "UV Toolset. See Add-ons Preferences for details",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/"
                "Py/Scripts/UV/Magic_UV",
    "tracker_url": "https://github.com/nutti/Magic-UV",
    "category": "UV"
}

if "bpy" in locals():
    import importlib
    importlib.reload(op)
    importlib.reload(ui)
    importlib.reload(common)
    importlib.reload(preferences)
    importlib.reload(properites)
    importlib.reload(addon_updater_ops)
    importlib.reload(addon_updater)
else:
    from . import op
    from . import ui
    from . import common
    from . import preferences
    from . import properites
    from . import addon_updater_ops
    from . import addon_updater

import bpy


def register():
    if not common.is_console_mode():
        addon_updater_ops.register(bl_info)
    properites.init_props(bpy.types.Scene)
    bpy.utils.register_module(__name__)
    if preferences.Preferences.enable_builtin_menu:
        preferences.add_builtin_menu()


def unregister():
    if preferences.Preferences.enable_builtin_menu:
        preferences.remove_builtin_menu()
    bpy.utils.unregister_module(__name__)
    properites.clear_props(bpy.types.Scene)
    if not common.is_console_mode():
        addon_updater_ops.unregister()


if __name__ == "__main__":
    register()
