#coding=utf-8
import pandas as pd
import numpy as np
import K_classify as K_classify
# ��csv�ļ�
df = pd.read_csv("train_tfidf.csv")
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


#���ɱ�ǩԤ������
df_test = pd.read_csv("test_tfidf.csv")
test_label = df_test["documentId"].values #��ȡdocumentId
df_test = df_test.drop(df_test.columns[0], axis=1)
df_test = df_test.drop("emotion_words", axis=1)
df_test = df_test.drop("emotionId", axis=1)

test_data = []
for i in range(len(df_test)):
    test_data.append(df_test.iloc[i][0:].values) #��ÿһ�е�����ת��Ϊlist
test_data = np.array(test_data)



Max_k = 0
Max_accuracy = 0
#Ԥ���ǩ,����Ч����õ�kֵ
#ʹ��ͼ�񻭳�kֵ��׼ȷ�ʵĹ�ϵ
import matplotlib.pyplot as plt
x = []
y = []
for k in range(1, 50):
    K_classifier = K_classify.K_classifier(k, train_data, train_label) #����K_classifier����
    predict_label = []
    for i in range(len(test_data)):
        predict_label.append(K_classifier(test_data[i]))

    df_predict_label = pd.DataFrame(predict_label, columns=["emotionId"])

    #����׼ȷ��
    #�Ȼ����ȷ�ı�ǩ
    correct_label = pd.read_csv("test_label.csv") #��ȡ��ȷ�ı�ǩ
    #����׼ȷ��
    correct_label = correct_label["emotionId"].values
    count = 0
    for i in range(len(correct_label)):
        if correct_label[i] == predict_label[i]:
            count += 1
    accuracy = count / len(correct_label)
    if accuracy > Max_accuracy:
        Max_accuracy = accuracy
        Max_k = k
    x.append(k)
    y.append(accuracy)

plt.plot(x, y)
plt.xlabel("k")
plt.ylabel("accuracy")
plt.show()
print("Max_k:", Max_k)
print("Max_accuracy:", Max_accuracy)

#ʹ����õ�kֵ����Ԥ��
K_classifier = K_classify.K_classifier(Max_k, train_data, train_label) #����K_classifier����
predict_label = []
for i in range(len(test_data)):
    predict_label.append(K_classifier(test_data[i]))

df_predict_label = pd.DataFrame(predict_label, columns=["emotionId"])
df_predict_label["documentId"] = test_label
df_predict_label.to_csv("predict_label.csv")

#���뵽Դ�ļ�
df_test = pd.read_csv("test.csv")
df_test.insert(3, "predict_emotionId", df_predict_label["emotionId"].values)
df_test.to_csv("test_tfidf_output.csv")