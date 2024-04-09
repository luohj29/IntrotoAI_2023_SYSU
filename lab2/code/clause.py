#coding=gbk 
from literal import literal as literal
#�Ӿ���󣬰����˶�����֣��ڱ���������ʱ�����е�������Ӧ��Ҫ����  
class clause:
    #��ʼ������������Ϊһ���б��б��ÿ��Ԫ��������
    def __init__(self, list_input : list):
        self.model = []    #��¼�Ӿ�����ķ�ʽ�����ڽ�����
        self.parents = []   #��¼���ڵ�
        self.literals = []
        for i in range(len(list_input)):
            self.literals.append(literal(list_input[i]))
    
    #�ع���Ⱥ����������ж������Ӿ������ԣ������Ļ��жϵ�ַ��
    def __eq__(self, other):
        isLength = isinstance(other, self.__class__)
        if not isLength or len(self.literals) != len(other.literals):
            return False
        for i in range(len(self.literals)):
            if not self.literals[i]!=other.literals[i]:
                return False
        else:
            return True

     #���ɾ�����������ڹ���г����˻�������֣�����Ҫɾ����Щ����  
    def remove(self, a:literal):
        self.literals.remove(a)

    #��������������������MGU�л�����������������ֵı���ҲҪ����
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