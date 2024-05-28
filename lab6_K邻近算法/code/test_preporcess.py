#coding=utf-8
import pandas as pd
import numpy as np
#打开训练数据
df = pd.read_csv("train_one_hot.csv")
df = df.drop(df.columns[0], axis=1)
df = df.drop("emotion_words", axis=1)



# 打开测试数据文本文件
with open("test.txt", "r") as file:
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
df_test = pd.DataFrame(data, columns=["documentId", "emotionId", "emotion_words"])
df_test = df_test.set_index("documentId")
df_test.to_csv("test.csv")

#获取测试数据标签
test_label = pd.DataFrame(df_test["emotionId"])
test_label.insert(0, "documentId", df_test.index.values)
test_label.set_index("documentId", inplace=True)   #将documentId设置为索引     
test_label.to_csv("train_label.csv")

#词向量编码
#使用One-Hot编码,将训练数据得到的词表作为测试数据的词表
for word in df.columns[1:]:
    for i in range(len(df_test)):
        words = df_test.iloc[i]["emotion_words"].split()
        if word in words:
            df_test.at[df_test.index[i], word] = 1 #将单词的列设为1
        else:
            df_test.at[df_test.index[i], word] = 0 #将单词的列设为0
#填充缺失值
df_test = df_test.fillna(0)

df_test.to_csv("test_one_hot.csv")

def counter(list, word):
    count = 0
    for item in list:
        if item == word:
            count = count + 1
    return count


#使用TF-IDF加权编码
#计算IDF,使用训练数据得到的IDF
IDF = pd.read_csv("IDF.csv")
IDF = np.array(IDF["IDF"])


#计算TF
for i in range(len(df_test)):
    words = df_test.iloc[i]["emotion_words"].split()
    for word in words:
        if word in df.columns:
            df_test.at[df_test.index[i], word] = counter(words, word)/len(words) #计算频率
            df_test.at[df_test.index[i], word] = df_test.at[df_test.index[i], word]*IDF[df.columns.get_loc(word)-2]         #计算TF-IDF
df_test.to_csv("test_tfidf.csv") #保存TF-IDF编码的数据



