#coding=gbk
counter = 1 
from literal import literal as literal
from clause import clause as clause
import copy

#�ж����������Ƿ��ǻ���ġ�����������ֵ�ν����ͬ�������෴
def resolable(a:literal, b:literal):
    if a.weici == b.weici and a.fuhao != b.fuhao:
        return True
    else:
        return False

#�ж�һ���ַ����Ƿ������ɱ����� ����������Ϊ1����Сд��ĸ
def str_is_variable(str):
    if len(str) == 1 and str.islower():
        return True
    else:
        return False
    
#��������ھ������Ƿ����,�����ظ����
def check_in_clause(clause1 : clause, literal_in:literal):
    for i in range(len(clause1.literals)):
        if clause1.literals[i] == literal_in:
            return True
    return False

#MGU�ҹ�ắ�������������Ӿ䣬�����Ӿ�ı�ţ�����Ƿ���Ժϲ����Լ��ϲ�����Ӿ�
def MGU_Resolve(clause_1 : clause, clause_2:clause, a, b, num):  #a,b �ǲ���MGU_Resolve�ı��
    global counter
    clause1 = copy.deepcopy(clause_1)  #��ȡ�������������ԭ�����Ӿ�
    clause2 = copy.deepcopy(clause_2)
    old = []   #װ�ؾɱ������±���
    new = []
    delete_flag = 0   #����ɾ����־
    rename_flag = 0   #���ɱ���������־

    #Ѱ�������Ӿ��еĿ��Ա����ɱ����滻������
    for i in range(len(clause1.literals)):
        for j in range(len(clause2.literals)):
            if resolable(clause1.literals[i], clause2.literals[j]):  #�����������ν����ͬ�ҷ����෴
                for k in range(len(clause1.literals[i].variable)):  #Ѱ���Ӿ�1�����е����ɱ���
                    if str_is_variable(clause1.literals[i].variable[k]) and not(str_is_variable(clause2.literals[j].variable[k])): #�жϷ��������������ɶ��ҶԷ���������
                        rename_flag = 1
                        old.append(clause1.literals[i].variable[k])
                        new.append(clause2.literals[j].variable[k])
                for k in range(len(clause2.literals[j].variable)): #�Ӿ�2
                    if str_is_variable(clause2.literals[j].variable[k]) and not(str_is_variable(clause1.literals[i].variable[k])):
                        rename_flag = 1
                        if clause2.literals[j].variable[k] not in old:    #�����ظ�������ɱ���
                            old.append(clause2.literals[j].variable[k])
                            new.append(clause1.literals[i].variable[k]) #��¼Ҫ�ı�ı���

    clauses_out = clause([])  #��¼���ɵ��Ӿ�

    if rename_flag == 1:  #��������ɱ�����Ҫ����
        clause1.rename(old, new)
        clause2.rename(old, new)
        for i in range(len(old)):  #��¼�����ı���
            clauses_out.model.append(old[i])
            clauses_out.model.append(new[i])

    #��¼ɾ����Ԫ�ص�λ��
    pos1 = []
    pos2 = []

    #���������Ӿ��п��Ա��ϲ������ɾ����ԭ�Ӿ��е���:���������������Ӿ䣬�ҵ����Ժϲ����ν����ͬ��������ͬ�������෴����Ȼ��ɾ����������
    for i in range(len(clause1.literals)):
        for j in range(len(clause2.literals)):
            if clause1.literals[i].weici == clause2.literals[j].weici and clause1.literals[i].variable == clause2.literals[j].variable and clause1.literals[i].fuhao != clause2.literals[j].fuhao:   #����������ֵı�����ͬ�������෴����ô�Ϳ��Թ��
                delete_flag = 1 #˵�����Ժϲ�������
                pos1.append(i)
                pos2.append(j)
                break
        if delete_flag == 1:
            break
    #ɾ��Ԫ�� �ϲ������Ӿ�

    #�ϳ����Ӿ�
    for k in range(len(clause1.literals)):
        if k not in pos1:
            clauses_out.literals.append(clause1.literals[k])
    for k in range(len(clause2.literals)):
        if k not in pos2 and not check_in_clause( clauses_out, clause2.literals[k]):
            clauses_out.literals.append(clause2.literals[k])
    
    if delete_flag == 1:
        clauses_out.parents.append(a)
        clauses_out.parents.append(b)
        return True, clauses_out  #�����Ӿ�
    else:
        return False, clauses_out  #û�з������




#�Ӿ伯�������г����˿��Ӿ��ʱ��˵�����ɹ��������߼�Ϊ��
class clauseSet:
    def __init__(self, list_input : list):
        self.KB_first = []  #�����б�洢������ĿΪ1���Ӿ�
        self.KB = []
        for i in range(len(list_input)):
            if len(list_input[i])==1:  #����Ӿ�ֻ��һ�����֣���ô������֪����ʵ
                self.KB_first.append(clause(list_input[i]))
            self.KB.append(clause(list_input[i]))
    
    def display(self):
        for i in range(len(self.KB)):
            self.KB[i].display(i)

   #�Ӿ伯���ù�ắ��
    def unify(self):  
        global counter    
        i = 0
        while i < len(self.KB):  #��Ҫʹ��for_in_range�ṹ����Ϊ��ѭ���л�ı�KB�ĳ���
            j = 0
            while j < len(self.KB):
                if(i != j):  #��ͬ���Ӿ���ܹ��(�Լ����Լ����û������
                    flag, new_clause = MGU_Resolve(self.KB[i], self.KB[j],i,j,len(self.KB))
                    if len(new_clause.literals)==0 and flag ==True:  #����Ӿ伯����Ҫ���һ�����Ӿ䣬˵��������ȷ
                        display_parents(self, new_clause, len(self.KB))
                        print("��������ȷ�ģ�^_^")
                        return
                    if flag == True:  #����й��ɹ����Ӿ䣬��ô����ӵ��Ӿ伯����
                        for k in range(len(self.KB)): #���������Ӿ伯�ϣ���Ҫ�ظ����
                            if new_clause.literals == self.KB[k].literals:
                                break
                            if k == len(self.KB)-1:
                                self.KB.append(new_clause)
                j+=1
            i+=1
        print("no more clauses can be resolved")
        return  
        
        



#������Ƚ��ĺϳɲ��裺ʹ���������������˼·���ڹ���ʱ���Ѿ�����˹�Ჽ��id�ͱ����������������Ƚ��ĺϳɲ��裬Ȼ���������ǰ���ĺϳɲ���
def display_parents(set: clauseSet, clause_final: clause, id : int):
    if len(clause_final.parents) == 0:
        return
    a = clause_final.parents[0]
    b = clause_final.parents[1]
    length = len(clause_final.model)
    display_parents(set,set.KB[a], a)
    display_parents(set,set.KB[b], b)  #�ȴ�ӡ������Ƚ��ĺϳɲ���
    print("R[%d,%d]("%(a , b),end = "")
    i = 0
    while i<length:
        if i == length-2:
            print("%s = %s"%(clause_final.model[i],clause_final.model[i+1]), end="")
        else:
            print("%s = %s, "%(clause_final.model[i],clause_final.model[i+1]), end="")
        i += 2
    print(") = ", end = "")
    clause_final.display(id)