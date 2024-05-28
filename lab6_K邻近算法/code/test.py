#coding=utf-8
import pandas as pd
import numpy as np
import K_classify as K_classify
# ��csv�ļ�
df = pd.read_csv("train_one_hot.csv")
# ɾ����һ��
df1 = df.drop(df.columns[0], axis=1)
# ɾ��emotion_words��
df1= df1.drop("emotion_words", axis=1)
# ��ʾDataFrame
train_data = []
for i in range(len(df1)):
    train_data.append(df1.iloc[i][1:].values)
train_data = np.array(train_data)

train_label = df1["emotionId"].values
K_classifier = K_classify.K_classifier(200, train_data, train_label) #����K_classifier����

#���ɱ�ǩԤ������
df_test = pd.DataFrame(train_data[0:5], columns=df1.columns[1:])
print(df_test)
test_label = []
for i in range(len(df_test)):
    test_label.append(K_classifier(df_test.iloc[i].values))
print(test_label)
#Ԥ���ǩ