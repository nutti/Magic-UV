# <pep8-80 compliant>

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

__author__ = "imdjs, Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "4.5"
__date__ = "19 Nov 2017"

import math
from math import atan2, tan, sin, cos

import bpy
import bmesh
from mathutils import Vector
from bpy.props import EnumProperty, BoolProperty, FloatProperty

from . import muv_common


# get selected loop pair whose loops are connected each other
def get_loop_pairs(l, uv_layer):

    def __get_loop_pairs(l_, pairs_, uv_layer_, parsed_):
        parsed_.append(l_)
        for ll in l_.vert.link_loops:
            # forward direction
            lln = ll.link_loop_next
            # if there is same pair, skip it
            found = False
            for p in pairs_:
                if (ll in p) and (lln in p):
                    found = True
                    break
            # two loops must be selected
            if ll[uv_layer_].select and lln[uv_layer_].select:
                if not found:
                    pairs_.append([ll, lln])
                if lln not in parsed_:
                    __get_loop_pairs(lln, pairs_, uv_layer_, parsed_)

            # backward direction
            llp = ll.link_loop_prev
            # if there is same pair, skip it
            found = False
            for p in pairs_:
                if (ll in p) and (llp in p):
                    found = True
                    break
            # two loops must be selected
            if ll[uv_layer_].select and llp[uv_layer_].select:
                if not found:
                    pairs_.append([ll, llp])
                if llp not in parsed_:
                    __get_loop_pairs(llp, pairs_, uv_layer_, parsed_)

    pairs = []
    parsed = []
    __get_loop_pairs(l, pairs, uv_layer, parsed)

    return pairs


# sort pair by vertex
# (v0, v1) - (v1, v2) - (v2, v3) ....
def sort_loop_pairs(uv_layer, pairs, closed):
    rest = pairs
    sorted_pairs = [rest[0]]
    rest.remove(rest[0])

    # prepend
    while True:
        p1 = sorted_pairs[0]
        for p2 in rest:
            if p1[0].vert == p2[0].vert:
                sorted_pairs.insert(0, [p2[1], p2[0]])
                rest.remove(p2)
                break
            elif p1[0].vert == p2[1].vert:
                sorted_pairs.insert(0, [p2[0], p2[1]])
                rest.remove(p2)
                break
        else:
            break

    # append
    while True:
        p1 = sorted_pairs[-1]
        for p2 in rest:
            if p1[1].vert == p2[0].vert:
                sorted_pairs.append([p2[0], p2[1]])
                rest.remove(p2)
                break
            elif p1[1].vert == p2[1].vert:
                sorted_pairs.append([p2[1], p2[0]])
                rest.remove(p2)
                break
        else:
            break

    begin_vert = sorted_pairs[0][0].vert
    end_vert = sorted_pairs[-1][-1].vert
    if begin_vert != end_vert:
        return sorted_pairs, ""
    if closed and (begin_vert == end_vert):
        # if the sequence of UV is circular, it is ok
        return sorted_pairs, ""

    # if the begin vertex and the end vertex are same, search the UVs which
    # are separated each other
    tmp_pairs = sorted_pairs
    for i, (p1, p2) in enumerate(zip(tmp_pairs[:-1], tmp_pairs[1:])):
        diff = p2[0][uv_layer].uv - p1[-1][uv_layer].uv
        if diff.length > 0.000000001:
            # UVs are separated
            sorted_pairs = tmp_pairs[i+1:]
            sorted_pairs.extend(tmp_pairs[:i+1])
            break
    else:
        p1 = tmp_pairs[0]
        p2 = tmp_pairs[-1]
        diff = p2[-1][uv_layer].uv - p1[0][uv_layer].uv
        if diff.length < 0.000000001:
            # all UVs are not separated
            return None, "All UVs are not separted"

    return sorted_pairs, ""


# x ---- x   <- next_loop_pair
# |      |
# o ---- o   <- pair
def get_next_loop_pair(pair):
    lp = pair[0].link_loop_prev
    if lp.vert == pair[1].vert:
        lp = pair[0].link_loop_next
        if lp.vert == pair[1].vert:
            # no loop is found
            return None

    ln = pair[1].link_loop_next
    if ln.vert == pair[0].vert:
        ln = pair[1].link_loop_prev
        if ln.vert == pair[0].vert:
            # no loop is found
            return None

    # tri-face
    if lp == ln:
        return [lp]

    # quad-face
    return [lp, ln]


# | ---- |
# % ---- %   <- next_poly_loop_pair
# x ---- x   <- next_loop_pair
# |      |
# o ---- o   <- pair
def get_next_poly_loop_pair(pair):
    v1 = pair[0].vert
    v2 = pair[1].vert
    for l1 in v1.link_loops:
        if l1 == pair[0]:
            continue
        for l2 in v2.link_loops:
            if l2 == pair[1]:
                continue
            if l1.link_loop_next == l2:
                return [l1, l2]
            elif l1.link_loop_prev == l2:
                return [l1, l2]

    # no next poly loop is found
    return None


