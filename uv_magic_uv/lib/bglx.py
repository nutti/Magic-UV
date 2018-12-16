from threading import Lock

import gpu
from gpu_extras.batch import batch_for_shader

GL_LINES = 0
GL_LINE_STRIP = 1
GL_TRIANGLES = 5
GL_QUADS = 4

class InternalData:
    __inst = None
    __lock = Lock()

    def __init__(self):
        raise NotImplementedError("Not allowed to call constructor")

    @classmethod
    def __internal_new(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls.__inst:
            with cls.__lock:
                if not cls.__inst:
                    cls.__inst = cls.__internal_new()

        return cls.__inst

    def init(self):
        self.clear()

    def set_prim_mode(self, mode):
        self.prim_mode = mode

    def set_dims(self, dims):
        self.dims = dims

    def add_vert(self, v):
        self.verts.append(v)

    def set_color(self, c):
        self.color = c

    def clear(self):
        self.prim_mode = None
        self.verts = []
        self.dims = None

    def get_verts(self):
        return self.verts

    def get_dims(self):
        return self.dims

    def get_prim_mode(self):
        return self.prim_mode

    def get_color(self):
        return self.color


def glBegin(mode):
    inst = InternalData.get_instance()
    inst.init()
    inst.set_prim_mode(mode)


def glColor4f(r, g, b, a):
    inst = InternalData.get_instance()
    inst.set_color([r, g, b, a])


def glEnd():
    inst = InternalData.get_instance()

    color = inst.get_color()
    coords = inst.get_verts()
    if inst.get_dims() == 2:
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    else:
        raise NotImplemented("get_dims() != 2")


    if inst.get_prim_mode() == GL_LINES:
        indices = []
        for i in range(0, len(coords), 2):
            indices.append([i, i + 1])
        batch = batch_for_shader(shader, 'LINES', {"pos": coords},
                                 indices=indices)

    elif inst.get_prim_mode() == GL_LINE_STRIP:
        batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": coords})

    elif inst.get_prim_mode() == GL_TRIANGLES:
        indices = []
        for i in range(0, len(coords), 3):
            indices.append([i, i + 1, i + 2])
        batch = batch_for_shader(shader, 'TRIS', {"pos": coords},
                                 indices=indices)

    elif inst.get_prim_mode() == GL_QUADS:
        indices = []
        for i in range(0, len(coords), 4):
            indices.append([i, i + 1, i + 2, i +3])
        batch = batch_for_shader(shader, 'TRIS', {"pos": coords},
                                 indices=indices)
    else:
        raise NotImplemented("get_prim_mode() != (GL_LINES|GL_TRIANGLES)")

    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

    inst.clear()


def glVertex2f(x, y):
    inst = InternalData.get_instance()
    inst.add_vert([x, y])
    inst.set_dims(2)


