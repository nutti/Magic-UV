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
import bgl
import mathutils
from bpy_extras import view3d_utils
from bpy.props import *
from collections import namedtuple

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "0.1"
__date__ = "26 May 2015"

bl_info = {
    "name": "Texture Projection",
    "author": "Nutti",
    "version": (0, 1),
    "blender": (2, 70, 0),
    "location": "UV > Texture Projection",
    "description": "Project texture to mesh in View3D mode.",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "UV"
}

SelectedFaceInfo = namedtuple(
    'SelectedFaceInfo', 'face_index indices vertices loc loc_on_canvas')
Rect = namedtuple('Rect', 'x0 y0 x1 y1')
Rect2 = namedtuple('Rect2', 'x y width height')

addon_keymaps = []


def SetTextureImageName(scene, context):
    items = [(key, key, "") for key in bpy.data.images.keys()]
    items.append(("None", "None", ""))
    return items


# Properties used in this add-on.
class TPProperties(bpy.types.PropertyGroup):
    running = BoolProperty(
        name="Is Running",
        description="Is TP operation running now?",
        default=False)


class View3DModeMemory():
    __mode_orig = None

    def __init__(self):
        self.__mode_orig = bpy.context.object.mode

    def change_mode(self, mode):
        bpy.ops.object.mode_set(mode=mode)

    def __del__(self):
        bpy.ops.object.mode_set(mode=self.__mode_orig)


class TPError(Exception):
    """This add-on's exception class."""

    def __init__(self, level, err_str):
        self.err_level = level
        self.err_str = err_str

    def __str__(self):
        return repr(self.err_str)

    def report(self, obj):
        obj.report(self.err_level, self.err_str)
    

def memorize_view_3d_mode(fn):
    def __memorize_view_3d_mode(*args, **kwargs):
        mode_orig = bpy.context.object.mode
        result = fn(*args, **kwargs)
        bpy.ops.object.mode_set(mode=mode_orig)
        return result
    return __memorize_view_3d_mode


def get_selected_faces(obj):
    """
    get information about selected faces.
    @param  obj object
    @return information about selected faces (list of SelectedFaceInfo)
    """
    return get_faces_from_indices(obj, get_selected_face_indices(obj))


