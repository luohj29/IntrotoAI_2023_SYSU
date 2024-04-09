def Search(board, EMPTY, BLACK, WHITE, isblack):
    # 目前 AI 的行为是随机落子，请实现 AlphaBetaSearch 函数后注释掉现在的 return 
    # 语句，让函数调用你实现的 alpha-beta 剪枝
    #return RandomSearch(board, EMPTY)
    return AlphaBetaSearch(board, EMPTY, BLACK, WHITE, isblack)

def RandomSearch(board, EMPTY):
    # AI 的占位行为，随机选择一个位置落子
    # 在实现 alpha-beta 剪枝中不需要使用
    from random import randint
    ROWS = len(board)
    x = randint(0, ROWS - 1)
    y = randint(0, ROWS - 1)
    while board[x][y] != EMPTY:
        x = randint(0, ROWS - 1)
        y = randint(0, ROWS - 1)
    return x, y, 0

def AlphaBetaSearch(board, EMPTY, BLACK, WHITE, isblack):
    '''
    ---------------参数---------------
    board       当前的局面，是 15×15 的二维 list，表示棋盘
    EMPTY       空格在 board 中的表示，默认为 -1
    BLACK       黑棋在 board 中的表示，默认为 1
    WHITE       白棋在 board 中的表示，默认为 0
    isblack     bool 变量，表示当前是否轮到黑子落子
    ---------------返回---------------
    x           落子的 x 坐标（行数/第一维）
    y           落子的 y 坐标（列数/第二维）
    alpha       本层的 alpha 值
    '''
    # 请修改此函数，实现 alpha-beta 剪枝
    # =============你的代码=============
    ...
    return x, y, alpha

# 你可能还需要定义评价函数或者别的什么
# =============你的代码=============
...



# 以下为编写搜索和评价函数时可能会用到的函数，请看情况使用、修改和优化
# =============辅助函数=============

def _coordinate_priority(coordinate):
    x, y = coordinate[0], coordinate[1]
    return x * 15 + y

def get_successors(board, color, priority=_coordinate_priority, EMPTY=-1):
    '''
    返回当前状态的所有后继（默认按坐标顺序从左往右，从上往下）
    ---------------参数---------------
    board       当前的局面，是 15×15 的二维 list，表示棋盘
    color       当前轮到的颜色
    EMPTY       空格在 board 中的表示，默认为 -1
    priority    判断落子坐标优先级的函数（结果为小的优先）
    ---------------返回---------------
    一个生成器，每次迭代返回一个的后继状态 (x, y, next_board)
        x           落子的 x 坐标（行数/第一维）
        y           落子的 y 坐标（列数/第二维）
        next_board  后继棋盘
    '''
    # 注意：生成器返回的所有 next_board 是同一个 list！
    from copy import deepcopy
    next_board = deepcopy(board)
    ROWS = len(board)
    idx_list = [(x, y) for x in range(15) for y in range(15)]
    idx_list.sort(key=priority)
    print(idx_list)
    for x, y in idx_list:
        if board[x][y] == EMPTY:
            next_board[x][y] = color
            yield (x, y, next_board)
            next_board[x][y] = EMPTY

# 这是使用 successors 函数的一个例子，打印所有后继棋盘
def _test_print_successors():
    '''
    棋盘：
      0 y 1   2
    0 1---+---1
    x |   |   |
    1 +---0---0
      |   |   |
    2 +---+---1
    本步轮到 1 下
    '''
    board = [
        [ 1, -1,  1],
        [-1,  0,  0],
        [-1, -1,  1]]
    EMPTY = -1
    next_states = get_successors(board, 1)
    for x, y, state in next_states:
        print(x, y, state)
    # 输出：
    # 0 1 [[1, 1, 1], [-1, 0, 0], [-1, -1, 1]]
    # 1 0 [[1, -1, 1], [1, 0, 0], [-1, -1, 1]]
    # 2 0 [[1, -1, 1], [-1, 0, 0], [1, -1, 1]]
    # 2 1 [[1, -1, 1], [-1, 0, 0], [-1, 1, 1]]

def get_next_move_locations(board, EMPTY=-1):
    '''
    获取下一步的所有可能落子位置
    ---------------参数---------------
    board       当前的局面，是 15×15 的二维 list，表示棋盘
    EMPTY       空格在 board 中的表示，默认为 -1
    ---------------返回---------------
    一个由 tuple 组成的 list，每个 tuple 代表一个可下的坐标
    '''
    next_move_locations = []
    ROWS = len(board)
    for x in range(ROWS):
        for y in range(ROWS):
            if board[x][y] != EMPTY:
                next_move_locations.append((x,y))
    return next_move_locations

