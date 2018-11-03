import bpy

from . import common


class TestSelectUVOverlapped(common.TestBase):
    module_name = "select_uv"
    submodule_name = "overlapped"
    idname = [
        # Select UV
        ('OPERATOR', 'uv.muv_select_uv_operator_select_overlapped'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=True")
        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_operator_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_no_select_sync(self):
        print("[TEST] (OK) Select Overlapped with UV_Select_Sync=False")
        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_operator_select_overlapped()
        self.assertSetEqual(result, {'FINISHED'})


class TestSelectUVFlipped(common.TestBase):
    module_name = "select_uv"
    submodule_name = "flipped"
    idname = [
        # Select UV
        ('OPERATOR', 'uv.muv_select_uv_operator_select_flipped'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ok_select_sync(self):
        print("[TEST] (OK) Select Flipped with UV_Select_Sync=True")
        bpy.context.tool_settings.use_uv_select_sync = True
        result = bpy.ops.uv.muv_select_uv_operator_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_no_select_sync(self):
        print("[TEST] (OK) Select Flipped with UV_Select_Sync=False")
        bpy.context.tool_settings.use_uv_select_sync = False
        result = bpy.ops.uv.muv_select_uv_operator_select_flipped()
        self.assertSetEqual(result, {'FINISHED'})