@memorize_view_3d_mode
def get_selected_face_indices(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    polys = obj.data.polygons
    return [i for i, p in enumerate(polys) if p.select is True]


def get_faces_from_indices(obj, indices):
    polys = obj.data.polygons
    return [
        SelectedFaceInfo(
            i,
            list(polys[i].loop_indices),
            list(polys[i].vertices),
            [], [])
        for i in indices]


def get_canvas(context, magnitude):
    """Get canvas to be renderred texture."""
    PAD_X = 20
    PAD_Y = 20
    width = context.region.width
    height = context.region.height
    
    center_x = width * 0.5
    center_y = height * 0.5
    len_x = (width - PAD_X * 2.0) * magnitude
    len_y = (height - PAD_Y * 2.0) * magnitude
    
    x0 = int(center_x - len_x * 0.5)
    y0 = int(center_y - len_y * 0.5)
    x1 = int(center_x + len_x * 0.5)
    y1 = int(center_y + len_y * 0.5)
    return Rect(x0, y0, x1, y1)


def rect_to_rect2(rect):
    """Convert Rect1 to Rect2"""
    return Rect2(
        rect.x0,
        rect.y0,
        rect.x1 - rect.x0,
        rect.y1 - rect.y0
        )


def region_to_canvas(region, rg_vec, canvas):
    """Convert screen region to canvas"""  
    cv_rect = rect_to_rect2(canvas)
    cv_vec = mathutils.Vector()
    cv_vec.x = (rg_vec.x - cv_rect.x) / cv_rect.width
    cv_vec.y = (rg_vec.y - cv_rect.y) / cv_rect.height
    return cv_vec


class TPTextureRenderer(bpy.types.Operator):
    """Rendering texture"""
    
    bl_idname = "uv.tp_texture_renderer"
    bl_label = "Texture renderer"

    __handle = None
    __timer = None
    
    @staticmethod
    def handle_add(self, context):
        TPTextureRenderer.__handle = bpy.types.SpaceView3D.draw_handler_add(
            TPTextureRenderer.draw_texture,
            (self, context), 'WINDOW', 'POST_PIXEL')
    
    @staticmethod
    def handle_remove(self, context):
        if TPTextureRenderer.__handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(
                TPTextureRenderer.__handle, 'WINDOW')
            TPTextureRenderer.__handle = None
    
    @staticmethod
    def draw_texture(self, context):
        wm = context.window_manager
        sc = context.scene
        
        # no texture is selected
        if sc.tex_image == "None":
            return

        # setup rendering region
        rect = get_canvas(context, sc.tex_magnitude)
        positions = [
            [rect.x0, rect.y0],
            [rect.x0, rect.y1],
            [rect.x1, rect.y1],
            [rect.x1, rect.y0]
            ]
        tex_coords = [[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]]

        # get texture to be renderred
        img = bpy.data.images[sc.tex_image]

        # OpenGL configuration
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        if img.bindcode:
            bind = img.bindcode
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, bind)
            bgl.glTexParameteri(
                bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)
            bgl.glTexParameteri(
                bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
            bgl.glTexEnvi(
                bgl.GL_TEXTURE_ENV, bgl.GL_TEXTURE_ENV_MODE, bgl.GL_MODULATE)
        
        # render texture
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glColor4f(1.0, 1.0, 1.0, sc.tex_transparency)
        for (v1, v2), (u, v) in zip(positions, tex_coords):
            bgl.glTexCoord2f(u, v)
            bgl.glVertex2f(v1, v2)
        bgl.glEnd()


class TPStartTextureProjection(bpy.types.Operator):
    """Start Texture Projection"""
    
    bl_idname = "uv.tp_start_texture_projection"
    bl_label = "Start Texture Projection"
    bl_description = "Start Texture Projection."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tp_props
        if props.running is False:
            TPTextureRenderer.handle_add(self, context)
            props.running = True
        if context.area:
            context.area.tag_redraw()
        return {'FINISHED'}


class TPStopTextureProjection(bpy.types.Operator):
    """Stop Texture Projection"""
    
    bl_idname = "uv.tp_stop_texture_projection"
    bl_label = "Stop Texture Projection"
    bl_description = "Stop Texture Projection."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.tp_props
        if props.running is True:
            TPTextureRenderer.handle_remove(self, context)
            props.running = False
        if context.area:
            context.area.tag_redraw()
        return {'FINISHED'}


class TPProjectTexture(bpy.types.Operator):
    """Project texture."""
    
    bl_idname = "uv.tp_project_texture"
    bl_label = "Project Texture"
    bl_description = "Project Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mem = View3DModeMemory()
        sc = context.scene
        
        try:
            if sc.tex_image == "None":
                raise TPError({'WARNING'}, "You must select texture.")
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    break
            else:
                raise TPError(
                    {'WARNING'}, "Could not find any 'VIEW_3D' areas.")
            for region in area.regions:
                if region.type == 'WINDOW':
                    break
            else:
                raise TPError(
                    {'WARNING'}, "Could not find any 'WINDOW' regions.")
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    break
            else:
                raise TPError(
                    {'WARNING'}, "Could not find any 'VIEW_3D' spaces.")
            
            # get faces to be texture projected
            obj = bpy.context.active_object
            world_mat = obj.matrix_world
            sel_faces = get_selected_faces(obj)
            # transform 3d space to screen region
            for f in sel_faces:
                for v in f.vertices:
                    f.loc.append(view3d_utils.location_3d_to_region_2d(
                        region,
                        space.region_3d,
                        world_mat * obj.data.vertices[v].co
                        ))
            # transform screen region to canvas
            for f in sel_faces:
                for l in f.loc:
                    f.loc_on_canvas.append(region_to_canvas(
                        region, l,
                        get_canvas(bpy.context, sc.tex_magnitude)))
            # project texture to object
            mem.change_mode('OBJECT')
            uv = obj.data.uv_layers[obj.data.uv_layers.active.name]
            tex = obj.data.uv_textures[obj.data.uv_textures.active.name]
            for f in sel_faces:
                tex.data[f.face_index].image = bpy.data.images[sc.tex_image]
                for l, i in zip(f.loc_on_canvas, f.indices):
                    uv.data[i].uv = l.to_2d()
        except TPError as e:
            e.report(self)
            return {'CANCELLED'}

        return {'FINISHED'}


class TPMagnitudeUp(bpy.types.Operator):
    """Up texture magnitude."""
    
    bl_idname = "uv.tp_magnitude_up"
    bl_label = "Magnitude UP"
    bl_description = "Up texture magnitude"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.area:
            context.area.tag_redraw()
        sc = context.scene
        sc.tex_magnitude = sc.tex_magnitude + 0.1
        return {'FINISHED'}


class TPMagnitudeDown(bpy.types.Operator):
    """Down texture magnitude."""
    
    bl_idname = "uv.tp_magnitude_down"
    bl_label = "Magnitude DOWN"
    bl_description = "Down texture magnitude"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.area:
            context.area.tag_redraw()
        sc = context.scene
        sc.tex_magnitude = sc.tex_magnitude - 0.1
        return {'FINISHED'}


# master menu
class TPMenu(bpy.types.Menu):
    bl_idname = "uv.tp_menu"
    bl_label = "Texture Projection"
    bl_description = "Project texture menu"

    def draw(self, context):
        self.layout.operator(TPStartTextureProjection.bl_idname)
        self.layout.operator(TPProjectTexture.bl_idname)
        self.layout.operator(TPStopTextureProjection.bl_idname)


# UI view
class OBJECT_PT_TP(bpy.types.Panel):
    bl_label = "Texture Projection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        sc = context.scene
        layout = self.layout
        props = sc.tp_props
        if props.running:
            layout.label(text="Image: ")
            layout.prop(sc, "tex_image", text="")
            layout.prop(sc, "tex_magnitude", text="Magnitude")
            layout.prop(sc, "tex_transparency", text="Transparency")


def init_properties():
    sc = bpy.types.Scene
    sc.tp_props = PointerProperty(
        name="TP operation internal data",
        description="TP operation internal data",
        type=TPProperties)
    sc.tex_magnitude = FloatProperty(
        name="Magnitude",
        description="Texture Magnitude.",
        default=0.5,
        min=0.0,
        max=100.0)
    sc.tex_image = EnumProperty(
        name="Image",
        description="Texture Image.",
        items=SetTextureImageName)
    sc.tex_transparency = FloatProperty(
        name="Transparency",
        description="Texture Transparency.",
        default=0.2,
        min=0.0,
        max=1.0)


def clear_properties():
    sc = bpy.types.Scene
    del sc.tex_transparency
    del sc.tex_image
    del sc.tex_magnitude
    del sc.tp_props


# registration
def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(TPMenu.bl_idname)


def register():
    bpy.utils.register_module(__name__)
    init_properties()
    bpy.types.VIEW3D_MT_uv_map.append(menu_fn)
    # assign shortcut keys
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    key_assign_list = [
        (TPMagnitudeUp.bl_idname, "UP_ARROW", "PRESS", True, True, False),
        (TPMagnitudeDown.bl_idname, "DOWN_ARROW", "PRESS", True, True, False),
        (TPProjectTexture.bl_idname, "P", "PRESS", True, True, False),
        (TPStartTextureProjection.bl_idname, "S", "PRESS", True, True, False),
        (TPStopTextureProjection.bl_idname, "T", "PRESS", True, True, False)
        ]
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        for (idname, key, event, ctrl, alt, shift) in key_assign_list:
            kmi = km.keymap_items.new(
                idname, key, event, ctrl=ctrl, alt=alt, shift=shift)
            addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_module(__name__)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.types.VIEW3D_MT_uv_map.remove(menu_fn)
    clear_properties()


if __name__ == "__main__":
    register()
