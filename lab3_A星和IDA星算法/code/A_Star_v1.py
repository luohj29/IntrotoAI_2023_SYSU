#coding=gbk
# A* algorithm
import time
import numpy as np
import copy
import heapq
import H as H
x_upper = 3
y_upper = 3
#read from txt
start1 = np.array([
    [14,10,6,0],
    [4,9,1,8],
    [2,3,5,11],
    [12,13,7,15]
])

node_sum = 0
goal = np.array([
    [1, 2, 3, 4], 
    [5, 6, 7, 8], 
    [9, 10, 11, 12], 
    [13, 14, 15, 0]
])



class node:
    def __init__(self, state : np.array, blank: tuple, g_cost: int, h_cost : int, parent = None):
        self.blank = blank    #空白块的位置
        self.state = state    #当前状态,矩阵
        self.g_cost = g_cost  #从初始状态到当前状态的代价
        self.h_cost = h_cost  #从当前状态到目标状态的代价
        self.parent = parent
    
    def f_cost(self):
        return self.g_cost + self.h_cost

#获取四个方向的移动，返回一个列表包含四个方向的坐标元组
def try_moving(state, blank: tuple):
    blank_i, blank_j = blank[0], blank[1]
    moves = []
    if blank_i > 0:
        moves.append((blank_i - 1, blank_j))
    if blank_i < 3:
        moves.append((blank_i + 1, blank_j))
    if blank_j > 0:
        moves.append((blank_i, blank_j - 1))
    if blank_j < 3:    
        moves.append((blank_i, blank_j + 1))
    return moves


#交换两个位置的数值,返回移动后的state 和 blank的位置
def swap(state, blank, move: tuple):
    new_state = copy.deepcopy(state)
    new_state[blank[0]][blank[1]], new_state[move[0]][move[1]] = new_state[move[0]][move[1]], new_state[blank[0]][blank[1]]
    return new_state, move

# A*算法
def A_Star(state : np.array, H_x):
    # find the blank in the state
    global node_sum
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                blank = (i, j)
    open_list = []     #open_list是一个优先队列
    closed_list = set()  #记录已经访问过的结点,用于环检测
    start_node = node(state, blank, 0, H_x(state)) #建立初始状态结点
    # 以下使用堆排序来实现优先队列，排序标准是代价函数和结点的id
    heapq.heappush(open_list, (start_node.f_cost, id(start_node), start_node))  #将初始状态结点放入open_list
    while open_list:
        current_node = heapq.heappop(open_list)[2]  #取出open_list中代价最小的结点,2表示元组中的第三个元素
        node_sum += 1
        if np.array_equal(current_node.state, goal):
            print("done!")
            current_blank = current_node.blank
            current_node = current_node.parent
            movement = []
            while current_node:
                movement.append(current_node.state[current_blank])  #记录移动
                current_blank = current_node.blank
                current_node = current_node.parent              
            movement.reverse()
            return movement  #返回移动

        closed_list.add(tuple(map(tuple, current_node.state)))         #set会使用hash函数来判断同元素的state是否存在,作为环检测

        for move in try_moving(current_node.state, current_node.blank):         # 以下是对当前结点的四个方向进行搜索
            new_state, new_blank= swap(current_node.state, current_node.blank, move)
            if tuple(map(tuple, new_state)) not in closed_list:
                new_g_cost = current_node.g_cost + 1 #上一个状态代价函数的加一步
                new_h_cost = H_x(new_state) #新状态到目标状态的代价
                new_node = node(new_state, new_blank, new_g_cost, new_h_cost, current_node)
                heapq.heappush(open_list, (new_node.f_cost(), id(new_node), new_node))    #将新结点放入open_list
    return None

if __name__ == "__main__":
    read_txt = [ ".\\data\\1.txt",
                ".\\data\\2.txt",
                ".\\data\\3.txt",
                ".\\data\\4.txt",
                ".\\data\\ppt_1.txt",
                ".\\data\\ppt_2.txt",

                ]
    f = open('.\\result\\AStar_v1_manhattan.txt','w')
    for idx, txt in enumerate(read_txt):
        with open(txt, "r") as f2:
            start = np.loadtxt(f2)

        
        begin = time.perf_counter()
        PATH = A_Star(start, H.manhattan_list)
        end = time.perf_counter()
        for i, w in enumerate(PATH):
            if i == 0:
                print("Test source from %s:"%(txt))
                #print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, w))
                print("%d"%(int(w)),end = ' ')
                f.write("Test source from : %s\n"%(txt))
                #f.write('%s\n' %(str(p)))
                #f.write("Next step %d: move the tile %d\n\n"%(i, w))
                f.write("%d "%(int(w)))
            else:
                #print(np.array(p).reshape(4,4))
                #print("Next step %d: move the tile %d"%(i, w))
                print("%d"%(int(w)),end = ' ')
                #f.write("%s\n" %(str(p)))
                #f.write("Next step {}: move the tile {}\n\n".format(i, w))
                f.write("%d "%(int(w)))
                #将矩阵转化为字符写入文件

        
        print('\nTest %d, Total Step %d' %(idx+1, len(PATH)))
        print("Used Time %f" %(end - begin), "sec")
        print("Expanded %d nodes" %(node_sum))
        print("---------------------------------")

        f.write('\nTest %d, Total Step %d \n' %(idx+1, len(PATH)))
        f.write("Used Time %f sec\n" %(end - begin))
        f.write("Expanded %d nodes\n\n" %(node_sum))
        f.write("---------------------------------\n")

        node_sum = 0
