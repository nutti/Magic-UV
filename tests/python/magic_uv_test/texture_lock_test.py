import bpy

from . import common


class TestTextureLock(common.TestBase):
    module_name = "texture_lock"
    submodule_name = "non_intr"
    idname = [
        # Texture Lock
        ('OPERATOR', 'uv.muv_texture_lock_lock'),
        ('OPERATOR', 'uv.muv_texture_lock_unlock'),
    ]

    # can not test interactive mode
    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='EDIT')

    def test_lock_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV (Lock)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_texture_lock_lock()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_unlock_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV (Unlock)")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_texture_lock_unlock()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_lock_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.image.new(name='Test')
        result = bpy.ops.uv.muv_texture_lock_lock()
        self.assertSetEqual(result, {'FINISHED'})

        result = bpy.ops.uv.muv_texture_lock_unlock()
        self.assertSetEqual(result, {'FINISHED'})

    def test_lock_ok_with_connect(self):
        print("[TEST] (OK) With connect")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.image.new(name='Test')
        bpy.ops.uv.smart_project()    # this needs because previous result corrupts UV and arise errors
        result = bpy.ops.uv.muv_texture_lock_lock()
        self.assertSetEqual(result, {'FINISHED'})

        result = bpy.ops.uv.muv_texture_lock_unlock(
            connect=False
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestTextureLockIntr(common.TestBase):
    module_name = "texture_lock"
    submodule_name = "intr"
    idname = [
        # Texture Lock
        ('OPERATOR', 'uv.muv_texture_lock_intr'),
    ]

    # modal operator can not invoke directly from cmdline
    def test_nothing(self):
        pass
