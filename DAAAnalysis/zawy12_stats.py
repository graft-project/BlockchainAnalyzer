import numpy as np


def LWMA_charts(daa_data, target_st=180, single_image=False):
    num_avg_st = 11
    step = len(daa_data[0]) if single_image else 3000
    avg_d = []
    subsets = int(len(daa_data[0]) / step)
    if subsets * step < len(daa_data[0]):
        subsets += 1
    for inx in range(0, subsets, 1):
        diff_subset = daa_data[2][(step * inx):(step * (inx + 1))]
        avg_d.append(np.average(diff_subset))
    diff_div = [0]
    for inx in range(0, len(daa_data[1]) - 1, 1):
        diff_div.append(daa_data[1][inx + 1] - daa_data[1][inx])
    avg_st = []
    for inx in range(0, subsets, 1):
        diff_div_set = diff_div[step * inx:step * (inx + 1)]
        avg_st.append(1.0/1000.0 * int(1000 * np.average(diff_div_set) / target_st))
    norm_avg_diff = []
    for avg_di in avg_d:
        norm_avg_diff.append(daa_data[2] / avg_di)

    # zawy M8
    start_offset = 8
    m8_avg_st = 0
    if diff_div[start_offset - int(num_avg_st / 2)] == 1:
        if diff_div[start_offset - int(num_avg_st / 2) - 1] == 1:
            st_point = start_offset - int(num_avg_st / 2) - 2
            m8_avg_st = np.average(diff_div[st_point:st_point + num_avg_st + 2])
        else:
            st_point = start_offset - int(num_avg_st / 2) - 1
            m8_avg_st = np.average(diff_div[st_point:st_point + num_avg_st + 1])
    else:
        if diff_div[start_offset + int(num_avg_st / 2)] == 1:
            if diff_div[start_offset + int(num_avg_st / 2) + 1] == 1:
                st_point = start_offset - int(num_avg_st / 2)
                m8_avg_st = np.average(diff_div[st_point:st_point + num_avg_st + 2])
            else:
                st_point = start_offset - int(num_avg_st / 2)
                m8_avg_st = np.average(diff_div[st_point:st_point + num_avg_st + 1])
        else:
            if (diff_div[start_offset + int(num_avg_st / 2)] < 0
                    or diff_div[start_offset - int(num_avg_st / 2) - 1] < 0
                    or diff_div[start_offset - int(num_avg_st / 2)] > 7 * target_st
                    or diff_div[start_offset + int(num_avg_st / 2)] > 7 * target_st):
                m8_avg_st = 1 * target_st / avg_st[0]
            else:
                st_point = start_offset - int(num_avg_st / 2)
                m8_avg_st = np.average(diff_div[st_point:st_point + num_avg_st])
    m8_avg_st = m8_avg_st / target_st / avg_st[0]
    # zawy M
    vec_avg_st = [__solve_avg_g(i, diff_div, target_st) for i in range(0, len(diff_div) - 9, 1)]
    # print "vec avg ST", vec_avg_st
    # zawy N
    shift = 16
    hash_attacks = []
    for inx in range(0, shift, 1):
        hash_attacks.append(0)
    for inx in range(0, len(diff_div) - shift, 1):
        n = 0
        if vec_avg_st[shift / 2 + inx - 1] < 0.385:
            n = 1 / vec_avg_st[shift / 2 + inx - 1] / 4
        else:
            if np.sum(hash_attacks[shift + inx - num_avg_st:shift + inx]) > 1.5:
                n = 0.01
        if n < 0:
            n = 0
        hash_attacks.append(n)
    # zawy P
    avg_solvetime = [0 for _ in range(0, 8, 1)]
    avg_solvetime.append(m8_avg_st / 4 if m8_avg_st > 2.1 else 0)
    for avg_st_val in vec_avg_st:
        avg_solvetime.append(avg_st_val / 4 if avg_st_val > 2.1 else 0)
    # avg 11 st
    full_avg_st = [m8_avg_st]
    for avg_st_val in vec_avg_st:
        full_avg_st.append(avg_st_val)
    count_vec = [step - start_offset]
    full_avg_count = len(full_avg_st) - count_vec[0]
    for inx in range(1, subsets, 1):
        if full_avg_count > step:
            count_vec.append(step)
            full_avg_count -= step
        else:
            count_vec.append(full_avg_count)
    avg_11_st = []
    start_from = 0
    for inx in range(0, subsets, 1):
        count_if = []
        for v in full_avg_st[start_from:start_from + count_vec[inx]]:
            if v > 2:
                count_if.append(v)
        avg_11_st.append(1.0 / 100.0 * int(10000.0 * len(count_if) / count_vec[inx]))
        start_from += count_vec[inx]
    stolen_blocks = []
    for inx in range(0, subsets, 1):
        diff_sub_len = len(daa_data[2][(step * inx):(step * (inx + 1))])
        attacks_count = 0
        for v in hash_attacks[(step * inx):(step * (inx + 1))]:
            if v > 0:
                attacks_count += 1
        stolen_blocks.append(1.0 / 100.0 * int(10000.0 * attacks_count / diff_sub_len - 30))
    result_data = []
    for inx in range(0, subsets, 1):
        blocks = daa_data[0][(step * inx):(step * (inx + 1))]
        diff = norm_avg_diff[inx][(step * inx):(step * (inx + 1))]
        hattack = hash_attacks[(step * inx):(step * (inx + 1))]
        solvetimes = avg_solvetime[(step * inx):(step * (inx + 1))]
        title_text = "T={} ".format(target_st)
        title_text += "{} avg ST/T ".format(avg_st[inx])
        title_text += "{} avg 11 ST > 2xT ".format(avg_11_st[inx])
        title_text += "{}% stolen blocks ".format(stolen_blocks[inx])
        last = step * (inx + 1) if step * (inx + 1) < len(daa_data[0]) else len(daa_data[0]) - 1
        title_text += "Blocks: {} to {}".format(int(daa_data[0][0] + step * inx), int(daa_data[0][0] + last))
        char_data = {
            'title': title_text,
            'charts': [
                [blocks, diff, "Difficulty"],
                [blocks, hattack, "Hash attacks"],
                # [blocks, solvetimes, "avg 11 solvetimes >2x target"]
            ]
        }
        result_data.append(char_data)
    return result_data


def __solve_avg_g(i, diff_div, target_st):
    q = 0
    if diff_div[4 + i] > 1:
        if diff_div[3 + i] < 1:
            q = -1
        else:
            if diff_div[3 + i] == 1:
                if diff_div[2 + i] == 1:
                    q = -3
                else:
                    q = -2
            else:
                q = 0
    else:
        if diff_div[4 + i] == 1:
            if diff_div[3 + i] == 1:
                q = -2
            else:
                q = -1
        else:
            q = 0
    d = 0
    if diff_div[14] == 1:
        if diff_div[15] == 1:
            d = 2
        else:
            d = 1
    else:
        if diff_div[14] < 1:
            d = -1
        else:
            d = 0

    return np.average(diff_div[4 + i + q:4 + i + 11 - q + d]) / target_st
