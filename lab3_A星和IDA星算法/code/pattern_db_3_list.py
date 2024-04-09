#coding=gbk
import pickle
n = 4
# 读取.pkl文件
with open('pattern_database_3_1.pkl', 'rb') as f:
    data1 = pickle.load(f)

with open('pattern_database_3_2.pkl', 'rb') as f:
    data2 = pickle.load(f)

with open('pattern_database_3_3.pkl', 'rb') as f:
    data3 = pickle.load(f)    


# 使用读取的数据

def get_subset_positions(state, values_to_find):
            """Traverses through the state and returns the positions of the values in the values_to_find list

            Inputs:
                - state (list of lists): the state of the puzzle
                - values_to_find (list): the values to find in the state. E.g. [1, 2, 4, 5, 13]
            Outputs:
                - positions (tuple): the positions of the values in the state. E.g. ((0, 1), (0, 2), (1, 0), (1, 1), (3, 2))
            """

            # initialize the dictionary
            values_poistion_dict = {value: (0, 0) for value in values_to_find}

            # traverse through the state and add the positions of the values to the dictionary
            '''
            for i in range(16):
                    if state[i] in values_to_find:
                        values_poistion_dict[state[i]] = (i//4, i%4)
                        '''
            for i in range(4):
                for j in range(4):
                    if state[i][j] in values_to_find:
                        values_poistion_dict[state[i][j]] = (i, j)

            # return the positions of the values in the state from the dictionary as a tuple
            return tuple(values_poistion_dict.values())
           
def pattern_db_3(state: list):
    '''
    This function calculates the sum of the distances of the tiles in the 4 subsets([1, 2, 5, 6, 9] [3, 4, 7, 8, 12] [10, 11, 13, 14, 15]) 
    Previously calculated distances are stored in the data dictionaries.

    Inputs:
    - state (list of lists): the state of the puzzle

    Outputs:
    - distance (int): the sum of the distances of the tiles in the subsets
    '''
    # get the positions of the tiles in the subsets
    indexes_1 = get_subset_positions(state, data1[0]['values'])
    indexes_2 = get_subset_positions(state, data2[0]['values'])
    indexes_3 = get_subset_positions(state, data3[0]['values'])
    # get the distances from the subsets
    distance_1 = data1[0]['distances'][indexes_1]
    distance_2 = data2[0]['distances'][indexes_2]
    distance_3 = data3[0]['distances'][indexes_3]
    # return the sum of the distances
    return distance_1 + distance_2 + distance_3 

#test it as main
# test the speed
if __name__ == "__main__":
    import time
    state = (6, 10, 3, 15, 14, 8, 7, 11, 1, 0, 9, 2, 5, 13, 12, 4)
    begin = time.perf_counter() 
    print(pattern_db_3(state))
    end = time.perf_counter()
    print("time:", end-begin)