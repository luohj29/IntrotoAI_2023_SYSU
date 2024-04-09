#coding=gbk
'''
this file is used to calculate the pattern database of 4 subsets, previously calculated distances are stored in the data dictionaries.
you can check them in the pattern_database.pkl file and so on.
-Input: state as tuple
-Output: the heuristic value of the state
'''
import pickle
n = 4
# 读取.pkl文件
with open('pattern_database1.pkl', 'rb') as f:
    data1 = pickle.load(f)

with open('pattern_database2.pkl', 'rb') as f:
    data2 = pickle.load(f)

with open('pattern_database3.pkl', 'rb') as f:
    data3 = pickle.load(f)    

with open('pattern_database4.pkl', 'rb') as f:
    data4 = pickle.load(f)
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
            for i in range(16):
                if state[i] in values_to_find:
                    values_poistion_dict[state[i]] = (i//4, i%4)

            # return the positions of the values in the state from the dictionary as a tuple
            return tuple(values_poistion_dict.values())
           
def pattern_db_4(state: tuple):
    '''
    This function calculates the sum of the distances of the tiles in the 4 subsets([1, 2, 5, 6] [3, 4, 7, 8] [9, 10, 13, 14] [11, 12, 15]). 
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
    indexes_4 = get_subset_positions(state, data4[0]['values'])
    # get the distances from the subsets
    distance_1 = data1[0]['distances'][indexes_1]
    distance_2 = data2[0]['distances'][indexes_2]
    distance_3 = data3[0]['distances'][indexes_3]
    distance_4 = data4[0]['distances'][indexes_4]
    
    # return the sum of the distances
    return distance_1 + distance_2 + distance_3 + distance_4

#test it as main
# test the speed


if __name__ == "__main__":
    input_data = [(6, 10, 3, 15, 14, 0, 7, 11, 1, 8, 9, 2, 5, 13, 12, 4),
(6, 10, 3, 15, 0, 14, 7, 11, 1, 8, 9, 2, 5, 13, 12, 4),
(6, 10, 3, 15, 1, 14, 7, 11, 0, 8, 9, 2, 5, 13, 12, 4),
(6, 10, 3, 15, 1, 14, 7, 11, 5, 8, 9, 2, 0, 13, 12, 4),
(6, 10, 3, 15, 1, 14, 7, 11, 5, 8, 9, 2, 13, 0, 12, 4),
(6, 10, 3, 15, 1, 14, 7, 11, 5, 0, 9, 2, 13, 8, 12, 4),
(6, 10, 3, 15, 1, 0, 7, 11, 5, 14, 9, 2, 13, 8, 12, 4),
(6, 10, 3, 15, 1, 7, 0, 11, 5, 14, 9, 2, 13, 8, 12, 4),
(6, 10, 3, 15, 1, 7, 11, 0, 5, 14, 9, 2, 13, 8, 12, 4),
(6, 10, 3, 15, 1, 7, 11, 2, 5, 14, 9, 0, 13, 8, 12, 4),    
]
    import time
    for i in range(len(input_data)):
        state = input_data[i]
        begin = time.perf_counter() 
        print(pattern_db_4(state))
        end = time.perf_counter()
        print("time:", end-begin)
