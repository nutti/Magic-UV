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

bl_info = {
    "name" : "Copy and Paste UV",
    "author" : "Nutti",
    "version" : (1,0),
    "blender" : (2, 6, 5),
    "location" : "UV Mapping > Copy and Paste UV",
    "description" : "Copy and Paste UV data",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "UV"
}

import bpy

src_indices=None           # source indices
dest_indices=None          # destination indices
src_obj=None               # source object

# copy UV
class CopyAndPasteUV_CopyUV( bpy.types.Operator ):
    ''''''
    bl_idname = "uv.copy_uv"
    bl_label = "Copy UV"
    bl_description = "Copy UV data"
    bl_options = { 'REGISTER', 'UNDO' }

    def execute( self, context):
        
        # global variables
        global src_indices
        global dest_indices
        global src_obj
        
        # get active (source) object to be copied from.
        active_obj = bpy.context.active_object;

        bpy.ops.object.mode_set( mode = 'OBJECT' )

        # create source indices list
        src_indices=list()
        for i in range( len( active_obj.data.polygons ) ):
            # get selected faces
            poly = active_obj.data.polygons[ i ]
            if poly.select:
                for j in range( len( poly.loop_indices ) ):
                    src_indices.append( poly.loop_indices[ j ] )
        
        if len( src_indices ) == 0:
            self.report( { 'WARNING' }, "No faces are not selected." )
        else:
            src_obj=active_obj
        
        bpy.ops.object.mode_set( mode = 'EDIT' )
        
        return { 'FINISHED' }

# paste UV
class CopyPasteUVs_PasteUV( bpy.types.Operator ):
    ''''''
    bl_idname = "uv.paste_uv"
    bl_label = "Paste UV"
    bl_description = "Paste UV data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        # global variables
        global src_indices
        global dest_indices
        global src_obj
        
        # get active (source) object to be pasted to.
        active_obj = bpy.context.active_object

        bpy.ops.object.mode_set( mode = 'OBJECT' )

        # create source indices list
        dest_indices = list()
        for i in range( len( active_obj.data.polygons ) ):
            # get selected faces
            poly = active_obj.data.polygons[ i ]
            if poly.select:
                for j in range( len( poly.loop_indices ) ):
                    dest_indices.append( poly.loop_indices[ j ] )
        
        if len( dest_indices ) != len( src_indices ):
            self.report( { 'WARNING' }, "Number of selected faces is different from copied faces." )
            return { 'CANCELLED' }
        else:
            dest_obj = active_obj

        # update UV data
        src_uv = src_obj.data.uv_layers.active         # source UV data
        dest_uv = dest_obj.data.uv_layers.active       # destination UV data
        for i in range( len( dest_indices ) ):
            dest_uv.data[ dest_indices[ i ] ].uv = src_uv.data[ src_indices[ i ] ].uv

        bpy.ops.object.mode_set( mode = 'EDIT' )

        return { 'FINISHED' }

# registration

def add_to_menu( self, context ):
    self.layout.operator( "uv.copy_uv" )
    self.layout.operator( "uv.paste_uv" )
    
def register():
    bpy.utils.register_module( __name__ )
    bpy.types.VIEW3D_MT_uv_map.append( add_to_menu )

def unregister():
    bpy.utils.unregister_module( __name__ )
    bpy.types.VIEW3D_MT_uv_map.remove( add_to_menu )
    
if __name__ == "__main__":
    register()