# get index of the island group which includes loop
def get_island_group_include_loop(loop, island_info):
    for i, isl in enumerate(island_info):
        for f in isl['faces']:
            for l in f['face'].loops:
                if l == loop:
                    return i    # found

    return -1   # not found


# get index of the island group which includes pair.
# if island group is not same between loops, it will be invalid
def get_island_group_include_pair(pair, island_info):
    l1_grp = get_island_group_include_loop(pair[0], island_info)
    if l1_grp == -1:
        return -1   # not found

    for p in pair[1:]:
        l2_grp = get_island_group_include_loop(p, island_info)
        if (l2_grp == -1) or (l1_grp != l2_grp):
            return -1   # not found or invalid

    return l1_grp


# get loop sequence in the same island
def get_loop_sequence_internal(uv_layer, pairs, island_info, closed):
    loop_sequences = []
    for i, pair in enumerate(pairs):
        seqs = [pair]
        p = pair
        isl_grp = get_island_group_include_pair(pair, island_info)
        if isl_grp == -1:
            return None, "Can not find the island or invalid island"

        while True:
            nlp = get_next_loop_pair(p)
            if not nlp:
                break       # no more loop pair
            nlp_isl_grp = get_island_group_include_pair(nlp, island_info)
            if nlp_isl_grp != isl_grp:
                break       # another island
            for nlpl in nlp:
                if nlpl[uv_layer].select:
                    return None, \
                           "Do not select UV which does not belong to " \
                           "the end edge"

            seqs.append(nlp)

            # when face is triangle, it indicates CLOSED
            if (len(nlp) == 1) and closed:
                break

            nplp = get_next_poly_loop_pair(nlp)
            if not nplp:
                break       # no more loop pair
            nplp_isl_grp = get_island_group_include_pair(nplp, island_info)
            if nplp_isl_grp != isl_grp:
                break       # another island

            # check if the UVs are already parsed.
            # this check is needed for the mesh which has the circular
            # sequence of the verticies
            matched = False
            for p1 in seqs:
                p2 = nplp
                if ((p1[0] == p2[0]) and (p1[1] == p2[1])) or \
                   ((p1[0] == p2[1]) and (p1[1] == p2[0])):
                    matched = True
            if matched:
                muv_common.debug_print("This is a circular sequence")
                break

            for nlpl in nplp:
                if nlpl[uv_layer].select:
                    return None, \
                           "Do not select UV which does not belong to " \
                           "the end edge"

            seqs.append(nplp)

            p = nplp

        loop_sequences.append(seqs)
    return loop_sequences, ""


def get_closed_loop_sequences(bm, uv_layer):
    sel_faces = [f for f in bm.faces if f.select]

    # get candidate loops
    cand_loops = []
    for f in sel_faces:
        for l in f.loops:
            if l[uv_layer].select:
                cand_loops.append(l)

    if len(cand_loops) < 2:
        return None, "More than 2 UVs must be selected"

    first_loop = cand_loops[0]
    isl_info = muv_common.get_island_info_from_bmesh(bm, False)
    loop_pairs = get_loop_pairs(first_loop, uv_layer)
    loop_pairs, err = sort_loop_pairs(uv_layer, loop_pairs, True)
    if not loop_pairs:
        return None, err
    loop_seqs, err = get_loop_sequence_internal(uv_layer, loop_pairs, isl_info,
                                                True)
    if not loop_seqs:
        return None, err

    return loop_seqs, ""


def get_loop_sequences(bm, uv_layer):
    sel_faces = [f for f in bm.faces if f.select]

    # get candidate loops
    cand_loops = []
    for f in sel_faces:
        for l in f.loops:
            if l[uv_layer].select:
                cand_loops.append(l)

    if len(cand_loops) < 2:
        return None, "More than 2 UVs must be selected"

    first_loop = cand_loops[0]
    isl_info = muv_common.get_island_info_from_bmesh(bm, False)
    loop_pairs = get_loop_pairs(first_loop, uv_layer)
    loop_pairs, err = sort_loop_pairs(uv_layer, loop_pairs, False)
    if not loop_pairs:
        return None, err
    loop_seqs, err = get_loop_sequence_internal(uv_layer, loop_pairs, isl_info,
                                                False)
    if not loop_seqs:
        return None, err

    return loop_seqs, ""


# get sum vertex length of loop sequences
def get_loop_vert_len(loops):
    length = 0
    for l1, l2 in zip(loops[:-1], loops[1:]):
        diff = l2.vert.co - l1.vert.co
        length = length + abs(diff.length)

    return length


# get sum uv length of loop sequences
def get_loop_uv_len(loops, uv_layer):
    length = 0
    for l1, l2 in zip(loops[:-1], loops[1:]):
        diff = l2[uv_layer].uv - l1[uv_layer].uv
        length = length + abs(diff.length)

    return length


