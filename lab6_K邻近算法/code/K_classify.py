#coding=utf-8
'''
    this module is about K_classify algorithm
'''
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def Minkowski_distance(point1 :np.array, point2 :np.array, p=2):
    '''
        this function is to calculate the Minkowski distance between two points
    '''
    return np.linalg.norm(point1-point2, ord=p, axis=None, keepdims=False)




class K_classifier:
    def __init__(self, k, train_data, train_label):
        self.k = k
        '''
        train_data shape : (n_samples, n_features)
        '''
        self.train_data = train_data
        '''
        train_label shape : (n_samples, 1)
        '''
        self.train_label = train_label

    def __call__(self, x):
        '''
            this function is to predict the label of x
        '''
        distances = []
        for i in range(self.train_data.shape[0]):
            distance = Minkowski_distance(x, self.train_data[i], 2)  #2维距离
            distances.append((distance, self.train_label[i], i))
        distances.sort(key=lambda x:x[0]) #按照距离排序,从小到大
        labels = [item[1] for item in distances[:self.k]] #取前k个的label
        index = [item[2] for item in distances[:self.k]]
        return max(set(labels), key=labels.count) #返回出现次数最多的label

if __name__ == "__main__":
    #测试
    train_data = np.array([[1,1],[2,2],[3,3],[4,4],[5,5]])#包含了每一个训练样本的特征向量
    train_label = np.array([0,0,1,1,1])
    k = 3
    x = np.array([2,1])
    k_classifier = K_classifier(k, train_data, train_label)
    print(k_classifier(x)) 
