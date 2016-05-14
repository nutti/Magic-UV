import sys
import subprocess

blender_path = 'blender'

if len(sys.argv) != 2:
	exit(-1)

blender_path = sys.argv[1]

testset_path = 'tests/'
uv_magic_uv_path = 'uv_magic_uv/'
src_file = testset_path + uv_magic_uv_path + 'cpuv.py'

subprocess.call([blender_path, '--addons', 'uv_magic_uv', '--factory-startup', '-noaudio', '-b', '--python', src_file])

