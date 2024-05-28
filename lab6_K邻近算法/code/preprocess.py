#coding=utf-8
import pandas as pd
import numpy as np
import math as math

# 打开文本文件
with open("train.txt", "r") as file:
    lines = file.readlines()[1:]  # 删除第一行

# 解析每一行并创建DataFrame
data = []
for line in lines:
    parts = line.strip().split()  # 分割每一行的数据
    document_id = parts[0]
    emotion_id = parts[1]
    emotion = parts[2]
    emotion_words = " ".join(parts[3:])  # 将剩余部分组合成情绪词
    data.append([document_id, emotion_id, emotion_words])

# 创建DataFrame
df = pd.DataFrame(data, columns=["documentId", "emotionId", "emotion_words"])
df = df.set_index("documentId")
df.to_csv("train.csv")

#获取训练数据标签
df_label = pd.DataFrame(df["emotionId"])
df_label.insert(0, "documentId", df.index.values)
df_label.set_index("documentId", inplace=True)   #将documentId设置为索引     
df_label.to_csv("train_label.csv")

#词向量编码
#使用One-Hot编码
for i in range(len(df)): #遍历每一行
    words = df.iloc[i]["emotion_words"].split() #将单词分割
    for word in words:
        df.at[df.index[i], word] = 1 #将单词的列设为1
#填充缺失值
df = df.fillna(0)
print(df.columns)
df.to_csv("train_one_hot.csv")

def counter(list, word):
    count = 0
    for item in list:
        if item == word:
            count = count + 1
    return count


#使用TF-IDF加权编码
#计算IDF
IDF = np.zeros(len(df.columns)-2) #初始化IDF
for word in df.columns[2:]:
    sum = 0 #计算出现单词的文档数
    condition = df[word] == 1 #出现过的条件
    sum = sum + len(df[condition]) #计算出现单词的文档数
    IDF[df.columns.get_loc(word)-2] = math.log(len(df)/sum+1) #计算IDF
#保存IDF
df_IDF = pd.DataFrame(IDF, index=df.columns[2:], columns=["IDF"])
df_IDF.to_csv("IDF.csv")

#计算TF
for i in range(len(df)):
    words = df.iloc[i]["emotion_words"].split()
    for word in words:
        df.at[df.index[i], word] = counter(words, word)/len(words) #计算频率
        df.at[df.index[i], word] = df.at[df.index[i], word]*IDF[df.columns.get_loc(word)-2]         #计算TF-IDF
df.to_csv("train_tfidf.csv") #保存TF-IDF编码的数据



