#coding=gbk
import time
from clause_set import clauseSet 
import clause_set as clause_set
import re
'''
���ȶ�ȡ���Ӽ��е������Ӿ䣬�����s�б��У�
-ÿ���Ӿ�Ҳ�������б��ʾ���б��е�Ԫ���Ǵ���
-��~��ʾȡ��
'''
def readClauseSet(filename):
    s = []
    with open(filename, 'r') as f:
        data = f.read()
        row_num = data.split('\n')
        row_num = row_num[0]
        row_num = int(row_num)
        for row in range(1, row_num+1):
            clause = data.split('\n')[row]
            clause = clause.split('),')
            clause = [x.replace('(','').replace(')','').replace(' ','') for x in clause]
            for x in clause:
                if x[0] == '~':
                    str = x[0:2]+','+x[2:]
                elif x[0].isupper():
                    str = x[0]+','+x[1:]
                else:
                    str = x  
                clause[clause.index(x)] = str
            clause = [x.split(',') for x in clause]            
            s.append(clause)
    return s

s = readClauseSet("C:\\Users\\rogers\\Documents\\learning in cs\\ai\\lab2\\blockworld_data.txt")  #��ȡ���Ӽ�
Set = clauseSet(s)

Set.display()  #��ʾ���Ӽ�
starttime = time.perf_counter()
Set.unify()   #���й��
endtime = time.perf_counter()
print("��ʱ��%lfs"%(endtime - starttime))


