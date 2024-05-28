#coding=utf-8
import pandas as pd
import numpy as np
import K_classify as K_classify
# 打开csv文件
df = pd.read_csv("train_one_hot.csv")
# 删除第一列
df1 = df.drop(df.columns[0], axis=1)
# 删除emotion_words列
df1= df1.drop("emotion_words", axis=1)
# 显示DataFrame
train_data = []
for i in range(len(df1)):
    train_data.append(df1.iloc[i][1:].values)
train_data = np.array(train_data)

train_label = df1["emotionId"].values
K_classifier = K_classify.K_classifier(200, train_data, train_label) #创建K_classifier对象

#生成标签预测数据
df_test = pd.DataFrame(train_data[0:5], columns=df1.columns[1:])
print(df_test)
test_label = []
for i in range(len(df_test)):
    test_label.append(K_classifier(df_test.iloc[i].values))
print(test_label)
#预测标签