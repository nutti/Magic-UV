import sys

DEBUGGING = True

def start_debug():
    PYDEV_SRC_DIR = 'C:\\Tools\\adt-bundle-windows-x86_64-20140624\\eclipse\\plugins\\org.python.pydev_3.9.2.201502050007\\pysrc'
    if PYDEV_SRC_DIR not in sys.path:
        sys.path.append(PYDEV_SRC_DIR)
    import pydevd
    pydevd.settrace()
    print("started blender script debugging...")