# get center/radius of circle by 3 vertices
def get_circle(v):
    alpha = atan2((v[0].y - v[1].y), (v[0].x - v[1].x)) + math.pi / 2
    beta = atan2((v[1].y - v[2].y), (v[1].x - v[2].x)) + math.pi / 2
    ex = (v[0].x + v[1].x) / 2.0
    ey = (v[0].y + v[1].y) / 2.0
    fx = (v[1].x + v[2].x) / 2.0
    fy = (v[1].y + v[2].y) / 2.0
    cx = (ey - fy - ex * tan(alpha) + fx * tan(beta)) / (tan(beta) - tan(alpha))
    cy = ey - (ex - cx) * tan(alpha)
    center = Vector((cx, cy))

    r = v[0] - center
    radian = r.length

    return center, radian


# get position on circle with same arc length
def calc_v_on_circle(v, center, radius):
    base = v[0]
    theta = atan2(base.y - center.y, base.x - center.x)
    new_v = []
    for i, uv in enumerate(v):
        angle = theta + i * 2 * math.pi / len(v)
        new_v.append(Vector((center.x + radius * sin(angle),
                             center.y + radius * cos(angle))))

    return new_v


class MUV_AUVCircle(bpy.types.Operator):

    bl_idname = "uv.muv_auv_circle"
    bl_label = "Circle"
    bl_description = "Align UV coordinates to Circle"
    bl_options = {'REGISTER', 'UNDO'}

    transmission = BoolProperty(
        name="Transmission",
        description="Align linked UVs",
        default=False
    )
    select = BoolProperty(
        name="Select",
        description="Select UVs which are aligned",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.verify()

        # loop_seqs[horizontal][vertical][loop]
        loop_seqs, error = get_closed_loop_sequences(bm, uv_layer)
        if not loop_seqs:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # get circle and new UVs
        uvs = [hseq[0][0][uv_layer].uv.copy() for hseq in loop_seqs]
        c, r = get_circle(uvs[0:3])
        new_uvs = calc_v_on_circle(uvs, c, r)

        # check center UV of circle
        center = loop_seqs[0][-1][0].vert
        for hseq in loop_seqs[1:]:
            if len(hseq[-1]) != 1:
                self.report({'WARNING'}, "Last face must be triangle")
                return {'CANCELLED'}
            if hseq[-1][0].vert != center:
                self.report({'WARNING'}, "Center must be identical")
                return {'CANCELLED'}

        # align to circle
        if self.transmission:
            for hidx, hseq in enumerate(loop_seqs):
                for vidx, pair in enumerate(hseq):
                    all_ = int((len(hseq) + 1) / 2)
                    pair[0][uv_layer].uv = c +\
                        (new_uvs[hidx] - c) * (all_ - int((vidx+1)/2)) / all_
                    if self.select:
                        pair[0][uv_layer].select = True

                    # for quad polygon
                    if len(pair) >= 2:
                        pair[1][uv_layer].uv = c +\
                            ((new_uvs[(hidx+1) % len(loop_seqs)]) - c) *\
                            (all_ - int((vidx+1)/2)) / all_
                        if self.select:
                            pair[1][uv_layer].select = True
        else:
            for hidx, hseq in enumerate(loop_seqs):
                pair = hseq[0]
                pair[0][uv_layer].uv = new_uvs[hidx]
                pair[1][uv_layer].uv = new_uvs[(hidx+1) % len(loop_seqs)]
                if self.select:
                    pair[0][uv_layer].select = True
                    pair[1][uv_layer].select = True

        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}


