#coding=gbk
counter = 1 
from literal import literal as literal
from clause import clause as clause
import copy

#判断两个文字是否是互斥的。如果两个文字的谓词相同，符号相反
def resolable(a:literal, b:literal):
    if a.weici == b.weici and a.fuhao != b.fuhao:
        return True
    else:
        return False

#判断一个字符串是否是自由变量： 方法：长度为1且是小写字母
def str_is_variable(str):
    if len(str) == 1 and str.islower():
        return True
    else:
        return False
    
#检测文字在句子中是否存在,避免重复添加
def check_in_clause(clause1 : clause, literal_in:literal):
    for i in range(len(clause1.literals)):
        if clause1.literals[i] == literal_in:
            return True
    return False

#MGU且归结函数，输入两个子句，两个子句的编号，输出是否可以合并，以及合并后的子句
def MGU_Resolve(clause_1 : clause, clause_2:clause, a, b, num):  #a,b 是参与MGU_Resolve的编号
    global counter
    clause1 = copy.deepcopy(clause_1)  #获取副本，避免更改原来的子句
    clause2 = copy.deepcopy(clause_2)
    old = []   #装载旧变量和新变量
    new = []
    delete_flag = 0   #互斥删除标志
    rename_flag = 0   #自由变量更名标志

    #寻找两个子句中的可以被自由变量替换的文字
    for i in range(len(clause1.literals)):
        for j in range(len(clause2.literals)):
            if resolable(clause1.literals[i], clause2.literals[j]):  #如果两个文字谓词相同且符号相反
                for k in range(len(clause1.literals[i].variable)):  #寻找子句1文字中的自由变量
                    if str_is_variable(clause1.literals[i].variable[k]) and not(str_is_variable(clause2.literals[j].variable[k])): #判断方法：本身是自由而且对方不是自由
                        rename_flag = 1
                        old.append(clause1.literals[i].variable[k])
                        new.append(clause2.literals[j].variable[k])
                for k in range(len(clause2.literals[j].variable)): #子句2
                    if str_is_variable(clause2.literals[j].variable[k]) and not(str_is_variable(clause1.literals[i].variable[k])):
                        rename_flag = 1
                        if clause2.literals[j].variable[k] not in old:    #避免重复添加自由变量
                            old.append(clause2.literals[j].variable[k])
                            new.append(clause1.literals[i].variable[k]) #记录要改变的变量

    clauses_out = clause([])  #记录生成的子句

    if rename_flag == 1:  #如果有自由变量需要更名
        clause1.rename(old, new)
        clause2.rename(old, new)
        for i in range(len(old)):  #记录更名的变量
            clauses_out.model.append(old[i])
            clauses_out.model.append(new[i])

    #记录删除的元素的位置
    pos1 = []
    pos2 = []

    #搜索两个子句中可以被合并的项，并删除在原子句中的项:方法：遍历两个子句，找到可以合并的项（谓词相同，变量相同，符号相反），然后删除这两个项
    for i in range(len(clause1.literals)):
        for j in range(len(clause2.literals)):
            if clause1.literals[i].weici == clause2.literals[j].weici and clause1.literals[i].variable == clause2.literals[j].variable and clause1.literals[i].fuhao != clause2.literals[j].fuhao:   #如果两个文字的变量相同，符号相反，那么就可以归结
                delete_flag = 1 #说明可以合并互斥项
                pos1.append(i)
                pos2.append(j)
                break
        if delete_flag == 1:
            break
    #删除元素 合并两个子句

    #合成新子句
    for k in range(len(clause1.literals)):
        if k not in pos1:
            clauses_out.literals.append(clause1.literals[k])
    for k in range(len(clause2.literals)):
        if k not in pos2 and not check_in_clause( clauses_out, clause2.literals[k]):
            clauses_out.literals.append(clause2.literals[k])
    
    if delete_flag == 1:
        clauses_out.parents.append(a)
        clauses_out.parents.append(b)
        return True, clauses_out  #返回子句
    else:
        return False, clauses_out  #没有发生归结




#子句集，当其中出现了空子句的时候，说明归结成功，命题逻辑为真
class clauseSet:
    def __init__(self, list_input : list):
        self.KB_first = []  #优先列表存储文字数目为1的子句
        self.KB = []
        for i in range(len(list_input)):
            if len(list_input[i])==1:  #如果子句只有一个文字，那么就是已知的事实
                self.KB_first.append(clause(list_input[i]))
            self.KB.append(clause(list_input[i]))
    
    def display(self):
        for i in range(len(self.KB)):
            self.KB[i].display(i)

   #子句集调用归结函数
    def unify(self):  
        global counter    
        i = 0
        while i < len(self.KB):  #不要使用for_in_range结构，因为在循环中会改变KB的长度
            j = 0
            while j < len(self.KB):
                if(i != j):  #不同的子句才能归结(自己和自己归结没有意义
                    flag, new_clause = MGU_Resolve(self.KB[i], self.KB[j],i,j,len(self.KB))
                    if len(new_clause.literals)==0 and flag ==True:  #如果子句集合中要添加一个空子句，说明推理正确
                        display_parents(self, new_clause, len(self.KB))
                        print("命题是正确的！^_^")
                        return
                    if flag == True:  #如果有归结成功的子句，那么就添加到子句集合中
                        for k in range(len(self.KB)): #遍历整个子句集合，不要重复添加
                            if new_clause.literals == self.KB[k].literals:
                                break
                            if k == len(self.KB)-1:
                                self.KB.append(new_clause)
                j+=1
            i+=1
        print("no more clauses can be resolved")
        return  
        
        



#输出祖先结点的合成步骤：使用深度优先搜索的思路，在归结的时候已经获得了归结步的id和变名情况。先输出祖先结点的合成步骤，然后再输出当前结点的合成步骤
def display_parents(set: clauseSet, clause_final: clause, id : int):
    if len(clause_final.parents) == 0:
        return
    a = clause_final.parents[0]
    b = clause_final.parents[1]
    length = len(clause_final.model)
    display_parents(set,set.KB[a], a)
    display_parents(set,set.KB[b], b)  #先打印输出祖先结点的合成步骤
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