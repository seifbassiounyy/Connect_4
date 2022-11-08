import sys



def minimax(state, k):
    beststate = recursion(state, (2*k-1), 1)


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
            r = recursion(child, k-1, 0)
            value = r[1]
            if value > max:
                max = value

    elif flag == 1:
        children = getchildren(state)
        Min = sys.maxsize
        for child in children:
            value = recursion(child, k-1, 1)
            if value < Min:
                Min = value




def heuristic(state):
    score = get_score(state)
    h1 = score[0]-score[1]




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
                child = []
                for i in range(6):
                    child.append(state[i].copy())
                if flag == 1:
                    child[row][col] = 1
                    children.append(child)
                else:
                    child[row][col] = 2
                    children.append(child)
                break
                #for i  in range(6-row):

    print(children)


def get_score(state):
    pass


def get_search_tree(map):   #{state, [h, p]}):0'''
    pass



if __name__ == '__main__':
    flag = 2
    state = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]
    #print(state)
    #getchildren(state, flag)
    x = is_full(state)
    print(x)