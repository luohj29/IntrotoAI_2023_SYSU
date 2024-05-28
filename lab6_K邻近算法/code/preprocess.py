#coding=utf-8
import pandas as pd
import numpy as np
import math as math

# ���ı��ļ�
with open("train.txt", "r") as file:
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
df = pd.DataFrame(data, columns=["documentId", "emotionId", "emotion_words"])
df = df.set_index("documentId")
df.to_csv("train.csv")

#��ȡѵ�����ݱ�ǩ
df_label = pd.DataFrame(df["emotionId"])
df_label.insert(0, "documentId", df.index.values)
df_label.set_index("documentId", inplace=True)   #��documentId����Ϊ����     
df_label.to_csv("train_label.csv")

#����������
#ʹ��One-Hot����
for i in range(len(df)): #����ÿһ��
    words = df.iloc[i]["emotion_words"].split() #�����ʷָ�
    for word in words:
        df.at[df.index[i], word] = 1 #�����ʵ�����Ϊ1
#���ȱʧֵ
df = df.fillna(0)
print(df.columns)
df.to_csv("train_one_hot.csv")

def counter(list, word):
    count = 0
    for item in list:
        if item == word:
            count = count + 1
    return count


#ʹ��TF-IDF��Ȩ����
#����IDF
IDF = np.zeros(len(df.columns)-2) #��ʼ��IDF
for word in df.columns[2:]:
    sum = 0 #������ֵ��ʵ��ĵ���
    condition = df[word] == 1 #���ֹ�������
    sum = sum + len(df[condition]) #������ֵ��ʵ��ĵ���
    IDF[df.columns.get_loc(word)-2] = math.log(len(df)/sum+1) #����IDF
#����IDF
df_IDF = pd.DataFrame(IDF, index=df.columns[2:], columns=["IDF"])
df_IDF.to_csv("IDF.csv")

#����TF
for i in range(len(df)):
    words = df.iloc[i]["emotion_words"].split()
    for word in words:
        df.at[df.index[i], word] = counter(words, word)/len(words) #����Ƶ��
        df.at[df.index[i], word] = df.at[df.index[i], word]*IDF[df.columns.get_loc(word)-2]         #����TF-IDF
df.to_csv("train_tfidf.csv") #����TF-IDF���������



