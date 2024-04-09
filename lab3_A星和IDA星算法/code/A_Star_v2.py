#coding=gbk
import time
import numpy as np
import copy
import heapq
import H
'''
    A* algorithm 
    implement the A* algorithm by using tuple, because the tuple is hashable and compressible in python.
'''

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

def A_Star(start : tuple, H_x):
    root = node(start,  0, H_x(start), None)
    heapq.heappush(OPEN, root)
    
    while OPEN:
        top = heapq.heappop(OPEN)
        if top.state == (6, 10, 3, 15, 14, 8, 7, 11, 1, 0, 9, 2, 5, 13, 12, 4):
            print("here")
        CLOSE.add(top.state)
        global node_sum
        node_sum += 1
        if top.state == goal:
            return print_path(top)   
        generator = child_generator()
        for cost, state in generator(top.state):
            if  state in CLOSE:
                continue
            child = node(state, top.g_cost + cost, H_x(state), top)
            heapq.heappush(OPEN, child)

if __name__ == "__main__":
    read_txt = [
                ".\\data\\ppt_2.txt",

                ]
    f = open('.\\result\\test.txt','w')
    for idx, txt in enumerate(read_txt):
        with open(txt, "r") as f2:
            start = f2.read().split()
        start = tuple(map(int, start))

        begin = time.perf_counter()
        PATH , WAY= A_Star(start, H.pattern_db_4)
        end = time.perf_counter()
        result = zip(PATH, WAY)
        for i, (p, w) in enumerate(result):
            if i == 0:
                print("Test source from %s:"%(txt))
                print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, w))
                print("%d"%(int(w)),end = ' ')
                f.write("Test source from : %s\n"%(txt))
                f.write('%s\n' %(str(p)))
                f.write("Next step %d: move the tile %d\n\n"%(i, w))
                f.write("%d "%(int(w)))
            else:
                #print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, w))
                print("%d"%(int(w)),end = ' ')
                f.write("%s\n" %(str(p)))
                f.write("Next step {}: move the tile {}\n\n".format(i, w))
                f.write("%d "%(int(w)))
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
