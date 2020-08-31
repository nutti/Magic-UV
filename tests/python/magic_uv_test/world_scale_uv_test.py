import unittest

import bpy
import bmesh

from . import common
from . import compatibility as compat


class TestWorldScaleUVMeasure(common.TestBase):
    module_name = "world_scale_uv"
    submodule_name = "measure"
    idname = [
        # World Scale UV
        ('OPERATOR', 'uv.muv_world_scale_uv_measure'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map and texture
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_measure()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_texture(self):
        print("[TEST] (NG) No Texture")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_measure()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        common.assign_new_image(self.active_obj, "Test")
        result = bpy.ops.uv.muv_world_scale_uv_measure()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User Specified")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        common.assign_new_image(self.active_obj, "Test")
        result = bpy.ops.uv.muv_world_scale_uv_measure(
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestWorldScaleUVApplyManual(common.TestBase):
    module_name = "world_scale_uv"
    submodule_name = "manual"
    idname = [
        # World Scale UV
        ('OPERATOR', 'uv.muv_world_scale_uv_apply_manual'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map and texture
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_manual()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_manual()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_world_scale_uv_apply_manual(
            tgt_density=0.5,
            tgt_texture_size=(2048, 2048),
            origin='CENTER',
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] (OK) Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_world_scale_uv_apply_manual(
            tgt_density=0.5,
            tgt_texture_size=(2048, 2048),
            origin='CENTER',
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestWorldScaleUVApplyScalingDensity(common.TestBase):
    module_name = "world_scale_uv"
    submodule_name = "scaling_density"
    idname = [
        # World Scale UV
        ('OPERATOR', 'uv.muv_world_scale_uv_apply_scaling_density'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map and texture
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_texture(self):
        print("[TEST] (NG) No Texture")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density()
        self.assertSetEqual(result, {'CANCELLED'})

    def __prepare_apply_test(self):
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        common.assign_new_image(self.active_obj, "Test")

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_apply_test()
        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_1(self):
        print("[TEST] (OK) User specified 1")
        self.__prepare_apply_test()
        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density(
            tgt_scaling_factor=0.5,
            origin='RIGHT_TOP',
            src_density=0.5,
            same_density=False
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_2(self):
        print("[TEST] (OK) User specified 2")
        self.__prepare_apply_test()
        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density(
            tgt_scaling_factor=0.8,
            origin='CENTER',
            src_density=1.5,
            same_density=True,
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] (OK) Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')
            common.assign_new_image(bpy.data.objects[name], "Test")

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_world_scale_uv_apply_scaling_density(
            tgt_scaling_factor=0.8,
            origin='CENTER',
            src_density=1.5,
            same_density=True,
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})


class TestWorldScaleUVProportionalToMesh(common.TestBase):
    module_name = "world_scale_uv"
    submodule_name = "proportional_to_mesh"
    idname = [
        # World Scale UV
        ('OPERATOR', 'uv.muv_world_scale_uv_apply_proportional_to_mesh'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        self.active_obj = compat.get_active_object(bpy.context)
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map and texture
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_proportional_to_mesh()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_texture(self):
        print("[TEST] (NG) No Texture")
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_world_scale_uv_apply_proportional_to_mesh()
        self.assertSetEqual(result, {'CANCELLED'})

    def __prepare_apply_test(self):
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.mesh.select_all(action='SELECT')
        common.assign_new_image(self.active_obj, "Test")

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        self.__prepare_apply_test()
        result = bpy.ops.uv.muv_world_scale_uv_apply_proportional_to_mesh(
            src_mesh_area=1.0
        )
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified(self):
        print("[TEST] (OK) User specified")
        self.__prepare_apply_test()
        result = bpy.ops.uv.muv_world_scale_uv_apply_proportional_to_mesh(
            origin='LEFT_TOP',
            src_density=0.3,
            src_uv_area=1.3,
            src_mesh_area=189.1,
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] (OK) Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')
            common.assign_new_image(bpy.data.objects[name], "Test")

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_world_scale_uv_apply_proportional_to_mesh(
            origin='LEFT_TOP',
            src_density=0.3,
            src_uv_area=1.3,
            src_mesh_area=189.1,
            tgt_area_calc_method='UV ISLAND',
            only_selected=True
        )
        self.assertSetEqual(result, {'FINISHED'})
