# SPDX-License-Identifier: GPL-2.0-or-later

import os
import gpu


class ShaderManager:
    shader_instances = {}

    SHADER_FILES = {
        'IMAGE_COLOR': {
            "vertex": "image_color_vert.glsl",
            "fragment": "image_color_frag.glsl",
        },
        'IMAGE_COLOR_SCISSOR': {
            "vertex": "image_color_vert.glsl",
            "fragment": "image_color_scissor_frag.glsl",
        },
        'UNIFORM_COLOR_SCISSOR': {
            "vertex": "uniform_color_scissor_vert.glsl",
            "fragment": "uniform_color_scissor_frag.glsl",
        },
        'POLYLINE_UNIFORM_COLOR_SCISSOR': {
            "vertex": "polyline_uniform_color_scissor_vert.glsl",
            "fragment": "polyline_uniform_color_scissor_frag.glsl",
            "geometry": "polyline_uniform_color_scissor_geom.glsl",
        },
    }

    @classmethod
    def register_shaders(cls):
        if gpu.platform.backend_type_get() != 'OPENGL':
            return

        for shader_name, shader_files in cls.SHADER_FILES.items():
            vert_code = None
            frag_code = None
            geom_code = None
            for category, filename in shader_files.items():
                filepath = f"{os.path.dirname(__file__)}/shaders/{filename}"
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()

                if category == "vertex":
                    vert_code = code
                elif category == "fragment":
                    frag_code = code
                elif category == 'geometry':
                    geom_code = code
            if geom_code is not None:
                instance = gpu.types.GPUShader(
                    vert_code, frag_code, geocode=geom_code)
            else:
                instance = gpu.types.GPUShader(vert_code, frag_code)
            cls.shader_instances[shader_name] = instance

    @classmethod
    def unregister_shaders(cls):
        if gpu.platform.backend_type_get() != 'OPENGL':
            return

        for instance in cls.shader_instances.values():
            del instance
        cls.shader_instances = {}

    @classmethod
    def get_shader(cls, shader_name):
        if gpu.platform.backend_type_get() != 'OPENGL':
            return None

        return cls.shader_instances[shader_name]
