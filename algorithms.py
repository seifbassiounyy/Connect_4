import sys


def minimax(state, k):
    beststate = recursion(state, (2 * k - 1), 1)


def recursion(state, k, flag, alpha, beta):
    if k == 1:
        max = -sys.maxsize
        children = getchildren(state)
        for child in children:
            h = heuristic(child)
            if h > max:
                max = h

        return [child, max]

    if flag == 2:
        children = getchildren(state)
        max = -sys.maxsize
        for child in children:
            r = recursion(child, k - 1, 0)
            value = r[1]
            if value > max:
                max = value

    elif flag == 1:
        children = getchildren(state)
        Min = sys.maxsize
        for child in children:
            value = recursion(child, k - 1, 1)
            if value < Min:
                Min = value


def heuristic(state):
    score = getScore(state)
    h1 = score[0] - score[1]


def is_full(state):
    for col in range(7):
        for row in range(6):
            if state[row][col] == 0:
                return 0
    return 1


def getchildren(state, flag):
    children = []
    for col in range(7):
        for row in range(6):
            x = state[row][col]
            if x == 0:
                child = [state[i].copy() for i in range(6)]
                if flag == 1:
                    child[row][col] = '1'
                    children.append(child)
                else:
                    child[row][col] = '2'
                    children.append(child)
                break

    return children


def getScore(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0

    # check rows
    for i in range(6):
        for j in range(4):
            if state[i][j] != '0' and state[i][j] == state[i][j + 1] and state[i][j] == state[i][j + 2] and \
                    state[i][j] == state[i][j + 3]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1
    # check columns
    for j in range(7):
        for i in range(3):
            if state[i][j] != '0' and state[i][j] == state[i + 1][j] and state[i][j] == state[i + 2][j] and \
                    state[i][j] == state[i + 3][j]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1
    # check diagonals
    for i in range(3):
        for j in range(4):
            if state[i][j] != '0' and state[i][j] == state[i + 1][j + 1] and state[i][j] == state[i + 2][j + 2] and \
                    state[i][j] == state[i + 3][j + 3]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1
    for i in range(3):
        for j in range(6, 2, -1):
            if state[i][j] != '0' and state[i][j] == state[i + 1][j - 1] and state[i][j] == state[i + 2][j - 2] and \
                    state[i][j] == state[i + 3][j - 3]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1

    return agent, user

def get_search_tree(map):  # {state, [h, p]}):0'''
    pass


def check_children(state, flag):
    children = getchildren(state, flag)
    agent, user = getScore(state)
    result = 0

    for child in children:
        newAgent, newUser = getScore(child)
        if flag == 1:
            result -= newUser - user
        else:
            result += newAgent - agent

    return result


def check_zeros(state, flag):
    result = 0
    agent, user = getScore(state)
    for i in range(6):
        for j in range(7):
            if state[i][j] == '0':
                newState = [state[z].copy() for z in range(6)]
                if flag == '1':
                    newState[i][j] = '1'
                    newUser = getScore(newState)[1]
                    result -= newUser - user

                else:
                    newState[i][j] = '2'
                    newAgent = getScore(newState)[0]
                    result += newAgent - agent

    return result


def checkThree(state: list[list[str]], flag: str) -> int:
    for i in range(6):
        for j in range(3):
            # 0,1,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == flag and state[i][j + 2] == flag and\
                    state[i][j + 3] == flag and state[i][j + 4] == '0':
                if i == 0:
                    return 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 4] != '0':
                        return 1
    return 0

def checkDefiniteFour(state: list[list[str]], flag: str) -> int:
    for i in range(1,6):
        for j in range(4):
            #0,1,1,1
            #0,1,1,1
            if state[i][j] == '0' and state[i][j + 1] == flag and state[i][j + 2] == flag and state[i][j + 3] == flag:
                if state[i-1][j] == '0' and state[i-1][j + 1] == flag and state[i-1][j + 2] == flag and state[i-1][j + 3] == flag:
                    return 1
            #1,1,1,0
            #1,1,1,0
            if state[i][j] == flag and state[i][j + 1] == flag and state[i][j + 2] == flag and state[i][j + 3] == '0':
                if state[i-1][j] == flag and state[i-1][j + 1] == flag and state[i-1][j + 2] == flag and state[i-1][j + 3] == '0':
                    return 1
            # 1,0,1,1
            # 1,0,1,1
            if state[i][j] == flag and state[i][j + 1] == '0' and state[i][j + 2] == flag and state[i][j + 3] == flag:
                if state[i-1][j] == flag and state[i-1][j + 1] == '0' and state[i-1][j + 2] == flag and state[i-1][j + 3] == flag:
                    return 1
            #1,1,0,1
            #1,1,0,1
            if state[i][j] == flag and state[i][j + 1] == flag and state[i][j + 2] == '0' and state[i][j + 3] == flag:
                if state[i-1][j] == flag and state[i-1][j + 1] == flag and state[i-1][j + 2] == '0' and state[i-1][j + 3] == flag:
                    return 1
    return 0

def checkDefiniteTwo(state: list[list[str]]) -> int:
    for i in range(6):
        for j in range(3):
            # 0,0,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == '0' and state[i][j + 2] == '1' and state[i][j + 3] == '1' and state[i][j + 4] == '0':
                if i == 0:
                    return 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 1] != '0' and state[i - 1][j + 4] != '0':
                        return 1
            # 0,1,1,0,0
            if state[i][j] == '0' and state[i][j + 1] == '1' and state[i][j + 2] == '1' and state[i][j + 3] == '0' and state[i][j + 4] == '0':
                if i == 0:
                    return 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 3] != '0' and state[i - 1][j + 4] != '0':
                        return 1
    return 0

if __name__ == '__main__':
    flag = 2
    state = [['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1']]
    # print(state)
    # getchildren(state, flag)
    x = is_full(state)
    print(x)