class MUV_AUVSmooth(bpy.types.Operator):

    bl_idname = "uv.muv_auv_smooth"
    bl_label = "Smooth"
    bl_description = "Smooth UV coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    transmission = BoolProperty(
        name="Transmission",
        description="Smooth linked UVs",
        default=False
    )
    mesh_infl = FloatProperty(
        name="Mesh Influence",
        description="Influence rate of mesh vertex",
        min=0.0,
        max=1.0,
        default=0.0
    )
    select = BoolProperty(
        name="Select",
        description="Select UVs which are smoothed",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def __smooth_wo_transmission(self, loop_seqs, uv_layer):
        # calculate path length
        loops = []
        for hseq in loop_seqs:
            loops.extend([hseq[0][0], hseq[0][1]])
        full_vlen = 0
        accm_vlens = [0.0]
        full_uvlen = 0
        accm_uvlens = [0.0]
        orig_uvs = [loop_seqs[0][0][0][uv_layer].uv.copy()]
        for l1, l2 in zip(loops[:-1], loops[1:]):
            diff_v = l2.vert.co - l1.vert.co
            full_vlen = full_vlen + diff_v.length
            accm_vlens.append(full_vlen)
            diff_uv = l2[uv_layer].uv - l1[uv_layer].uv
            full_uvlen = full_uvlen + diff_uv.length
            accm_uvlens.append(full_uvlen)
            orig_uvs.append(l2[uv_layer].uv.copy())

        for hidx, hseq in enumerate(loop_seqs):
            pair = hseq[0]
            for pidx, l in enumerate(pair):
                if self.select:
                    l[uv_layer].select = True

                # ignore start/end loop
                if (hidx == 0 and pidx == 0) or\
                   ((hidx == len(loop_seqs) - 1) and (pidx == len(pair) - 1)):
                    continue

                # calculate target path length
                # target = no influenced * (1 - infl) + influenced * infl
                tgt_noinfl = full_uvlen * (hidx + pidx) / (len(loop_seqs))
                tgt_infl = full_uvlen * accm_vlens[hidx*2 + pidx] / full_vlen
                target_length = tgt_noinfl * (1 - self.mesh_infl) +\
                                tgt_infl * self.mesh_infl

                # get target UV
                for i in range(len(accm_uvlens[:-1])):
                    # get line segment which UV will be placed
                    if ((accm_uvlens[i] <= target_length) and
                            (accm_uvlens[i+1] > target_length)):
                        tgt_seg_len = target_length - accm_uvlens[i]
                        seg_len = accm_uvlens[i+1] - accm_uvlens[i]
                        uv1 = orig_uvs[i]
                        uv2 = orig_uvs[i+1]
                        target_uv = uv1 + (uv2 - uv1) * tgt_seg_len / seg_len
                        break
                else:
                    self.report({'ERROR'}, "Failed to get target UV")
                    return {'CANCELLED'}

                # update UV
                l[uv_layer].uv = target_uv

    def __smooth_w_transmission(self, loop_seqs, uv_layer):
        # calculate path length
        loops = []
        for vidx in range(len(loop_seqs[0])):
            ls = []
            for hseq in loop_seqs:
                ls.extend(hseq[vidx])
            loops.append(ls)

        orig_uvs = []
        accm_vlens = []
        full_vlens = []
        accm_uvlens = []
        full_uvlens = []
        for ls in loops:
            full_v = 0.0
            accm_v = [0.0]
            full_uv = 0.0
            accm_uv = [0.0]
            uvs = [ls[0][uv_layer].uv.copy()]
            for l1, l2 in zip(ls[:-1], ls[1:]):
                diff_v = l2.vert.co - l1.vert.co
                full_v = full_v + diff_v.length
                accm_v.append(full_v)
                diff_uv = l2[uv_layer].uv - l1[uv_layer].uv
                full_uv = full_uv + diff_uv.length
                accm_uv.append(full_uv)
                uvs.append(l2[uv_layer].uv.copy())
            accm_vlens.append(accm_v)
            full_vlens.append(full_v)
            accm_uvlens.append(accm_uv)
            full_uvlens.append(full_uv)
            orig_uvs.append(uvs)

        for hidx, hseq in enumerate(loop_seqs):
            for vidx, (pair, uvs, accm_v, full_v, accm_uv, full_uv)\
                    in enumerate(zip(hseq, orig_uvs, accm_vlens, full_vlens,
                                     accm_uvlens, full_uvlens)):
                for pidx, l in enumerate(pair):
                    if self.select:
                        l[uv_layer].select = True

                    # ignore start/end loop
                    if (hidx == 0 and pidx == 0) or\
                       ((hidx == len(loop_seqs) - 1) and
                            (pidx == len(pair) - 1)):
                        continue

                    # calculate target path length
                    # target = no influenced * (1 - infl) + influenced * infl
                    tgt_noinfl = full_uv * (hidx + pidx) / (len(loop_seqs))
                    tgt_infl = full_uv * accm_v[hidx * 2 + pidx] / full_v
                    target_length = tgt_noinfl * (1 - self.mesh_infl) +\
                                    tgt_infl * self.mesh_infl

                    # get target UV
                    for i in range(len(accm_uv[:-1])):
                        # get line segment to be placed
                        if ((accm_uv[i] <= target_length) and
                                (accm_uv[i+1] > target_length)):
                            tgt_seg_len = target_length - accm_uv[i]
                            seg_len = accm_uv[i+1] - accm_uv[i]
                            uv1 = uvs[i]
                            uv2 = uvs[i+1]
                            target_uv = uv1 +\
                                        (uv2 - uv1) * tgt_seg_len / seg_len
                            break
                    else:
                        self.report({'ERROR'}, "Failed to get target UV")
                        return {'CANCELLED'}

                    # update UV
                    l[uv_layer].uv = target_uv

    def __smooth(self, loop_seqs, uv_layer):
        if self.transmission:
            self.__smooth_w_transmission(loop_seqs, uv_layer)
        else:
            self.__smooth_wo_transmission(loop_seqs, uv_layer)

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.verify()

        # loop_seqs[horizontal][vertical][loop]
        loop_seqs, error = get_loop_sequences(bm, uv_layer)
        if not loop_seqs:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # smooth
        self.__smooth(loop_seqs, uv_layer)

        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}


# get horizontal differential of UV influenced by mesh vertex
def get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, pair_idx):
    muv_common.debug_print(
        "vidx={0}, hidx={1}, pair_idx={2}".format(vidx, hidx, pair_idx))

    # get total vertex length
    hloops = []
    for s in loop_seqs:
        hloops.extend([s[vidx][0], s[vidx][1]])
    vert_total_hlen = get_loop_vert_len(hloops)
    muv_common.debug_print(vert_total_hlen)

    # target vertex length
    hloops = []
    for s in loop_seqs[:hidx]:
        hloops.extend([s[vidx][0], s[vidx][1]])
    for pidx, l in enumerate(loop_seqs[hidx][vidx]):
        if pidx > pair_idx:
            break
        hloops.append(l)
    vert_hlen = get_loop_vert_len(hloops)
    muv_common.debug_print(vert_hlen)

    # get total UV length
    # uv_all_hdiff = loop_seqs[-1][0][-1][uv_layer].uv -
    # loop_seqs[0][0][0][uv_layer].uv
    uv_total_hlen = loop_seqs[-1][vidx][-1][uv_layer].uv -\
                   loop_seqs[0][vidx][0][uv_layer].uv
    muv_common.debug_print(uv_total_hlen)

    return uv_total_hlen * vert_hlen / vert_total_hlen


