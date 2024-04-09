#coding=gbk
'''
this is the heuristic function module, provide the heuristic function of 3 types: manhattan distance, pattern database of 3 and 4
- input: state, the current state of the puzzle
- output: the heuristic value of the state
'''
import numpy as np
import pattern_db_4 as p_db_4
import pattern_db_3 as p_db_3
import pattern_db_3_list as p_db_3_list
import pattern_db_4_list as p_db_4_list
# 启发式函数定义

goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)


def pattern_db_4(state):
    '''
    this heuristic function is based on the pattern database of 4
    devide the 15puzzle as 4 parts: ( [1, 2, 5, 6, 9],[3, 4, 7, 8, 12],[10, 11, 13 ,14, 15]), and calculate the manhattan distance of each part
    add up together as the heuristic value
    we pre-calculate the pattern database and store it in the pattern_db_4.py
    '''
    return p_db_4.pattern_db_4(state)

def pattern_db_4_list(state):
    '''
    as above but for 3 parts, for more info, check the pattern_db_3.py
    '''
    state = state.tolist()
    return p_db_4_list.pattern_db_4(state)

def pattern_db_3_list(state):
    '''
    as above but for 3 parts, for more info, check the pattern_db_3.py
    '''
    return p_db_3_list.pattern_db_3(state)


def pattern_db_3(state):
    '''
    this version is specially designed for the list used in the A*_v1.py, input state as a list
    '''
    state = state.tolist()
    return p_db_3_list.pattern_db_3(state)

#欧式距离
def O_distance(state : list):
    '''
    this heuristic function is based on the euclidean distance
    '''
    distance = 0
    for i in range(4):
        for j in range(4):
            #使用欧几里得距离
            if state[i][j] != 0:
                x_goal, y_goal = (state[i][j] - 1) // 4, (state[i][j] - 1) % 4
                distance += ((x_goal - i) ** 2 + (y_goal - j) ** 2) ** 0.5
    return distance

#manhattan距离
def manhattan_list(state: list):
    '''
    this version is specially designed for the list used in the A*_v1.py, input state as a list
    '''
    state = state.tolist()
    distance = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != 0:
                x_goal, y_goal = (state[i][j] - 1) // 4, (state[i][j] - 1) % 4
                distance += abs(x_goal - i) + abs(y_goal - j)
    return distance

def manhattan(state):
    '''
    manhattan distance is the sum of the distances of the tiles from their goal positions
    '''
    M = 0
    for i in range(16):
        if state[i] == goal[i] or state[i]== 0:
                continue
        if state[i] != 0:
            x_goal, y_goal = i // 4, i % 4
            x_state, y_state = (state[i] -1) // 4, (state[i] -1) % 4
            M += abs(x_goal - x_state) + abs(y_goal - y_state)
    return M

def linear_conflict(state):
    '''
    this heuristic function is based on the manhattan distance
    we add the linear conflict to the manhattan distance
    linear conflict is when two tiles on the same row or column that are in their goal position, but are reversed relative to each other
    '''

if __name__ == "__main__":
    import time
    state =(6, 10, 3, 15, 14, 8, 7, 11, 1, 0, 9, 2, 5, 13, 12, 4)

    begin = time.perf_counter() 
    print(pattern_db_4(state))
    end = time.perf_counter()
    print("time:", end-begin)   