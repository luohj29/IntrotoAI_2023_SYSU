#coding=gbk

#���ֶ��󣬰��������ֵ�ν�ʷ��ź����ֵ�ȡ�����Լ����ֵĶ���
class literal:
    #��ʼ������������Ϊһ���б��б�ĵ�һ��Ԫ�������ֵ�ν�ʷ��ź�ȡ���������Ԫ�������ֵı���
    def __init__(self, list_input : list):
        if list_input[0][0] == "~":
            self.fuhao = False
        else:
            self.fuhao = True
        if(self.fuhao==False): #ȡ��
            self.weici = list_input[0][1]
        else:
            self.weici = list_input[0][0]
        self.variable = []
        for i in range(1,len(list_input)):
            self.variable.append(list_input[i])
    
    #�ع���Ⱥ����������ж��������ֵ�����ԣ������Ļ��жϵ�ַ��
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
    
    #��������������������MGU�л�����������������ֵı���ҲҪ����.�������ɱ�������Ӧ���³���
    def rename(self, old: list, new: list):
        for j in range(len(old)):
            for i in range(len(self.variable)):
                if self.variable[i] == old[j]:    #�����Ҫ���������ɱ�������ô�͸���
                    self.variable[i] = new[j]