#coding=gbk
import time
import numpy as np
import copy
import heapq
import H



OPEN = []
CLOSE = set()
path = []
way = []


def print_path(node, move = 15):
    if node.parent != None:  #深度优先搜索
        print_path(node.parent, node.state.index(0))
    path.append(node.state)
    way.append(node.state[move])
    return path, way

def child_generator():
    movetable = []
    for i in range(16):
        x,y = i%4, i//4
        moves = []
        if x > 0: moves.append(-1)
        if x < 3: moves.append(+1)
        if y > 0: moves.append(-4)
        if y < 3: moves.append(+4)
        movetable.append(moves)
    def children(state):
        idxz = state.index(0)
        l = list(state)
        for m in movetable[idxz]:
            l[idxz] = l[idxz + m]
            l[idxz + m] = 0
            yield (1, tuple(l))
            l[idxz + m] = l[idxz]
            l[idxz] = 0
    return children

node_sum = 0
goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
class node:
    def __init__(self, state ,  g_cost: int, h_cost : int, parent = None):
        self.state = state    #当前状态,矩阵
        self.g_cost = g_cost  #从初始状态到当前状态的代价
        self.h_cost = h_cost  #从当前状态到目标状态的代价
        self.f_cost = self.g_cost + self.h_cost
        self.parent = parent

    def __lt__(self, other):
        if self.f_cost == other.f_cost:
            return self.g_cost > other.g_cost
        return self.f_cost < other.f_cost

def IDAsearch(g, Hx, bound): 
    global node_sum
    node = path[-1]  # 取出path中的start结点,这里相当于如果迭代超过了bound，回来继续迭代的开始结点，也就是path中的最后一个结点
    node_sum +=1
    f = g + Hx(node) 
    if f > bound:      # 如果f(n)的值大于bound则返回f(n)
        return f
    if node == goal: # 目标检测，以0表示找到目标
        return 0  
    
    Min = 99999 # 保存子结点中返回的最小的f值，作为下次迭代的bound
    generator = child_generator() # 获取child_generator()中生成的child
    for cost, state in generator(node):
        if state in CLOSE: continue
        path.append(state)
        way.append(state.index(0))
        CLOSE.add(state) # 利用set查找的优势，进行路径检测
        t = IDAsearch(g+1,Hx,bound)

        if t == 0: return 0
        if t < Min: Min = t

        path.pop() # 回溯
        way.pop()
        CLOSE.remove(state) 
    return Min
   

def IDAstar(start, Hx):
    global CLOSE
    global path
    bound = Hx(start) # IDA*迭代限制
    path = [start] # 路径集合, 视为栈

    while(True):
        ans = IDAsearch(0, Hx,bound) # path, g, Hx, bound
        if(ans == 0):
            return (path,way,bound)
        if ans == -1:
            return None
        bound = ans # 此处对bound进行更新

'''
test function:
    read the txt file and solve the 15-puzzle problem
    print the result and write the result to the file 
    input:
    normal: ".\\data\\1.txt",
                ".\\data\\2.txt",
                ".\\data\\3.txt",
                ".\\data\\4.txt",
    full complex: ".\\data\\1.txt",
                ".\\data\\2.txt",
                ".\\data\\3.txt",
                ".\\data\\4.txt",
                ".\\data\\ppt_1.txt",
                ".\\data\\ppt_2.txt",
                ".\\data\\ppt_3.txt",
                ".\\data\\ppt_4.txt",
'''
if __name__ == "__main__":
    read_txt = [
                ".\\data\\ppt_4.txt",
                ]
    f = open('.\\result\\IDAStar_Result_db4_add.txt','w')
    for idx, txt in enumerate(read_txt):
        with open(txt, "r") as f2:
            start = f2.read().split()
        start = tuple(map(int, start))
        
        begin = time.perf_counter()
        PATH , WAY, bound= IDAstar(start, H.pattern_db_4)
        end = time.perf_counter()
        result = zip(PATH, WAY)
        for i, (p, w) in enumerate(result):
            if i == 0:
                print("Test source from %s:"%(txt))
                print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, int(p[w])))
                print("%d"%(int(p[w])),end = ' ')
                f.write("Test source from : %s\n"%(txt))
                f.write('%s\n' %(str(p)))
                #f.write("Next step %d: move the tile %d\n\n"%(i, int(p[w])))
                f.write("%d "%(int(p[w])))
            else:
                #print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, int(p[w])))
                print("%d"%(int(p[w])),end = ' ')
                #f.write("%s\n" %(str(p)))
                #f.write("Next step {}: move the tile {}\n\n".format(i, int(p[w])))
                f.write("%d "%(int(p[w])))
                #将矩阵转化为字符写入文件

        
        print('\nTest %d, Total Step %d' %(idx+1, len(path)-1))
        print("Used Time %f" %(end - begin), "sec")
        print("Expanded %d nodes" %(node_sum))
        print("---------------------------------")

        f.write('\nTest %d, Total Step %d \n' %(idx+1, len(path)-1))
        f.write("Used Time %f sec\n" %(end - begin))
        f.write("Expanded %d nodes\n\n" %(node_sum))
        f.write("---------------------------------\n")

        OPEN.clear()
        CLOSE.clear()
        path.clear()
        way.clear()
        node_sum = 0