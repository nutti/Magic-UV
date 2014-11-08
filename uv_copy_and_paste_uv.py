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

bl_info = {
    "name" : "Copy and Paste UV",
    "author" : "Nutti",
    "version" : (2,0),
    "blender" : (2, 7, 0),
    "location" : "UV Mapping > Copy and Paste UV",
    "description" : "Copy and Paste UV data",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UV"
}

src_indices = None           # source indices
dest_indices = None          # destination indices
src_uv_map = None            # source uv map
dest_uv_map = None           # destination uv map
src_obj = None               # source object

# copy UV
class CopyAndPasteUVCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object."""
    
    bl_idname = "uv.copy_uv"
    bl_label = "Copy UV"
    bl_description = "Copy UV data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Copy UV coordinate.")
        
        return copy_from(self, "")


# paste UV
class CopyAndPasteUVPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied."""
    
    bl_idname = "uv.paste_uv"
    bl_label = "Paste UV"
    bl_description = "Paste UV data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Paste UV coordinate.")
    
        return paste_to(self, "")



# copy UV map (sub menu operator)
class CopyAndPasteUVCopyUVMapSubOpt(bpy.types.Operator):
    bl_idname = "uv.copy_uv_map_sub_opt"
    bl_label = "Copy UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()
    
    def execute(self, context):
        self.report(
            {'INFO'},
            "Copy UV coordinate. (UV map:" + self.uv_map + ")")
        
        return copy_from(self, self.uv_map)


# copy UV map
class CopyAndPasteUVCopyUVMap(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.copy_uv_map"
    bl_label = "Copy UV Map"
    bl_description = "Copy UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        global menu_count
    
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CopyAndPasteUVCopyUVMapSubOpt.bl_idname,
                text=m).uv_map = m
            

# paste UV map (sub menu operator)
class CopyAndPasteUVPasteUVMapSubOpt(bpy.types.Operator):
    bl_idname = "uv.paste_uv_map_sub_opt"
    bl_label = "Paste UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()
    
    def execute(self, context):
        self.report(
            {'INFO'},
            "Paste UV coordinate. (UV map:" + self.uv_map + ")")
        return paste_to(self, self.uv_map)


# paste UV map
class CopyAndPasteUVPasteUVMap(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.paste_uv_map"
    bl_label = "Paste UV Map"
    bl_description = "Paste UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        global menu_count
    
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CopyAndPasteUVPasteUVMapSubOpt.bl_idname,
                text=m).uv_map = m

# copy
def copy_from(self, uv_map):
    # global variables
    global src_indices
    global src_uv_map
    global src_obj
    
    # get active (source) object to be copied from
    active_obj = bpy.context.active_object;

    # change to 'OBJECT' mode, in order to access internal data
    mode_orig = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # create source indices list
    src_indices = []
    for i in range(len(active_obj.data.polygons)):
        # get selected faces
        poly = active_obj.data.polygons[i]
        if poly.select:
           src_indices.extend(poly.loop_indices)
    
    # check if any faces are selected
    if len(src_indices) == 0:
        self.report({'WARNING'}, "No faces are not selected.")
        bpy.ops.object.mode_set(mode=mode_orig)
        return {'CANCELLED'}
    else:
        self.report({'INFO'}, "%d indices are selected." % len(src_indices))
        src_obj = active_obj
    
    if uv_map == "":
        src_uv_map = src_obj.data.uv_layers.active.name
    else:
        src_uv_map = uv_map
    
    # revert to original mode
    bpy.ops.object.mode_set(mode=mode_orig)
    
    return {'FINISHED'}


# paste
def paste_to(self, uv_map):
    # global variables
    global src_indices
    global dest_indices
    global src_uv_map
    global dest_uv_map
    global src_obj
    
    # check if copying operation was executed
    if src_indices is None or src_obj is None:
        self.report({'WARNING'}, "Do copy operation at first.")
        return {'CANCELLED'}
    
    # get active (source) object to be pasted to
    active_obj = bpy.context.active_object

    # change to 'OBJECT' mode, in order to access internal data
    mode_orig = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # create source indices list
    dest_indices = []
    for i in range(len(active_obj.data.polygons)):
        # get selected faces
        poly = active_obj.data.polygons[i]
        if poly.select:
            dest_indices.extend(poly.loop_indices)
    
    if len(dest_indices) != len(src_indices):
        self.report(
            {'WARNING'},
            "Number of selected faces is different from copied faces." +
            "(src:%d, dest:%d)" % (len(src_indices), len(dest_indices)))
        bpy.ops.object.mode_set(mode=mode_orig)
        return {'CANCELLED'}
    else:
        dest_obj = active_obj
        
    if uv_map == "":
        dest_uv_map = dest_obj.data.uv_layers.active.name
    else:
        dest_uv_map = uv_map

    # update UV data
    src_uv = src_obj.data.uv_layers[src_uv_map]
    dest_uv = dest_obj.data.uv_layers[dest_uv_map]
    for i in range(len(dest_indices)):
        dest_data = dest_uv.data[dest_indices[i]]
        src_data = src_uv.data[src_indices[i]]
        dest_data.uv = src_data.uv

    self.report({'INFO'}, "%d indices are copied." % len(dest_indices))

    # revert to original mode
    bpy.ops.object.mode_set(mode=mode_orig)

    return {'FINISHED'}


# registration
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(CopyAndPasteUVCopyUV.bl_idname)
    self.layout.operator(CopyAndPasteUVPasteUV.bl_idname)
    self.layout.menu(CopyAndPasteUVCopyUVMap.bl_idname)
    self.layout.menu(CopyAndPasteUVPasteUVMap.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)


if __name__ == "__main__":
    register()