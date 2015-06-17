import unittest
import bpy
import bmesh

class TestCPUV(unittest.TestCase):
	
	src_obj = "Cube_src"
	dest_obj = "Cube_dest"

	def test_addon_enabled(self):
		self.assertIsNotNone(bpy.ops.uv.muv_cpuv_copy_uv)
		self.assertIsNotNone(bpy.ops.uv.muv_copy_paste_uv)
	
	def test_copy_uv(self):
		mode_orig = bpy.context.object.mode
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.context.scene.objects.active = bpy.data.objects[self.src_obj]
		active_obj = bpy.context.scene.objects.active
		bm = bmesh.from_edit_mesh(active_obj.data)

		result = bpy.ops.uv.muv_cpuv_copy_uv()
		self.assertSetEqual(result, {'CANCELLED'})
		
		bpy.ops.mesh.uv_texture_add()
		bpy.ops.mesh.select_all(action='DESELECT')
		result = bpy.ops.uv.muv_cpuv_copy_uv()
		self.assertSetEqual(result, {'CANCELLED'})

		bpy.ops.mesh.select_all(action='SELECT')
		result = bpy.ops.uv.muv_cpuv_copy_uv()
		self.assertSetEqual(result, {'FINISHED'})

		bpy.ops.object.mode_set(mode=mode_orig)



suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCPUV)
unittest.TextTestRunner().run(suite)