# get vertical differential of UV influenced by mesh vertex
def get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, pair_idx):
    muv_common.debug_print(
        "vidx={0}, hidx={1}, pair_idx={2}".format(vidx, hidx, pair_idx))

    # get total vertex length
    hloops = []
    for s in loop_seqs[hidx]:
        hloops.append(s[pair_idx])
    vert_total_hlen = get_loop_vert_len(hloops)
    muv_common.debug_print(vert_total_hlen)

    # target vertex length
    hloops = []
    for s in loop_seqs[hidx][:vidx+1]:
        hloops.append(s[pair_idx])
    vert_hlen = get_loop_vert_len(hloops)
    muv_common.debug_print(vert_hlen)

    # get total UV length
    # uv_all_hdiff = loop_seqs[0][-1][pair_idx][uv_layer].uv - \
    #                loop_seqs[0][0][pair_idx][uv_layer].uv
    uv_total_hlen = loop_seqs[hidx][-1][pair_idx][uv_layer].uv -\
                    loop_seqs[hidx][0][pair_idx][uv_layer].uv
    muv_common.debug_print(uv_total_hlen)

    return uv_total_hlen * vert_hlen / vert_total_hlen


# get horizontal differential of UV no influenced
def get_hdiff_uv(uv_layer, loop_seqs, hidx):
    base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()
    h_uv = loop_seqs[-1][0][1][uv_layer].uv.copy() - base_uv

    return hidx * h_uv / len(loop_seqs)


# get vertical differential of UV no influenced
def get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx):
    base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()
    v_uv = loop_seqs[0][-1][0][uv_layer].uv.copy() - base_uv

    hseq = loop_seqs[hidx]
    return int((vidx + 1) / 2) * v_uv / (len(hseq) / 2)


