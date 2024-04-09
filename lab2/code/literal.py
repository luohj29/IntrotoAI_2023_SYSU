#coding=gbk

#文字对象，包含了文字的谓词符号和文字的取反，以及文字的对象
class literal:
    #初始化函数，输入为一个列表，列表的第一个元素是文字的谓词符号和取反，后面的元素是文字的变量
    def __init__(self, list_input : list):
        if list_input[0][0] == "~":
            self.fuhao = False
        else:
            self.fuhao = True
        if(self.fuhao==False): #取反
            self.weici = list_input[0][1]
        else:
            self.weici = list_input[0][0]
        self.variable = []
        for i in range(1,len(list_input)):
            self.variable.append(list_input[i])
    
    #重构相等函数，用于判断两个文字的相等性（本来的会判断地址）
    def __eq__(self, __value: object) -> bool:
        isLength = isinstance(__value, self.__class__)
        if not isLength:
            return False
        if self.weici == __value.weici and self.fuhao == __value.fuhao and self.variable == __value.variable:
            return True
        else:
            return False
        
    def get_weici(self):
        return self.weici
    
    def get_fuhao(self):
        return self.fuhao
    
    #变量更名函数，由于在MGU中会更名变量，所以文字的变量也要更名.输入自由变量和相应的新常量
    def rename(self, old: list, new: list):
        for j in range(len(old)):
            for i in range(len(self.variable)):
                if self.variable[i] == old[j]:    #如果是要变名的自由变量，那么就更名
                    self.variable[i] = new[j]