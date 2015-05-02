import sys

DEBUGGING = False

def start_debug():
    if DEBUGGING is False:
        return
    
    PYDEV_SRC_DIR = 'XXXXXX\\eclipse\\plugins\\org.python.pydev_3.9.2.201502050007\\pysrc'
    if PYDEV_SRC_DIR not in sys.path:
        sys.path.append(PYDEV_SRC_DIR)
    import pydevd
    pydevd.settrace()
    print("started blender script debugging...")