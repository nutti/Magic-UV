import unittest

import bpy
import bmesh

from . import common
from . import compatibility as compat


class TestAlignUVCircle(common.TestBase):
    module_name = "align_uv"
    submodule_name = "circle"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_circle'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass


class TestAlignUVStraighten(common.TestBase):
    module_name = "align_uv"
    submodule_name = "straighten"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_straighten'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass


class TestAlignUVAxis(common.TestBase):
    module_name = "align_uv"
    submodule_name = "axis"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_axis'),
    ]

    # Align UV has a complicated condition to test
    def test_nothing(self):
        pass


class TestAlignUVSnapSetPointTargetToCursor(common.TestBase):
    module_name = "align_uv"
    submodule_name = "snap_set_point_target_to_cursor"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_snap_set_point_target_to_cursor'),
    ]

    # It is impossible to get cursor_location from the console.
    def test_nothing(self):
        pass


class TestAlignUVSnapSetPointTargetToVertexGroup(common.TestBase):
    module_name = "align_uv"
    submodule_name = "snap_set_point_target_to_vertex_group"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_snap_set_point_target_to_vertex_group'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.context.scene.tool_settings.use_uv_select_sync = True

    def tearDownEachMethod(self):
        bpy.context.scene.tool_settings.use_uv_select_sync = False

    def test_ok(self):
        print("[TEST] (OK)")

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_align_uv_snap_set_point_target_to_vertex_group()
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

        result = bpy.ops.uv.muv_align_uv_snap_set_point_target_to_vertex_group()
        self.assertSetEqual(result, {'FINISHED'})


class TestAlignUVSnapToPoint(common.TestBase):
    module_name = "align_uv"
    submodule_name = "snap_to_point"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_snap_to_point'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.context.scene.tool_settings.use_uv_select_sync = True

    def tearDownEachMethod(self):
        bpy.context.scene.tool_settings.use_uv_select_sync = False

    def test_ng_no_vertex(self):
        print("[TEST] (NG) Vertex")

        # Warning: Must select more than 1 Vertex.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='VERT')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_face(self):
        print("[TEST] (NG) Face")

        # Warning: Must select more than 1 Face.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(
            group='FACE', target=(0.5, 0.5))
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_uv_island(self):
        print("[TEST] (NG) UV Island")

        # Warning: Must select more than 1 UV Island.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='UV_ISLAND')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_vertex(self):
        print("[TEST] (OK) Vertex")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bm.faces[0].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='VERT')
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_face(self):
        print("[TEST] (OK) Face")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bm.faces[0].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(
            group='FACE', target=(0.5, 0.5))
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_uv_island(self):
        print("[TEST] (OK) UV Island")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bm.faces[0].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='UV_ISLAND')
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_vertex(self):
        print("[TEST] (OK) Multiple Objects - Vertex")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                f.select = False
            bm.faces[0].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='VERT')
        self.assertSetEqual(result, {'FINISHED'})


    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_face(self):
        print("[TEST] (OK) Multiple Objects - Face")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                f.select = False
            bm.faces[0].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_point(group='FACE')
        self.assertSetEqual(result, {'FINISHED'})


    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_uv_island(self):
        print("[TEST] (OK) Multiple Objects - UV Island")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                f.select = False
            bm.faces[0].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_point(
            group='UV_ISLAND', target=(0.5, 0.5))
        self.assertSetEqual(result, {'FINISHED'})


class TestAlignUVSnapSetEdgeTargetToEdgeCenter(common.TestBase):
    module_name = "align_uv"
    submodule_name = "snap_set_edge_target_to_edge_center"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_snap_set_edge_target_to_edge_center'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.context.scene.tool_settings.use_uv_select_sync = True

    def tearDownEachMethod(self):
        bpy.context.scene.tool_settings.use_uv_select_sync = False

    def test_ok(self):
        print("[TEST] (OK)")

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        result = bpy.ops.uv.muv_align_uv_snap_set_edge_target_to_edge_center()
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

        result = bpy.ops.uv.muv_align_uv_snap_set_edge_target_to_edge_center()
        self.assertSetEqual(result, {'FINISHED'})


class TestAlignUVSnapToEdge(common.TestBase):
    module_name = "align_uv"
    submodule_name = "snap_to_edge"
    idname = [
        ('OPERATOR', 'uv.muv_align_uv_snap_to_edge'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.context.scene.tool_settings.use_uv_select_sync = True

    def tearDownEachMethod(self):
        bpy.context.scene.tool_settings.use_uv_select_sync = False

    def test_ng_no_edge(self):
        print("[TEST] (NG) No selected edge")

        # Warning: Must select more than 1 Edge.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='EDGE')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_face(self):
        print("[TEST] (NG) No selected face")

        # Warning: Must select more than 1 Edge.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='FACE')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ng_no_uv_island(self):
        print("[TEST] (NG) No selected UV Island")

        # Warning: Must select more than 1 Edge.
        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select = False
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='UV_ISLAND')
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_edge(self):
        print("[TEST] (OK) Edge")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.verify()
        bm.edges.ensure_lookup_table()
        for e in bm.edges:
            e.select = False
        bm.edges[0].select = True
        bm.edges[0].link_loops[0][uv_layer].select = True
        bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='EDGE')
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_face(self):
        print("[TEST] (OK) Face")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.verify()
        bm.edges.ensure_lookup_table()
        for e in bm.edges:
            e.select = False
        bm.edges[0].select = True
        bm.edges[0].link_loops[0][uv_layer].select = True
        bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(
            group='FACE', target_1=(0.2, 0.1), target_2=(0.4, 0.6))
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_uv_island(self):
        print("[TEST] (OK) UV Island")

        obj = compat.get_active_object(bpy.context)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()

        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.verify()
        bm.edges.ensure_lookup_table()
        for e in bm.edges:
            e.select = False
        bm.edges[0].select = True
        bm.edges[0].link_loops[0][uv_layer].select = True
        bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
        bmesh.update_edit_mesh(obj.data)

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='UV_ISLAND')
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_edge(self):
        print("[TEST] (OK) Multiple Objects - Edge")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()
            bm.edges.ensure_lookup_table()
            for e in bm.edges:
                e.select = False
            bm.edges[0].select = True
            bm.edges[0].link_loops[0][uv_layer].select = True
            bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='EDGE')
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_face(self):
        print("[TEST] (OK) Multiple Objects - Face")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()
            bm.edges.ensure_lookup_table()
            for e in bm.edges:
                e.select = False
            bm.edges[0].select = True
            bm.edges[0].link_loops[0][uv_layer].select = True
            bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(group='FACE')
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects_uv_island(self):
        print("[TEST] (OK) Multiple Objects - UV Island")

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

            obj = compat.get_active_object(bpy.context)
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()
            bm.edges.ensure_lookup_table()
            for e in bm.edges:
                e.select = False
            bm.edges[0].select = True
            bm.edges[0].link_loops[0][uv_layer].select = True
            bm.edges[0].link_loops[0].link_loop_next[uv_layer].select = True
            bmesh.update_edit_mesh(obj.data)

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_align_uv_snap_to_edge(
            group='UV_ISLAND', target_1=(0.2, 0.1), target_2=(0.4, 0.6))
        self.assertSetEqual(result, {'FINISHED'})