class MUV_AUVStraighten(bpy.types.Operator):

    bl_idname = "uv.muv_auv_straighten"
    bl_label = "Straighten"
    bl_description = "Straighten UV coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    transmission = BoolProperty(
        name="Transmission",
        description="Align linked UVs",
        default=False
    )
    select = BoolProperty(
        name="Select",
        description="Select UVs which are aligned",
        default=False
    )
    vertical = BoolProperty(
        name="Vert-Infl (Vertical)",
        description="Align vertical direction influenced "
                    "by mesh vertex proportion",
        default=False
    )
    horizontal = BoolProperty(
        name="Vert-Infl (Horizontal)",
        description="Align horizontal direction influenced "
                    "by mesh vertex proportion",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    # selected and paralleled UV loop sequence will be aligned
    def __align_w_transmission(self, loop_seqs, uv_layer):
        base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()

        # calculate diff UVs
        diff_uvs = []
        # hseq[vertical][loop]
        for hidx, hseq in enumerate(loop_seqs):
            # pair[loop]
            diffs = []
            for vidx in range(0, len(hseq), 2):
                if self.horizontal:
                    hdiff_uvs = [
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                else:
                    hdiff_uvs = [
                        get_hdiff_uv(uv_layer, loop_seqs, hidx),
                        get_hdiff_uv(uv_layer, loop_seqs, hidx + 1),
                        get_hdiff_uv(uv_layer, loop_seqs, hidx),
                        get_hdiff_uv(uv_layer, loop_seqs, hidx + 1)
                    ]
                if self.vertical:
                    vdiff_uvs = [
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                else:
                    vdiff_uvs = [
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx)
                    ]
                diffs.append([hdiff_uvs, vdiff_uvs])
            diff_uvs.append(diffs)

        # update UV
        for hseq, diffs in zip(loop_seqs, diff_uvs):
            for vidx in range(0, len(hseq), 2):
                loops = [
                    hseq[vidx][0], hseq[vidx][1],
                    hseq[vidx + 1][0], hseq[vidx + 1][1]
                ]
                for l, hdiff, vdiff in zip(loops, diffs[int(vidx/2)][0],
                                           diffs[int(vidx/2)][1]):
                    l[uv_layer].uv = base_uv + hdiff + vdiff
                    if self.select:
                        l[uv_layer].select = True

    # only selected UV loop sequence will be aligned
    def __align_wo_transmission(self, loop_seqs, uv_layer):
        base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()

        h_uv = loop_seqs[-1][0][1][uv_layer].uv.copy() - base_uv
        for hidx, hseq in enumerate(loop_seqs):
            # only selected loop pair is targeted
            pair = hseq[0]
            hdiff_uv_0 = hidx * h_uv / len(loop_seqs)
            hdiff_uv_1 = (hidx + 1) * h_uv / len(loop_seqs)
            pair[0][uv_layer].uv = base_uv + hdiff_uv_0
            pair[1][uv_layer].uv = base_uv + hdiff_uv_1
            if self.select:
                pair[0][uv_layer].select = True
                pair[1][uv_layer].select = True

    def __align(self, loop_seqs, uv_layer):
        if self.transmission:
            self.__align_w_transmission(loop_seqs, uv_layer)
        else:
            self.__align_wo_transmission(loop_seqs, uv_layer)

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.verify()

        # loop_seqs[horizontal][vertical][loop]
        loop_seqs, error = get_loop_sequences(bm, uv_layer)
        if not loop_seqs:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # align
        self.__align(loop_seqs, uv_layer)

        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}


class MUV_AUVAxis(bpy.types.Operator):

    bl_idname = "uv.muv_auv_axis"
    bl_label = "XY-Axis"
    bl_description = "Align UV to XY-axis"
    bl_options = {'REGISTER', 'UNDO'}

    transmission = BoolProperty(
        name="Transmission",
        description="Align linked UVs",
        default=False
    )
    select = BoolProperty(
        name="Select",
        description="Select UVs which are aligned",
        default=False
    )
    vertical = BoolProperty(
        name="Vert-Infl (Vertical)",
        description="Align vertical direction influenced "
                    "by mesh vertex proportion",
        default=False
    )
    horizontal = BoolProperty(
        name="Vert-Infl (Horizontal)",
        description="Align horizontal direction influenced "
                    "by mesh vertex proportion",
        default=False
    )
    location = EnumProperty(
        name="Location",
        description="Align location",
        items=[
            ('LEFT_TOP', "Left/Top", "Align to Left or Top"),
            ('MIDDLE', "Middle", "Align to middle"),
            ('RIGHT_BOTTOM', "Right/Bottom", "Align to Right or Bottom")
        ],
        default='MIDDLE'
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    # get min/max of UV
    def __get_uv_max_min(self, loop_seqs, uv_layer):
        uv_max = Vector((-1000000.0, -1000000.0))
        uv_min = Vector((1000000.0, 1000000.0))
        for hseq in loop_seqs:
            for l in hseq[0]:
                uv = l[uv_layer].uv
                uv_max.x = max(uv.x, uv_max.x)
                uv_max.y = max(uv.y, uv_max.y)
                uv_min.x = min(uv.x, uv_min.x)
                uv_min.y = min(uv.y, uv_min.y)

        return uv_max, uv_min

    # get UV differentiation when UVs are aligned to X-axis
    def __get_x_axis_align_diff_uvs(self, loop_seqs, uv_layer, uv_min,
                                    width, height):
        diff_uvs = []
        for hidx, hseq in enumerate(loop_seqs):
            pair = hseq[0]
            luv0 = pair[0][uv_layer]
            luv1 = pair[1][uv_layer]
            target_uv0 = Vector((0.0, 0.0))
            target_uv1 = Vector((0.0, 0.0))
            if self.location == 'RIGHT_BOTTOM':
                target_uv0.y = target_uv1.y = uv_min.y
            elif self.location == 'MIDDLE':
                target_uv0.y = target_uv1.y = uv_min.y + height * 0.5
            elif self.location == 'LEFT_TOP':
                target_uv0.y = target_uv1.y = uv_min.y + height
            if luv0.uv.x < luv1.uv.x:
                target_uv0.x = uv_min.x + hidx * width / len(loop_seqs)
                target_uv1.x = uv_min.x + (hidx + 1) * width / len(loop_seqs)
            else:
                target_uv0.x = uv_min.x + (hidx + 1) * width / len(loop_seqs)
                target_uv1.x = uv_min.x + hidx * width / len(loop_seqs)
            diff_uvs.append([target_uv0 - luv0.uv, target_uv1 - luv1.uv])

        return diff_uvs

    # get UV differentiation when UVs are aligned to Y-axis
    def __get_y_axis_align_diff_uvs(self, loop_seqs, uv_layer, uv_min,
                                    width, height):
        diff_uvs = []
        for hidx, hseq in enumerate(loop_seqs):
            pair = hseq[0]
            luv0 = pair[0][uv_layer]
            luv1 = pair[1][uv_layer]
            target_uv0 = Vector((0.0, 0.0))
            target_uv1 = Vector((0.0, 0.0))
            if self.location == 'RIGHT_BOTTOM':
                target_uv0.x = target_uv1.x = uv_min.x + width
            elif self.location == 'MIDDLE':
                target_uv0.x = target_uv1.x = uv_min.x + width * 0.5
            elif self.location == 'LEFT_TOP':
                target_uv0.x = target_uv1.x = uv_min.x
            if luv0.uv.y < luv1.uv.y:
                target_uv0.y = uv_min.y + hidx * height / len(loop_seqs)
                target_uv1.y = uv_min.y + (hidx + 1) * height / len(loop_seqs)
            else:
                target_uv0.y = uv_min.y + (hidx + 1) * height / len(loop_seqs)
                target_uv1.y = uv_min.y + hidx * height / len(loop_seqs)
            diff_uvs.append([target_uv0 - luv0.uv, target_uv1 - luv1.uv])

        return diff_uvs

    # only selected UV loop sequence will be aligned along to X-axis
    def __align_to_x_axis_wo_transmission(self, loop_seqs, uv_layer,
                                          uv_min, width, height):
        # reverse if the UV coordinate is not sorted by position
        need_revese = loop_seqs[0][0][0][uv_layer].uv.x\
                      > loop_seqs[-1][0][0][uv_layer].uv.x
        if need_revese:
            loop_seqs.reverse()
            for hidx, hseq in enumerate(loop_seqs):
                for vidx, pair in enumerate(hseq):
                    tmp = loop_seqs[hidx][vidx][0]
                    loop_seqs[hidx][vidx][0] = loop_seqs[hidx][vidx][1]
                    loop_seqs[hidx][vidx][1] = tmp

        # get UV differential
        diff_uvs = self.__get_x_axis_align_diff_uvs(loop_seqs, uv_layer,
                                                    uv_min, width, height)

        # update UV
        for hseq, duv in zip(loop_seqs, diff_uvs):
            pair = hseq[0]
            luv0 = pair[0][uv_layer]
            luv1 = pair[1][uv_layer]
            luv0.uv = luv0.uv + duv[0]
            luv1.uv = luv1.uv + duv[1]

    # only selected UV loop sequence will be aligned along to Y-axis
    def __align_to_y_axis_wo_transmission(self, scene, loop_seqs, uv_layer,
                                          uv_min, width, height):
        # reverse if the UV coordinate is not sorted by position
        need_revese = loop_seqs[0][0][0][uv_layer].uv.y\
                      > loop_seqs[-1][0][0][uv_layer].uv.y
        if need_revese:
            loop_seqs.reverse()
            for hidx, hseq in enumerate(loop_seqs):
                for vidx, pair in enumerate(hseq):
                    tmp = loop_seqs[hidx][vidx][0]
                    loop_seqs[hidx][vidx][0] = loop_seqs[hidx][vidx][1]
                    loop_seqs[hidx][vidx][1] = tmp

        # get UV differential
        diff_uvs = self.__get_y_axis_align_diff_uvs(scene, loop_seqs, uv_layer,
                                                    uv_min, width, height)

        # update UV
        for hseq, duv in zip(loop_seqs, diff_uvs):
            pair = hseq[0]
            luv0 = pair[0][uv_layer]
            luv1 = pair[1][uv_layer]
            luv0.uv = luv0.uv + duv[0]
            luv1.uv = luv1.uv + duv[1]

    # selected and paralleled UV loop sequence will be aligned along to X-axis
    def __align_to_x_axis_w_transmission(self, loop_seqs, uv_layer,
                                         uv_min, width, height):
        # reverse if the UV coordinate is not sorted by position
        need_revese = loop_seqs[0][0][0][uv_layer].uv.x\
                      > loop_seqs[-1][0][0][uv_layer].uv.x
        if need_revese:
            loop_seqs.reverse()
            for hidx, hseq in enumerate(loop_seqs):
                for vidx, pair in enumerate(hseq):
                    tmp = loop_seqs[hidx][vidx][0]
                    loop_seqs[hidx][vidx][0] = loop_seqs[hidx][vidx][1]
                    loop_seqs[hidx][vidx][1] = tmp

        # get offset UVs when the UVs are aligned to X-axis
        align_diff_uvs = self.__get_x_axis_align_diff_uvs(loop_seqs, uv_layer,
                                                          uv_min, width, height)
        base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()
        offset_uvs = []
        for hseq, aduv in zip(loop_seqs, align_diff_uvs):
            luv0 = hseq[0][0][uv_layer]
            luv1 = hseq[0][1][uv_layer]
            offset_uvs.append([luv0.uv + aduv[0] - base_uv,
                               luv1.uv + aduv[1] - base_uv])

        # get UV differential
        diff_uvs = []
        # hseq[vertical][loop]
        for hidx, hseq in enumerate(loop_seqs):
            # pair[loop]
            diffs = []
            for vidx in range(0, len(hseq), 2):
                if self.horizontal:
                    hdiff_uvs = [
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                    hdiff_uvs[0].y = hdiff_uvs[0].y + offset_uvs[hidx][0].y
                    hdiff_uvs[1].y = hdiff_uvs[1].y + offset_uvs[hidx][1].y
                    hdiff_uvs[2].y = hdiff_uvs[2].y + offset_uvs[hidx][0].y
                    hdiff_uvs[3].y = hdiff_uvs[3].y + offset_uvs[hidx][1].y
                else:
                    hdiff_uvs = [
                        offset_uvs[hidx][0],
                        offset_uvs[hidx][1],
                        offset_uvs[hidx][0],
                        offset_uvs[hidx][1],
                    ]
                if self.vertical:
                    vdiff_uvs = [
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                else:
                    vdiff_uvs = [
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx)
                    ]
                diffs.append([hdiff_uvs, vdiff_uvs])
            diff_uvs.append(diffs)

        # update UV
        for hseq, diffs in zip(loop_seqs, diff_uvs):
            for vidx in range(0, len(hseq), 2):
                loops = [
                    hseq[vidx][0], hseq[vidx][1],
                    hseq[vidx + 1][0], hseq[vidx + 1][1]
                ]
                for l, hdiff, vdiff in zip(loops, diffs[int(vidx/2)][0],
                                           diffs[int(vidx/2)][1]):
                    l[uv_layer].uv = base_uv + hdiff + vdiff
                    if self.select:
                        l[uv_layer].select = True

    # selected and paralleled UV loop sequence will be aligned along to Y-axis
    def __align_to_y_axis_w_transmission(self, loop_seqs, uv_layer,
                                         uv_min, width, height):
        # reverse if the UV coordinate is not sorted by position
        need_revese = loop_seqs[0][0][0][uv_layer].uv.y\
                      > loop_seqs[-1][0][-1][uv_layer].uv.y
        if need_revese:
            loop_seqs.reverse()
            for hidx, hseq in enumerate(loop_seqs):
                for vidx, pair in enumerate(hseq):
                    tmp = loop_seqs[hidx][vidx][0]
                    loop_seqs[hidx][vidx][0] = loop_seqs[hidx][vidx][1]
                    loop_seqs[hidx][vidx][1] = tmp

        # get offset UVs when the UVs are aligned to Y-axis
        align_diff_uvs = self.__get_y_axis_align_diff_uvs(loop_seqs, uv_layer,
                                                          uv_min, width, height)
        base_uv = loop_seqs[0][0][0][uv_layer].uv.copy()
        offset_uvs = []
        for hseq, aduv in zip(loop_seqs, align_diff_uvs):
            luv0 = hseq[0][0][uv_layer]
            luv1 = hseq[0][1][uv_layer]
            offset_uvs.append([luv0.uv + aduv[0] - base_uv, luv1.uv + aduv[1] - base_uv])

        # get UV differential
        diff_uvs = []
        # hseq[vertical][loop]
        for hidx, hseq in enumerate(loop_seqs):
            # pair[loop]
            diffs = []
            for vidx in range(0, len(hseq), 2):
                if self.horizontal:
                    hdiff_uvs = [
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_hdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                    hdiff_uvs[0].x = hdiff_uvs[0].x + offset_uvs[hidx][0].x
                    hdiff_uvs[1].x = hdiff_uvs[1].x + offset_uvs[hidx][1].x
                    hdiff_uvs[2].x = hdiff_uvs[2].x + offset_uvs[hidx][0].x
                    hdiff_uvs[3].x = hdiff_uvs[3].x + offset_uvs[hidx][1].x
                else:
                    hdiff_uvs = [
                        offset_uvs[hidx][0],
                        offset_uvs[hidx][1],
                        offset_uvs[hidx][0],
                        offset_uvs[hidx][1],
                    ]
                if self.vertical:
                    vdiff_uvs = [
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx, hidx, 1),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 0),
                        get_vdiff_uv_vinfl(uv_layer, loop_seqs, vidx + 1,
                                           hidx, 1),
                    ]
                else:
                    vdiff_uvs = [
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx),
                        get_vdiff_uv(uv_layer, loop_seqs, vidx + 1, hidx)
                    ]
                diffs.append([hdiff_uvs, vdiff_uvs])
            diff_uvs.append(diffs)

        # update UV
        for hseq, diffs in zip(loop_seqs, diff_uvs):
            for vidx in range(0, len(hseq), 2):
                loops = [
                    hseq[vidx][0], hseq[vidx][1],
                    hseq[vidx + 1][0], hseq[vidx + 1][1]
                ]
                for l, hdiff, vdiff in zip(loops, diffs[int(vidx/2)][0],
                                           diffs[int(vidx/2)][1]):
                    l[uv_layer].uv = base_uv + hdiff + vdiff
                    if self.select:
                        l[uv_layer].select = True

    def __align(self, loop_seqs, uv_layer, uv_min, width, height):
        # align along to x-axis
        if width > height:
            if self.transmission:
                self.__align_to_x_axis_w_transmission(loop_seqs, uv_layer,
                                                      uv_min, width, height)
            else:
                self.__align_to_x_axis_wo_transmission(loop_seqs, uv_layer,
                                                       uv_min, width, height)
        # align along to y-axis
        else:
            if self.transmission:
                self.__align_to_y_axis_w_transmission(loop_seqs, uv_layer,
                                                      uv_min, width, height)
            else:
                self.__align_to_y_axis_wo_transmission(loop_seqs, uv_layer,
                                                       uv_min, width, height)

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        if muv_common.check_version(2, 73, 0) >= 0:
            bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.verify()

        # loop_seqs[horizontal][vertical][loop]
        loop_seqs, error = get_loop_sequences(bm, uv_layer)
        if not loop_seqs:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # get height and width
        uv_max, uv_min = self.__get_uv_max_min(loop_seqs, uv_layer)
        width = uv_max.x - uv_min.x
        height = uv_max.y - uv_min.y

        self.__align(loop_seqs, uv_layer, uv_min, width, height)

        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}
