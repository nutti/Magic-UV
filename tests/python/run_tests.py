import sys
import unittest

def test_main():
    import os
    path = os.path.dirname(__file__)
    sys.path.append(path)

    import magic_uv_test

    test_cases = [
        magic_uv_test.align_uv_test.TestAlignUVCircle,
        magic_uv_test.align_uv_test.TestAlignUVStraighten,
        magic_uv_test.align_uv_test.TestAlignUVAxis,
        magic_uv_test.align_uv_cursor_test.TestAlignUVCursor,
        magic_uv_test.clip_uv_test.TestClipUV,
        magic_uv_test.copy_paste_uv_test.TestCopyPasteUV,
        magic_uv_test.copy_paste_uv_test.TestCopyPasteUVSelseq,
        magic_uv_test.copy_paste_uv_object_test.TestCopyPasteUVObject,
        magic_uv_test.copy_paste_uv_uvedit_test.TestCopyPasteUVUVEdit,
        magic_uv_test.flip_rotate_uv_test.TestFlipRotateUV,
        magic_uv_test.mirror_uv_test.TestMirrorUV,
        magic_uv_test.move_uv_test.TestMoveUV,
        magic_uv_test.pack_uv_test.TestPackUV,
        magic_uv_test.preserve_uv_aspect_test.TestPreserveUVAspect,
        magic_uv_test.select_uv_test.TestSelectUVOverlapped,
        magic_uv_test.select_uv_test.TestSelectUVFlipped,
        magic_uv_test.smooth_uv_test.TestSmoothUV,
        magic_uv_test.texture_lock_test.TestTextureLock,
        magic_uv_test.texture_projection_test.TestTextureProjection,
        magic_uv_test.texture_wrap_test.TestTextureWrap,
        magic_uv_test.transfer_uv_test.TestTransferUV,
        magic_uv_test.unwrap_constraint_test.TestUnwrapConstraint,
        magic_uv_test.uv_bounding_box_test.TestUVBoundingBox,
        magic_uv_test.uv_inspection_test.TestUVInspection,
        magic_uv_test.uv_sculpt_test.TestUVSculpt,
        magic_uv_test.uvw_test.TestUVWBox,
        magic_uv_test.uvw_test.TestUVWBestPlaner,
        magic_uv_test.world_scale_uv_test.TestWorldScaleUVMeasure,
        magic_uv_test.world_scale_uv_test.TestWorldScaleUVApplyManual,
        magic_uv_test.world_scale_uv_test.TestWorldScaleUVApplyScalingDensity,
        magic_uv_test.world_scale_uv_test.TestWorldScaleUVProportionalToMesh,
    ]

    suite = unittest.TestSuite()
    for case in test_cases:
        suite.addTest(unittest.makeSuite(case))
    ret = unittest.TextTestRunner().run(suite).wasSuccessful()
    sys.exit(not ret)


if __name__ == "__main__":
    test_main()
