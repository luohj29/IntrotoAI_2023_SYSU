#coding=gbk 
from literal import literal as literal
#子句对象，包含了多个文字，在变量更名的时候，所有的文字相应都要更名  
class clause:
    #初始化函数，输入为一个列表，列表的每个元素是文字
    def __init__(self, list_input : list):
        self.model = []    #记录子句更名的方式，由于结果输出
        self.parents = []   #记录父节点
        self.literals = []
        for i in range(len(list_input)):
            self.literals.append(literal(list_input[i]))
    
    #重构相等函数，用于判断两个子句的相等性（本来的会判断地址）
    def __eq__(self, other):
        isLength = isinstance(other, self.__class__)
        if not isLength or len(self.literals) != len(other.literals):
            return False
        for i in range(len(self.literals)):
            if not self.literals[i]!=other.literals[i]:
                return False
        else:
            return True

     #归结删除函数，由于归结中出现了互斥的文字，所以要删除这些文字  
    def remove(self, a:literal):
        self.literals.remove(a)

    #变量更名函数，由于在MGU中会更名变量，所以文字的变量也要更名
    def rename(self, old, new):   
        for i in range(len(self.literals)):
            self.literals[i].rename(old, new)

    def display(self, id):
        print("%d: "%(id), end = "")
        if len(self.literals)==0:
            print("[]")
        for i in range(len(self.literals)):
            if self.literals[i].fuhao == False:
                print("~",end="")
            print(self.literals[i].weici,end="")
            for j in range(len(self.literals[i].variable)):
                print(self.literals[i].variable[j],end="")
            print(" ",end="")
        print()