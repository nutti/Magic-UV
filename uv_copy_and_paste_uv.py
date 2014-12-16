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
import bmesh

bl_info = {
    "name" : "Copy and Paste UV",
    "author" : "Nutti",
    "version" : (2,0),
    "blender" : (2, 7, 2),
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
src_obj = None               # source object

# master menu
class CopyAndPasteUVMenu(bpy.types.Menu):
    bl_idname = "uv.copy_and_paste_uv_menu"
    bl_label = "Copy/Paste UV"
    bl_description = "Copy and Paste UV Menu"

    def draw(self, context):
        self.layout.operator(CopyAndPasteUVCopyUV.bl_idname)
        self.layout.operator(CopyAndPasteUVPasteUV.bl_idname)
        self.layout.operator(CopyAndPasteUVCopyUVBySelSeq.bl_idname)
        self.layout.operator(CopyAndPasteUVPasteUVBySelSeq.bl_idname)
        self.layout.menu(CopyAndPasteUVCopyUVMap.bl_idname)
        self.layout.menu(CopyAndPasteUVPasteUVMap.bl_idname)


# copy UV
class CopyAndPasteUVCopyUV(bpy.types.Operator):
    """Copying UV coordinate on selected object."""
    
    bl_idname = "uv.copy_uv"
    bl_label = "Copy UV"
    bl_description = "Copy UV data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global src_indices
        global src_uv_map
        global src_obj
    
        self.report({'INFO'}, "Copy UV coordinate.")
        
        # prepare for coping
        ret, src_obj, mode_orig = prep_copy()
        if ret != 0:
            return {'CANCELLED'}
        
        # copy
        src_indices = get_selected_indices(src_obj)
        ret, src_uv_map = copy_opt(self, "", src_obj, src_indices)
        
        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# paste UV
class CopyAndPasteUVPasteUV(bpy.types.Operator):
    """Paste UV coordinate which is copied."""
    
    bl_idname = "uv.paste_uv"
    bl_label = "Paste UV"
    bl_description = "Paste UV data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global src_indices
        global dest_indices
        global src_uv_map
        global src_obj
    
        self.report({'INFO'}, "Paste UV coordinate.")

        ret, dest_obj, mode_orig = prep_paste(src_obj, src_indices)
        if ret != 0:
            return {'CANCELLED'}
        
        dest_indices = get_selected_indices(dest_obj)
        ret = paste_opt(
            self, "", src_obj, src_indices, src_uv_map, dest_obj, dest_indices)
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


# copy UV (by selection sequence)
class CopyAndPasteUVCopyUVBySelSeq(bpy.types.Operator):
    """Copying UV coordinate on selected object by selection sequence."""
    
    bl_idname = "uv.copy_uv_sel_seq"
    bl_label = "Copy UV (Selection Sequence)"
    bl_description = "Copy UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global src_indices
        global src_uv_map
        global src_obj

        self.report({'INFO'}, "Copy UV coordinate. (sequence)")
        
        # prepare for coping
        ret, src_obj, mode_orig = prep_copy()
        if ret != 0:
            return {'CANCELLED'}

        # copy
        src_indices = get_selected_indices_by_sel_seq(src_obj)
        ret, src_uv_map = copy_opt(self, "", src_obj, src_indices)

        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}


# paste UV (by selection sequence)
class CopyAndPasteUVPasteUVBySelSeq(bpy.types.Operator):
    """Paste UV coordinate which is copied by selection sequence."""
    
    bl_idname = "uv.paste_uv_sel_seq"
    bl_label = "Paste UV (Selection Sequence)"
    bl_description = "Paste UV data by selection sequence."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global src_indices
        global dest_indices
        global src_uv_map
        global src_obj

        self.report({'INFO'}, "Paste UV coordinate. (sequence)")

        ret, dest_obj, mode_orig = prep_paste(src_obj, src_indices)
        if ret != 0:
            return {'CANCELLED'}

        dest_indices = get_selected_indices_by_sel_seq(dest_obj)
        ret = paste_opt(
            self, "", src_obj, src_indices, src_uv_map, dest_obj, dest_indices)
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}

        return {'FINISHED'}


