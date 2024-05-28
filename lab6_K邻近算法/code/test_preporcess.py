#coding=utf-8
import pandas as pd
import numpy as np
#��ѵ������
df = pd.read_csv("train_one_hot.csv")
df = df.drop(df.columns[0], axis=1)
df = df.drop("emotion_words", axis=1)



# �򿪲��������ı��ļ�
with open("test.txt", "r") as file:
    lines = file.readlines()[1:]  # ɾ����һ��

# ����ÿһ�в�����DataFrame
data = []
for line in lines:
    parts = line.strip().split()  # �ָ�ÿһ�е�����
    document_id = parts[0]
    emotion_id = parts[1]
    emotion = parts[2]
    emotion_words = " ".join(parts[3:])  # ��ʣ�ಿ����ϳ�������
    data.append([document_id, emotion_id, emotion_words])

# ����DataFrame
df_test = pd.DataFrame(data, columns=["documentId", "emotionId", "emotion_words"])
df_test = df_test.set_index("documentId")
df_test.to_csv("test.csv")

#��ȡ�������ݱ�ǩ
test_label = pd.DataFrame(df_test["emotionId"])
test_label.insert(0, "documentId", df_test.index.values)
test_label.set_index("documentId", inplace=True)   #��documentId����Ϊ����     
test_label.to_csv("train_label.csv")

#����������
#ʹ��One-Hot����,��ѵ�����ݵõ��Ĵʱ���Ϊ�������ݵĴʱ�
for word in df.columns[1:]:
    for i in range(len(df_test)):
        words = df_test.iloc[i]["emotion_words"].split()
        if word in words:
            df_test.at[df_test.index[i], word] = 1 #�����ʵ�����Ϊ1
        else:
            df_test.at[df_test.index[i], word] = 0 #�����ʵ�����Ϊ0
#���ȱʧֵ
df_test = df_test.fillna(0)

df_test.to_csv("test_one_hot.csv")

def counter(list, word):
    count = 0
    for item in list:
        if item == word:
            count = count + 1
    return count


#ʹ��TF-IDF��Ȩ����
#����IDF,ʹ��ѵ�����ݵõ���IDF
IDF = pd.read_csv("IDF.csv")
IDF = np.array(IDF["IDF"])


#����TF
for i in range(len(df_test)):
    words = df_test.iloc[i]["emotion_words"].split()
    for word in words:
        if word in df.columns:
            df_test.at[df_test.index[i], word] = counter(words, word)/len(words) #����Ƶ��
            df_test.at[df_test.index[i], word] = df_test.at[df_test.index[i], word]*IDF[df.columns.get_loc(word)-2]         #����TF-IDF
df_test.to_csv("test_tfidf.csv") #����TF-IDF���������



