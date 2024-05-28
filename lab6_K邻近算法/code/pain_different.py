#coding=gbk
'''
    打开测试数据标签和预测数据标签，比对两者不同，绘画曲线，
    相同的点置为1， 不同的置为0，绘画曲线
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
df_test_label = pd.read_csv("test_label.csv")
df_predict_label = pd.read_csv("predict_label.csv")

test_label = df_test_label["emotionId"].values
predict_label = df_predict_label["emotionId"].values

#比对两者不同
different = []
for i in range(len(test_label)):
    if test_label[i] == predict_label[i]:
        different.append(1)
    else:
        different.append(0)
x = np.arange(len(test_label))
plt.plot(x, different)
plt.show()