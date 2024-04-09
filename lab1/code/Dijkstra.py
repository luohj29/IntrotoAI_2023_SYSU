#coding=gbk
class Ugraph():  # ����ͼ
    def __init__(self, contents, vertex: int, edge: int):
        self.contents = contents
        self.vertex = vertex
        self.edge = edge
        self.graph = {}
        for i in range(edge):  # ��ȡͼ�񣬱���Ϊ�ڽӱ�
            a, b, dis = contents[i + 1].split(' ', 2)
            dis = int(dis)
            if a not in self.graph.keys():  # ���ڱ���
                self.graph[a] = {}
                self.graph[a][b] = dis
            else:
                self.graph[a][b] = dis
            if b not in self.graph.keys():  # ���ڱ���
                self.graph[b] = {}
                self.graph[b][a] = dis
            else:
                self.graph[b][a] = dis

    def Dijkstra(self):
        src, dst = self.contents[self.edge + 1].split(' ', 1) 
        In_Part = {}   #��Χ����
        Out_Part = {}  #��Ȧ����
        In_Part[src] = 0  #�ȷ������
        parent ={src:None}
        while True:
            if In_Part is None:   #û�п��Լ�����¶����ˣ��˳�
                print("����ʧ���ˣ�������������·��")
                break

            distance, min_node = min(zip(In_Part.values(), In_Part.keys())) #ͨ�������ж�����Ķ��㣬��ȡ�þ���Ͷ�����
            In_Part.pop(min_node)    #�����Ķ���
            Out_Part[min_node] = distance  #���������Ϣ

            if min_node == dst:               #�Ѿ��ҵ�
                #�����ӡ����㵽�յ�����·��
                print("��",src,"��",dst,"�����·���ǣ�")
                node = dst
                path = []
                while node != src:
                    path.append(node)
                    path.append(self.graph[node][parent[node]])
                    node = parent[node]
                path.append(src)
                path.reverse()
                for i in range(len(path)-1):
                    print(path[i],end="->")
                print(path[-1])
                print("��̵ľ�����",distance)
                break

            for node in self.graph[min_node].keys():   #�����¼��붥����ڽӶ��㣬���¸ö�����Ϊ�м䶥������ı仯
                if node not in Out_Part.keys():      #������Χ����
                    if node in In_Part.keys():
                        if self.graph[min_node][node] + distance <In_Part[node]:  #�����С��Ҫ���¾���
                            In_Part[node] = self.graph[min_node][node] + distance
                            parent[node] = min_node    #���¸����
                        
                    else:
                        In_Part[node] = distance + self.graph[min_node][node]   #���벻���ڵ�Ҫ�������
                        parent[node] = min_node  #���¸��ڵ