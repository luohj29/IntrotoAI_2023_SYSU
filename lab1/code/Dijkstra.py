#coding=gbk
class Ugraph():  # 无向图
    def __init__(self, contents, vertex: int, edge: int):
        self.contents = contents
        self.vertex = vertex
        self.edge = edge
        self.graph = {}
        for i in range(edge):  # 获取图像，保存为邻接表
            a, b, dis = contents[i + 1].split(' ', 2)
            dis = int(dis)
            if a not in self.graph.keys():  # 不在表内
                self.graph[a] = {}
                self.graph[a][b] = dis
            else:
                self.graph[a][b] = dis
            if b not in self.graph.keys():  # 不在表内
                self.graph[b] = {}
                self.graph[b][a] = dis
            else:
                self.graph[b][a] = dis

    def Dijkstra(self):
        src, dst = self.contents[self.edge + 1].split(' ', 1) 
        In_Part = {}   #外围顶点
        Out_Part = {}  #内圈顶点
        In_Part[src] = 0  #先放入起点
        parent ={src:None}
        while True:
            if In_Part is None:   #没有可以加入的新顶点了，退出
                print("搜索失败了，不存在这样的路径")
                break

            distance, min_node = min(zip(In_Part.values(), In_Part.keys())) #通过距离判断最近的顶点，获取该距离和顶点编号
            In_Part.pop(min_node)    #弹出改顶点
            Out_Part[min_node] = distance  #加入距离信息

            if min_node == dst:               #已经找到
                #输出打印从起点到终点的最短路径
                print("从",src,"到",dst,"的最短路径是：")
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
                print("最短的距离是",distance)
                break

            for node in self.graph[min_node].keys():   #遍历新加入顶点的邻接顶点，更新该顶点作为中间顶点带来的变化
                if node not in Out_Part.keys():      #讨论外围顶点
                    if node in In_Part.keys():
                        if self.graph[min_node][node] + distance <In_Part[node]:  #距离变小的要更新距离
                            In_Part[node] = self.graph[min_node][node] + distance
                            parent[node] = min_node    #更新父结点
                        
                    else:
                        In_Part[node] = distance + self.graph[min_node][node]   #距离不存在的要加入距离
                        parent[node] = min_node  #更新父节点