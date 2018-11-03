import sys
import unittest

def test_main():
    import os
    path = os.path.dirname(__file__)
    sys.path.append(path)

    import uv_magic_uv_test

    test_cases = [
        uv_magic_uv_test.align_uv_test.TestAlignUVCircle,
        uv_magic_uv_test.align_uv_test.TestAlignUVStraighten,
        uv_magic_uv_test.align_uv_test.TestAlignUVAxis,
        uv_magic_uv_test.align_uv_cursor_test.TestAlignUVCursor,
        uv_magic_uv_test.copy_paste_uv_test.TestCopyPasteUV,
        uv_magic_uv_test.copy_paste_uv_test.TestCopyPasteUVSelseq,
        uv_magic_uv_test.copy_paste_uv_object_test.TestCopyPasteUVObject,
        uv_magic_uv_test.copy_paste_uv_uvedit_test.TestCopyPasteUVUVEdit,
        uv_magic_uv_test.flip_rotate_uv_test.TestFlipRotateUV,
        uv_magic_uv_test.mirror_uv_test.TestMirrorUV,
        uv_magic_uv_test.move_uv_test.TestMoveUV,
        uv_magic_uv_test.pack_uv_test.TestPackUV,
        uv_magic_uv_test.preserve_uv_aspect_test.TestPreserveUVAspect,
        uv_magic_uv_test.select_uv_test.TestSelectUVOverlapped,
        uv_magic_uv_test.select_uv_test.TestSelectUVFlipped,
        uv_magic_uv_test.smooth_uv_test.TestSmoothUV,
        uv_magic_uv_test.texture_lock_test.TestTextureLock,
        uv_magic_uv_test.texture_projection_test.TestTextureProjection,
        uv_magic_uv_test.texture_wrap_test.TestTextureWrap,
        uv_magic_uv_test.transfer_uv_test.TestTransferUV,
        uv_magic_uv_test.unwrap_constraint_test.TestUnwrapConstraint,
        uv_magic_uv_test.uv_bounding_box_test.TestUVBoundingBox,
        uv_magic_uv_test.uv_inspection_test.TestUVInspection,
        uv_magic_uv_test.uv_sculpt_test.TestUVSculpt,
        uv_magic_uv_test.uvw_test.TestUVWBox,
        uv_magic_uv_test.uvw_test.TestUVWBestPlaner,
        uv_magic_uv_test.world_scale_uv_test.TestWorldScaleUVMeasure,
        uv_magic_uv_test.world_scale_uv_test.TestWorldScaleUVApplyManual,
        uv_magic_uv_test.world_scale_uv_test.TestWorldScaleUVApplyScalingDensity,
        uv_magic_uv_test.world_scale_uv_test.TestWorldScaleUVProportionalToMesh,
    ]

    suite = unittest.TestSuite()
    for case in test_cases:
        suite.addTest(unittest.makeSuite(case))
    ret = unittest.TextTestRunner().run(suite).wasSuccessful()
    sys.exit(not ret)


if __name__ == "__main__":
    test_main()
