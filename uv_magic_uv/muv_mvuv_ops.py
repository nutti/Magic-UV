__author__ = "kgeogeo, mem, Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.0"
__date__ = "14 May 2016"


import bpy
import bmesh
from bpy.app.handlers import persistent
from bpy_extras import view3d_utils
from mathutils import Vector


class MUV_MVUV(bpy.types.Operator):
    """
    Operator class: Move UV from View3D
    """

    bl_idname = "view3d.muv_mvuv"
    bl_label = "Move the UV from View3D"
    bl_options = {'REGISTER', 'UNDO'}
    
    __topology_dict = []
    __first_mouse = Vector((0.0, 0.0))
    __offset_uv = Vector((0.0, 0.0))
    __old_offset_uv = Vector((0.0, 0.0))
    __first_time = True
    __ini_uvs = []

    def __find_uv(self, context):
        bm = bmesh.from_edit_mesh(context.object.data)
        topology_dict = []
        first = True
        diff = 0
        uvs = []
        active_uv = bm.loops.layers.uv.active
        for fidx, f in enumerate(bm.faces):
            for vidx, v in enumerate(f.verts):
                if v.select:
                    uvs.append(f.loops[vidx][active_uv].uv.copy())
                    topology_dict.append([fidx, vidx])
                    if first:
                        v1 = v.link_loops[0].vert.co
                        sv1 = view3d_utils.location_3d_to_region_2d(
                            context.region,
                            context.space_data.region_3d,
                            v1)
                        v2 = v.link_loops[0].link_loop_next.vert.co
                        sv2 = view3d_utils.location_3d_to_region_2d(
                            context.region,
                            context.space_data.region_3d,
                            v2)
                        vres = sv2 - sv1
                        va = vres.angle(Vector((0.0, 1.0)))
                        
                        uv1 = v.link_loops[0][active_uv].uv
                        uv2 = v.link_loops[0].link_loop_next[active_uv].uv
                        uvres = uv2 - uv1
                        uva = uvres.angle(Vector((0.0,1.0)))
                        diff = uva - va
                        first = False
                        
        return topology_dict, uvs 
   
    @classmethod
    def poll(cls, context):
        return (context.edit_object)

    def modal(self, context, event):
        if self.__first_time is True:
            self.__first_mouse = Vector((
                event.mouse_region_x, event.mouse_region_y))  
            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self.__first_time = False
            return {'RUNNING_MODAL'}

        ob = context.object
        bm = bmesh.from_edit_mesh(ob.data)             
        div = 10000
        self.__offset_uv += Vector((
            (event.mouse_region_x - self.__first_mouse.x) / div,
            (event.mouse_region_y - self.__first_mouse.y) / div))
        active_uv = bm.loops.layers.uv.active
        
        o = self.__offset_uv
        oo = self.__old_offset_uv
        for fidx, vidx in self.__topology_dict:
            d = bm.faces[fidx].loops[vidx][active_uv]
            vec = Vector((o.x - o.y, o.x + o.y))
            d.uv = d.uv - Vector((oo.x , oo.y)) + vec  
        
        self.__old_offset_uv = vec      
        self.__first_mouse = Vector((
            event.mouse_region_x, event.mouse_region_y))        
        ob.data.update()

        if context.user_preferences.inputs.select_mouse == 'RIGHT':
            confirm_btn = 'LEFTMOUSE'
            cancel_btn = 'RIGHTMOUSE'
        else:
            confirm_btn = 'RIGHTMOUSE'
            cancel_btn = 'LEFTMOUSE'

        if event.type == cancel_btn and event.value == 'PRESS':
            for (fidx, vidx), uv in zip(self.__topology_dict, self.__ini_uvs):
                bm.faces[fidx].loops[vidx][active_uv].uv = uv
            return {'FINISHED'} 
        if event.type == confirm_btn and event.value == 'PRESS':
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.__first_time = True
        context.window_manager.modal_handler_add(self)
        self.__topology_dict, self.__ini_uvs = self.__find_uv(context) 
        return {'RUNNING_MODAL'}  

