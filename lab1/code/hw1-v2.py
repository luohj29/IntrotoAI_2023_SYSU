# coding=gbk
from Dijkstra import Ugraph as Ugraph
# ������

#a dijstra algorithm
try:
    with open('C:\\Users\\rogers\\Documents\\learning in cs\\ai\lab1\\code\\data\\hw1_data.txt') as file_object:
        contents = file_object.read()
except FileNotFoundError:
    print("File not found. Please check the file path and try again.")
else:
    print("Data has been loaded ^_^ !")  
    content_list = contents.split('\n')  # ���Ϊ�б�
    line0 = content_list[0].split()  # ��ȡ��һ�еĶ������ͱ���
    vertex = int(line0[0])
    edge = int(line0[1])
    my_graph = Ugraph(content_list, vertex, edge)
    my_graph.Dijkstra()
