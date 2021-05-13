import pandas as pd
import numpy as np
from math import *
from sklearn.ensemble import RandomForestRegressor
import joblib
'''
输入：数据raw_data、磨损调整系数beta
输出：健康度H、磨损报警标志flag_wear
'''
def alarm(raw_data, beta=0.60):
    flag_wear = 0
    feature = []
    feature_all = []
    data = []
    for i in range(len(raw_data)):
        data += raw_data[i]

    # 计算rms
    tem = np.array(data)
    rms = sqrt(np.sum(np.int64(tem ** 2)) / len(data))
    feature.append(rms)

    data = pd.Series(data)
    # 计算std、kurt
    std = data.rolling(5000).std()
    feature.append(std[10000])

    kurt = data.rolling(5000).kurt()
    feature.append(kurt[10000])

    feature_all.append(feature)

    # 预测健康度
    rf = joblib.load('rfr.pkl')
    H = rf.predict(feature_all)

    # 磨损报警
    if H < beta:
        flag_wear = 1

    return H, flag_wear
if __name__ == '__main__':
    raw_data = [[150,160,150]]
    rf = joblib.load('rfr.pkl')
    h = rf.predict(raw_data)