# copy UV map (sub menu operator)
class CopyAndPasteUVCopyUVMapSubOpt(bpy.types.Operator):
    bl_idname = "uv.copy_uv_map_sub_opt"
    bl_label = "Copy UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()
    
    def execute(self, context):
        global src_indices
        global src_uv_map
        global src_obj
        
        self.report(
            {'INFO'},
            "Copy UV coordinate. (UV map:" + self.uv_map + ")")

        # prepare for coping
        ret, src_obj, mode_orig = prep_copy()
        if ret != 0:
            return {'CANCELLED'}
        
        # copy
        src_indices = get_selected_indices(src_obj)
        ret, src_uv_map = copy_opt(self, self.uv_map, src_obj, src_indices)
        
        # finish coping
        fini_copy(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


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
        global src_indices
        global dest_indices
        global src_uv_map
        global src_obj
        
        self.report(
            {'INFO'},
            "Paste UV coordinate. (UV map:" + self.uv_map + ")")
        
        self.report({'INFO'}, "Paste UV coordinate.")

        ret, dest_obj, mode_orig = prep_paste(src_obj, src_indices)
        if ret != 0:
            return {'CANCELLED'}
        
        dest_indices = get_selected_indices(dest_obj)
        ret = paste_opt(
            self, self.uv_map, src_obj, src_indices, src_uv_map,
            dest_obj, dest_indices)
        fini_paste(mode_orig)
        if ret != 0:
            return {'CANCELLED'}
        
        return {'FINISHED'}


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


def prep_copy():
    """
    parepare for copy operation.
    @return tuple(error code, active object, current mode)
    """
    # get active (source) object to be copied from
    obj = bpy.context.active_object;

    # change to 'OBJECT' mode, in order to access internal data
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return (0, obj, mode)


# finish copy operation
def fini_copy(mode_orig):
    """
    finish copy operation.
    @param  mode_orig orignal mode
    """
    # revert to original mode
    bpy.ops.object.mode_set(mode=mode_orig)


# prepare for paste operation
def prep_paste(src_obj, src_indices):
    """
    prepare for paste operation.
    @param  src_obj object that is copied from
    @param  src_indices indices will be copied
    @return tuple(error code, active object, current mode)
    """
     # check if copying operation was executed
    if src_indices is None or src_obj is None:
        self.report({'WARNING'}, "Do copy operation at first.")
        return (1, None, None)
    
    # get active (source) object to be pasted to
    obj = bpy.context.active_object

    # change to 'OBJECT' mode, in order to access internal data
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return (0, obj, mode)


# finish paste operation
def fini_paste(mode):
    """
    finish paste operation.
    @param  mode_orig orignal mode
    """
    # revert to original mode
    bpy.ops.object.mode_set(mode=mode)


def get_selected_indices(obj):
    """
    get selected indices.
    @param  obj object
    @return indices
    """
    out = []
    for i in range(len(obj.data.polygons)):
        # get selected faces
        poly = obj.data.polygons[i]
        if poly.select:
           out.extend(poly.loop_indices)
    return out


def get_selected_indices_by_sel_seq(obj):
    """
    get selected indices.
    @param  obj object
    @return indices
    """
    out = []
    faces = []
    
    # get selection sequence
    mode_orig = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    for e in bm.select_history:
        if isinstance(e, bmesh.types.BMFace) and e.select:
            faces.append(e.loops[0].face.index)
    
    # get selected indices by selection sequence
    bpy.ops.object.mode_set(mode='OBJECT')
    for f in faces:
        poly = obj.data.polygons[f]
        out.extend(poly.loop_indices)
    bpy.ops.object.mode_set(mode=mode_orig)
    
    return out


def copy_opt(self, uv_map, src_obj, src_indices):
    """
    copy operation.
    @param  self operation object
    @param  uv_map UV Map to be copied. (current map when null str)
    @param  src_obj source object
    @param  src_indices source indices
    @return tuple(error code, UV map)
    """
    # check if any faces are selected
    if len(src_indices) == 0:
        self.report({'WARNING'}, "No faces are not selected.")
        return (1, None)
    else:
        self.report({'INFO'}, "%d indices are selected." % len(src_indices))
    
    if uv_map == "":
        uv_map = src_obj.data.uv_layers.active.name
    else:
        uv_map = uv_map
    
    return (0, uv_map)


def paste_opt(self, uv_map, src_obj, src_indices,
    src_uv_map, dest_obj, dest_indices):
    """
    paste operation.
    @param  self operation object
    @param  uv_map UV Map to be pasted. (current map when null str)
    @param  src_obj source object
    @param  src_indices source indices
    @param  src_uv_map source UV map
    @param  dest_obj destination object
    @param  dest_indices destination object
    @return error code
    """
    if len(dest_indices) != len(src_indices):
        self.report(
            {'WARNING'},
            "Number of selected faces is different from copied faces." +
            "(src:%d, dest:%d)" % (len(src_indices), len(dest_indices)))
        return 1
        
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

    return 0


# registration
def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(CopyAndPasteUVMenu.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)


if __name__ == "__main__":
    register()
