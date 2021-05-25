import numpy as np
from math import *
'''
输入：数据raw_data、磨损调整系数beta
输出：健康度H、磨损报警标志flag_wear,断刀报警标志flag_broken
'''
def alarm(raw_data, beta=0.40):
    flag_wear = 0
    flag_broken = 0
    data = []
    for i in range(len(raw_data)):
        data += raw_data[i]

    # 计算rms
    tem = np.array(data)
    rms = sqrt(np.sum(np.int64(tem ** 2)) / len(data))

    # 断刀报警
    if rms < 85:
        flag_broken = 1

    # 预测健康度
    H = 2 - rms/110+0.15

    if H > 1:
        H = 1
        return H, flag_wear, flag_broken
    # 磨损报警
    elif beta < H < 1:
        return H, flag_wear, flag_broken

    elif 0 < H < beta:
        flag_wear = 1
        return H, flag_wear, flag_broken
    else:
        H = 0
        return H, flag_wear, flag_broken
