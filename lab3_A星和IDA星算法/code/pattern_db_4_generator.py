'''
this file is used to generate the pattern database for the 4x4 puzzle, first devide the puzzle into 4 subsets, then calculate the distance of each subset
then store the data in the pkl file for rapid access later
'''
n = 4
def get_subset_positions(state, values_to_find):
            '''
            this function is used to get the positions of the values in the values_to_find list
            Inputs: state (list of lists): the state of the puzzle
                    values_to_find (list): the values to find in the state. E.g. [1, 2, 5, 6]
            Outputs: positions (tuple): the positions of the values in the state. E.g. ((0, 0), (0, 1), (1, 0), (1, 1))
            '''
            # initialize the dictionary
            values_poistion_dict = {value: (0, 0) for value in values_to_find}

            # traverse through the state and add the positions of the values to the dictionary
            for i in range(n):
                for j in range(n):
                    if state[i][j] in values_to_find:
                        values_poistion_dict[state[i][j]] = (i, j)

            # return the positions of the values in the state from the dictionary as a tuple
            return tuple(values_poistion_dict.values())

def static_additive_disjoint_pattern_database():
    '''
    this function is used to train the data. use backward BFS from the goal state to every case to build the position-distance dictionary
    '''
    # read file if it exists
    try:
        with open('static_additive_disjoint_pattern_database.txt', 'r') as f:
            static_additive_disjoint_pattern_database = eval(f.read())
            print('Static additive disjoint pattern database loaded from file.')
    except:
        print('Static additive disjoint pattern database not found. Generating static additive disjoint pattern database...')

        from copy import deepcopy

        n = 4

        subset_1_goalstate = {'values': [1, 2, 5, 6],
                              'goalstate': [[1, 2, -1, -1],
                                            [5, 6, -1, -1],
                                            [-1, -1, -1, -1],
                                            [-1, -1, -1, 0]],
                              'goalstate_indexes': ((0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)),
                              'distances': {((0, 0), (0, 1), (1, 0), (1, 1)): 0}
                              }

        subset_2_goalstate = {'values': [3, 4, 7, 8],
                              'goalstate': [[-1, -1, 3, 4],
                                            [-1, -1, 7, 8],
                                            [-1, -1, -1, -1],
                                            [-1, -1, -1, 0]],
                              'goalstate_indexes': ((0, 3), (1, 2), (1, 3), (3, 2), (3, 3), (4, 3)),
                              'distances': {((0, 2), (0, 3), (1, 2), (1, 3)): 0}
                              }

        subset_3_goalstate = {'values': [9, 10, 13 ,14],
                              'goalstate': [[-1, -1, -1, -1],
                                            [-1, -1, -1, -1],
                                            [9, 10, -1, -1],
                                            [13, 14, -1, 0]],
                              'goalstate_indexes': ((3, 0), (3, 1), (3, 2)),
                              'distances': {((2, 0), (2, 1), (3, 0),(3, 1)): 0}
                              }
        subset_4_goalstate = {'values': [11, 12, 15],
                              'goalstate': [[-1, -1, -1, -1],
                                            [-1, -1, -1, -1],
                                            [-1, -1, 11, 12],
                                            [-1, -1, 15, 0]],
                              'goalstate_indexes': ((3, 0), (3, 1), (3, 2)),
                              'distances': {((2, 2), (2, 3), (3, 2)): 0}
                              }
        
        
        # initialize the action space
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for subset in [subset_3_goalstate,]: # for each of the subsets
            # BFS process
            queue = [] # initialize the queue
            visited = set() # initialize the visited set

            # Add the goal state to the queue
            queue.append(subset['goalstate'])
            # Add the goal state to the visited set
            visited.add(tuple([tuple(row) for row in subset['goalstate']]))

            # While the queue is not empty
            while queue:
                # Pop the first state from the queue
                state = queue.pop(0)
                indexes = get_subset_positions(state, subset['values'])
                distance = subset['distances'][indexes]

                # get the position of the blank space
                for i in range(n):
                    for j in range(n):
                        if state[i][j] == 0:
                            blank_row, blank_col = i, j
                            break

                # For each action in the action space
                for move in moves:
                    new_row, new_col = blank_row + move[0], blank_col + move[1] # get the new position of the blank space
                    if (new_row >= 0 and new_row < n) and (new_col >= 0 and new_col < n): # check if the new position is valid
                        new_state = deepcopy(state) # create a copy of the state
                        # switch the blank space with the tile in the new position
                        new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
                        indexes = get_subset_positions(
                            new_state, subset['values']) # get the positions of the tiles in the subset

                        # check if not in visited
                        if tuple([tuple(row) for row in new_state]) not in visited:
                            # check if blank switched with a tile that has a value of -1
                            if new_state[new_row][new_col] == -1: # if yes, then the distance is 1 more than the parent
                                if indexes in subset['distances']: # check if the distance is already in the dictionary
                                    subset['distances'][indexes] = min(
                                        distance, subset['distances'][indexes]) # update the distance if it is less than the current distance
                                else: # if the distance is not in the dictionary, then add it
                                    subset['distances'][indexes] = distance # add the distance to the dictionary
                            else: # if the blank space switched with a tile that has a value other than -1, then the distance is 1 more than the parent
                                if indexes in subset['distances']: # check if the distance is already in the dictionary
                                    subset['distances'][indexes] = min(
                                        distance+1, subset['distances'][indexes]) # update the distance if it is less than the current distance
                                else:
                                    subset['distances'][indexes] = distance + 1 # add the distance to the dictionary

                            queue.append(new_state) # add the new state to the queue
                visited.add(tuple([tuple(row) 
                            for row in state])) # add the new state to the visited set
            print("Subset finished. ")
            import pickle
             # save the pattern database to a pkl file so you only have to run it once
            with open('pattern_database3.pkl', 'wb') as f:
                pickle.dump(
                    [subset], f)
                print(subset['values'], end = '')
                print('Static additive disjoint pattern database saved to file.')
                f.close()
        # save the pattern database to a pkl file so you only have to run it once
       
        return subset_1_goalstate['distances'], subset_2_goalstate['distances'], subset_3_goalstate['distances']



static_additive_disjoint_pattern_database()

