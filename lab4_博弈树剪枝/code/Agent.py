#coding=utf-8
from math import *
import numpy as np



COLUMN = 15  # 列数
ROW = 15  # 行数

ratio = 10  # 系数，用于评估局面。大于1表示有利，小于1表示劣势
DEPTH = 3  # 搜索深度。可以是一个固定的值，如果是变量，函数的调用方会根据上次搜索的结果来决定搜索的层数，保证在决策的时候不会太深也不会太浅。

WIN_FLAG = False   
LOSE_FLAG = False

BEST_POS = [0, 0]  # AI下一步最应该下的位置
list1 = []  # AI方的落子记录
list2 = []  # 人类方的落子记录
list3 = []  # 所有落子记录



list_all = []  # 棋盘上所有位置的列表
for i in range(COLUMN+1):
    for j in range(ROW+1):
        list_all.append((i, j))

BEST_POS = [1, 0]  # AI下一步的最佳落子位置


#搜索函数
def Search(EMPTY, BLACK, WHITE, is_black, latest, board=None):
    print(latest)
    if latest is None:
        list3.append((7, 7)) #第一步落子在中间
        list1.append((7, 7))
        return (7, 7, 0) # 返回中间位置的坐标
    else:
        list2.append(latest)  #将上一步用户下的棋子放入列表
        list3.append(latest)
        BEST_POS[0], BEST_POS[1] = 0, 0  #初始化落子
        
        global cut_count   # 剪枝计数器
        cut_count = 0
        global search_count   # 搜索次数计数器
        search_count = 0

        alpha  = alpha_beta(True, DEPTH, -99999999, 99999999)
        print("cut time: " + str(cut_count))
        print("search time: " + str(search_count))
        print("cut efficiency: " + str(cut_count/search_count)) #剪枝效率
        print("alpha: " + str(alpha))
        
        
        list3.append((BEST_POS[0], BEST_POS[1]))   #将下一步落子放入列表
        list1.append((BEST_POS[0], BEST_POS[1]))   
        
        print("used location: ", end=":")
        print(list3)

        return (BEST_POS[0], BEST_POS[1],  alpha)

# 威胁形状的得分
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (999999, (1, 1, 1, 1, 1))]



# 极大极小算法加alpha-beta剪枝
def alpha_beta(is_ai, depth, alpha, beta):
    # 判断游戏是否结束，或者达到了搜索的深度
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    
    order(blank_list)   # 对搜索的顺序进行排序，提高剪枝效率
    # 遍历每一个空格
    for next_step in blank_list:
        global search_count
        search_count += 1

        # 如果当前位置周围没有相邻的位置被落子，不进行搜索
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)

        value = -alpha_beta(not is_ai, depth - 1, -beta, -alpha)   #负号表示对手的得分

        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if depth == DEPTH:  #在决策的时候
            global LOSE_FLAG
            if LOSE_FLAG:  #如果该步骤会导致敌方有胜利的机会，那么就不要走这一步
                LOSE_FLAG = False
                global cut_count
                cut_count += 1  
                continue
        if value > alpha:
            if depth == DEPTH:
                BEST_POS[0] = next_step[0]
                BEST_POS[1] = next_step[1]
            # alpha + beta剪枝
            if value >= beta:
                print(str(depth) + " " +str(value) + "  alpha:" + str(alpha) + "beta:" + str(beta))
                print(list3)
                cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


#  对搜索顺序进行优化， 将最后一次落子的位置放在列表的最前面
def order(blank_list):
    for last_pt in list3[:-2:-1]:
        for item in blank_list:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                        blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                        blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))
    


# 判断一个位置是否有相邻的落子
def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False


# 评估函数
def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 计算我方的总分数
    score_all_arr = []  # 记录棋型的位置列表，用于判断是否重复计算
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    # 计算敌方的总分数
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    if not is_ai and enemy_score >= 999999:  #判断Ai会不会赢
        global WIN_FLAG
        WIN_FLAG = True

    if not is_ai and my_score >= 50000 and not WIN_FLAG:
        global LOSE_FLAG
        LOSE_FLAG = True  # 输了
    total_score = my_score - enemy_score*10

    return total_score


# 计算每个位置的得分
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
  
    add_score = 0  # 增加的得分
    # 在当前方向上，取得最大的棋型得分
    max_score_shape = (0, None)

    # 如果该方向上已经计算过棋型的得分，则不再计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 遍历当前位置前后5个位置
    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1,1,1,1,1) :
                    print('continue 5')
                if tmp_shap6 == (0,1,1,1,1,0):
                    print('live 4')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # 将最大的棋型加入到记录列表中
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


# 判断游戏是否胜利
def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False


# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # 1 # # # # # # # #
# # # # # # # 0 # # # # # # #
# # # # # # # 1 0 # # # # # #
# # # # # # # 1 1 0 # # # # #
# # # # # # # 1 1 # # # # # #
# # # # # 0 # 0 0 # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #

def test():
    
    with open("lab4\\example\\14.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, x in enumerate(line.strip().split(" ")):
                if x=="1":
                    list1.append((i, j))
                    list3.append((i, j))
                if x=="0":
                    list2.append((i, j))
                    list3.append((i, j))
    print(list3)
    x, y, alpha = Search(0, 1, 2, True,  (8, 5) , board = None)
    print(x, y, alpha) 

if __name__  == "__main__":
    test()
    #