def get_pattern_locations(board, pattern):
    '''
    获取给定的棋子排列所在的位置
    ---------------参数---------------
    board       当前的局面，是 15×15 的二维 list，表示棋盘
    pattern     代表需要找的排列的 tuple
    ---------------返回---------------
    一个由 tuple 组成的 list，每个 tuple 代表在棋盘中找到的一个棋子排列
        tuple 的第 0 维     棋子排列的初始 x 坐标（行数/第一维）
        tuple 的第 1 维     棋子排列的初始 y 坐标（列数/第二维）
        tuple 的第 2 维     棋子排列的方向，0 为向下，1 为向右，2 为右下，3 为左下；
                            仅对不对称排列：4 为向上，5 为向左，6 为左上，7 为右上；
                            仅对长度为 1 的排列：方向默认为 0
    ---------------示例---------------
    对于以下的 board（W 为白子，B为黑子）
      0 y 1   2   3   4   ...
    0 +---W---+---+---+-- ...
    x |   |   |   |   |   ...
    1 +---+---B---+---+-- ...
      |   |   |   |   |   ...
    2 +---+---+---W---+-- ...
      |   |   |   |   |   ...
    3 +---+---+---+---+-- ...
      |   |   |   |   |   ...
    ...
    和要找的 pattern (WHITE, BLACK, WHITE)：
    函数输出的 list 会包含 (0, 1, 2) 这一元组，代表在 (0, 1) 的向右下方向找到了
    一个对应 pattern 的棋子排列。
    '''
    ROWS = len(board)
    DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]
    pattern_list = []
    palindrome = True if tuple(reversed(pattern)) == pattern else False
    for x in range(ROWS):
        for y in range(ROWS):
            if pattern[0] == board[x][y]:
                if len(pattern) == 1:
                    pattern_list.append((x, y, 0))
                else:
                    for dire_flag, dire in enumerate(DIRE):
                        if _check_pattern(board, ROWS, x, y, pattern, dire[0], dire[1]):
                            pattern_list.append((x, y, dire_flag))
                    if not palindrome:
                        for dire_flag, dire in enumerate(DIRE):
                            if _check_pattern(board, ROWS, x, y, pattern, -dire[0], -dire[1]):
                                pattern_list.append((x, y, dire_flag + 4))
    return pattern_list

# get_pattern_locations 调用的函数
def _check_pattern(board, ROWS, x, y, pattern, dx, dy):
    for goal in pattern[1:]:
        x, y = x + dx, y + dy
        if x < 0 or y < 0 or x >= ROWS or y >= ROWS or board[x][y] != goal:
            return False
    return True

def count_pattern(board, pattern):
    # 获取给定的棋子排列的个数
    return len(get_pattern_locations(board, pattern))

def is_win(board, color, EMPTY=-1):
    # 检查在当前 board 中 color 是否胜利
    pattern1 = (color, color, color, color, color)          # 检查五子相连
    pattern2 = (EMPTY, color, color, color, color, EMPTY)   # 检查「活四」
    return count_pattern(board, pattern1) + count_pattern(board, pattern2) > 0

# 这是使用以上函数的一个例子
def _test_find_pattern():
    '''
    棋盘：
      0 y 1   2   3   4   5
    0 1---+---1---+---+---+
    x |   |   |   |   |   |
    1 +---0---0---0---0---+ ... 此行有 0 的「活四」
      |   |   |   |   |   |
    2 +---+---1---+---+---1
      |   |   |   |   |   |
    3 +---+---+---+---0---+
      |   |   |   |   |   |
    4 +---+---+---1---0---1
      |   |   |   |   |   |
    5 +---+---+---+---+---+
    '''
    board = [
        [ 1, -1,  1, -1, -1, -1],
        [-1,  0,  0,  0,  0, -1],
        [-1, -1,  1, -1, -1,  1],
        [-1, -1, -1, -1,  0, -1],
        [-1, -1, -1,  1,  0,  1],
        [-1, -1, -1, -1, -1, -1]]
    pattern = (1, 0, 1)
    pattern_list = get_pattern_locations(board, pattern)
    assert pattern_list == [(0, 0, 2), (0, 2, 0), (2, 5, 3), (4, 3, 1)]
        # (0, 0) 处有向右下的 pattern
        # (0, 2) 处有向下方的 pattern
        # (2, 5) 处有向左下的 pattern
        # (4, 3) 处有向右方的 pattern
    assert count_pattern(board, (1,)) == 6
        # 6 个 1
    assert count_pattern(board, (1, 0)) == 13
        # [(0, 0, 2), (0, 2, 0), (0, 2, 2), (0, 2, 3), (2, 2, 4), 
        #  (2, 2, 6), (2, 2, 7), (2, 5, 3), (2, 5, 6), (4, 3, 1), 
        #  (4, 3, 7), (4, 5, 5), (4, 5, 6)]
    assert is_win(board, 1) == False
        # 1 没有达到胜利条件
    assert is_win(board, 0) == True
        # 0 有「活四」，胜利
