# SPDX-License-Identifier: GPL-2.0-or-later

if "bpy" in locals():
    import importlib
    # pylint: disable=E0601
    importlib.reload(shader)
    importlib.reload(imm)
else:
    from . import shader
    from . import imm

# pylint: disable=C0413
import bpy
