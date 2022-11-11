import sys

def heuristic(state: list[list[str]]) -> int:
    score = getScore(state)
    h1 = score[0] - score[1]


def is_full(state: list[list[str]]) -> int:
    for col in range(7):
        for row in range(6):
            if state[row][col] == 0:
                return 0
    return 1


def getchildren(state: list[list[str]], flag: str) -> list[list[list[str]]]:
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
    result = 0
    for i in range(6):
        for j in range(3):
            # 0,1,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == flag and state[i][j + 2] == flag and\
                    state[i][j + 3] == flag and state[i][j + 4] == '0':
                if i == 0:
                    result += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 4] != '0':
                        result += 1
    return result

def checkDefiniteFour(state: list[list[str]], flag: str) -> int:
    result = 0
    for i in range(1,6):
        for j in range(4):
            #0,1,1,1
            #0,1,1,1
            if state[i][j] == '0' and state[i][j + 1] == flag and state[i][j + 2] == flag and state[i][j + 3] == flag:
                if state[i-1][j] == '0' and state[i-1][j + 1] == flag and state[i-1][j + 2] == flag and state[i-1][j + 3] == flag:
                    result += 1
            #1,1,1,0
            #1,1,1,0
            if state[i][j] == flag and state[i][j + 1] == flag and state[i][j + 2] == flag and state[i][j + 3] == '0':
                if state[i-1][j] == flag and state[i-1][j + 1] == flag and state[i-1][j + 2] == flag and state[i-1][j + 3] == '0':
                    result += 1
            # 1,0,1,1
            # 1,0,1,1
            if state[i][j] == flag and state[i][j + 1] == '0' and state[i][j + 2] == flag and state[i][j + 3] == flag:
                if state[i-1][j] == flag and state[i-1][j + 1] == '0' and state[i-1][j + 2] == flag and state[i-1][j + 3] == flag:
                    result += 1
            #1,1,0,1
            #1,1,0,1
            if state[i][j] == flag and state[i][j + 1] == flag and state[i][j + 2] == '0' and state[i][j + 3] == flag:
                if state[i-1][j] == flag and state[i-1][j + 1] == flag and state[i-1][j + 2] == '0' and state[i-1][j + 3] == flag:
                    result += 1
    return result

def checkDefiniteTwo(state: list[list[str]]) -> int:
    result = 0
    for i in range(6):
        for j in range(3):
            # 0,0,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == '0' and state[i][j + 2] == '1' and state[i][j + 3] == '1' and state[i][j + 4] == '0':
                if i == 0:
                    result += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 1] != '0' and state[i - 1][j + 4] != '0':
                        result += 1
            # 0,1,1,0,0
            if state[i][j] == '0' and state[i][j + 1] == '1' and state[i][j + 2] == '1' and state[i][j + 3] == '0' and state[i][j + 4] == '0':
                if i == 0:
                    result += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 3] != '0' and state[i - 1][j + 4] != '0':
                        result += 1
    return result

def max(state: list[list[str]], k: int):
    k = (2*k) -1
    def minmax(state: list[list[str]], k: int, flag: str):

        if k == 1:
            maximum = -sys.maxsize
            children = getchildren(state, '2')
            for child in children:
                h = heuristic(child)
                if h > maximum:
                    maximum = h
            return maximum
        c = 0
        if flag == '2':
            children = getchildren(state,'2')
            maximum = -sys.maxsize
            for child in children:
                value = minmax(child, k - 1, '1')
                maximum = max(maximum,value)
                c = child
            return [c,maximum]

        if flag == '1':
            children = getchildren(state,'1')
            minimum = sys.maxsize
            for child in children:
                value = minmax(child, k - 1, '2')
                minimum = min(minimum,value)
                c = child
            return [c,minimum]

    return minmax(state, k, '2')



if __name__ == '__main__':
    flag = 2
    state = [['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1']]
    # print(state)
    # getchildren(state, flag)
    x = is_full(state)
    print(x)