import sys
from treelib import Tree


def heuristic(state: list[list[str]]) -> int:
    score = getScore(state)
    heu = 100 * (score[0] - score[1])
    if is_full(state):
        return heu

    heu -= 10 * checkDefiniteTwo(state)
    definite_four = checkDefiniteFour(state)
    heu += 10 * definite_four[0]
    heu -= 15 * definite_four[1]
    definite_three_in_row = checkDefiniteThreeInRow(state)
    heu += 10 * definite_three_in_row[0]
    heu -= 15 * definite_three_in_row[1]
    definite_three_in_diagonal = checkDefiniteThreeInDiagonal(state)
    heu += 5 * definite_three_in_diagonal[0]
    heu -= 10 * definite_three_in_diagonal[1]
    three = checkThree(state)
    heu += 3 * three[0]
    heu -= 5 * three[1]
    two = checkTwo(state)
    heu += 2 * two[0]
    heu -= 2 * two[1]
    return heu


def is_full(state: list[list[str]]) -> bool:
    for col in range(7):
        if state[-1][col] == '0':
            return False
    return True


def transpose(state: list[list[str]]):
    new_state = [['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0']]

    for col in range(6):

        for row in range(6):
            new_state[col][row] = state[row][col]

    for i in range(6):
        new_state[6][i] = state[i][6]

    return new_state


def transpose2(state: list[list[str]]):
    new_state = [['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0']]
    for row in range(6):

        for col in range(6):
            new_state[row][col] = state[col][row]

    for i in range(6):
        new_state[i][6] = state[6][i]

    return new_state


def decode_state(encoded):
    decoded = [['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0']]

    for col in range(6, -1, -1):
        column = encoded & 0b1111111111
        last_piece = column >> 6

        col_str = format(column, '10b')

        last_piece = last_piece - 8

        for row in range(4, 4 + last_piece):

            bit = col_str[row]

            if bit == '0':
                decoded[col][row - 4] = '1'

            elif bit == '1':
                decoded[col][row - 4] = '2'

            column << 1
        encoded = encoded >> 10

    decoded = transpose2(decoded)

    return decoded


def encode_state(state: list[list[str]]):
    encoded_state = 0b000000000

    state = transpose(state)

    for col in range(7):
        flag = 0
        encoded_col = 0b0
        last_piece = 0b000

        for row in range(6):
            if state[col][row] == '0':
                last_piece = row
                flag = 1

                if last_piece == 0:
                    last_piece = 8
                elif last_piece == 1:
                    last_piece = 9
                elif last_piece == 2:
                    last_piece = 10
                elif last_piece == 3:
                    last_piece = 11
                elif last_piece == 4:
                    last_piece = 12
                elif last_piece == 5:
                    last_piece = 13

                for i in range(6 - row):
                    encoded_col = encoded_col << 1
                break

            else:
                if state[col][row] == '1':
                    encoded_col = encoded_col << 1

                if state[col][row] == '2':
                    encoded_col = (encoded_col << 1) | 1

        if flag == 0:
            last_piece = 14

        last_piece = (last_piece << 6) | encoded_col
        encoded_state = (encoded_state << 10) | last_piece

    return encoded_state


def getchildren(state: list[list[str]], flag: str) -> list[list[list[str]]]:
    children = []
    for col in range(7):
        for row in range(6):
            x = state[row][col]
            if x == '0':
                child = [state[i].copy() for i in range(6)]
                if flag == '1':
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
    # check diagonals from the left
    for i in range(3):
        for j in range(4):
            if state[i][j] != '0' and state[i][j] == state[i + 1][j + 1] and state[i][j] == state[i + 2][j + 2] and \
                    state[i][j] == state[i + 3][j + 3]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1
    # check diagonals from the right
    for i in range(3):
        for j in range(6, 2, -1):
            if state[i][j] != '0' and state[i][j] == state[i + 1][j - 1] and state[i][j] == state[i + 2][j - 2] and \
                    state[i][j] == state[i + 3][j - 3]:
                if state[i][j] == '1':
                    user += 1
                if state[i][j] == '2':
                    agent += 1
    return agent, user


def checkDefiniteTwo(state: list[list[str]], flag: str) -> tuple:
    agent = 0
    user = 0
    for i in range(6):
        for j in range(3):
            # 0,0,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == '0' and state[i][j + 2] == flag and\
                    state[i][j + 3] == flag and state[i][j + 4] == '0':
                if i == 0:
                    if state[i][j + 2] == '1':
                        user += 1
                    elif state[i][j + 2] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 1] != '0' and state[i - 1][j + 4] != '0':
                        if state[i][j + 2] == '1':
                            user += 1
                        elif state[i][j + 2] == '2':
                            agent += 1
            # 0,1,1,0,0
            if state[i][j] == '0' and state[i][j + 1] == flag and state[i][j + 2] == flag and\
                    state[i][j + 3] == '0' and state[i][j + 4] == '0':
                if i == 0:
                    if state[i][j + 1] == '1':
                        user += 1
                    elif state[i][j + 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 3] != '0' and state[i - 1][j + 4] != '0':
                        if state[i][j + 1] == '1':
                            user += 1
                        elif state[i][j + 1] == '2':
                            agent += 1

    for i in range(2):
        for j in range(3):
            #             0
            #          0
            #       1
            #    1
            # 0
            if state[i][j] == '0' and state[i + 3][j + 3] == '0' and state[i + 4][j + 4] == '0' and\
                    state[i + 1][j + 1] == flag and state[i + 2][j + 2] == flag:
                if i == 0 and state[i + 2][j + 3] != '0' and state[i + 3][j + 4] != '0':
                    if state[i + 1][j + 1] == '1':
                        user += 1
                    elif state[i + 1][j + 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i + 2][j + 3] != '0' and state[i + 3][j + 4] != '0':
                        if state[i + 1][j + 1] == '1':
                            user += 1
                        elif state[i + 1][j + 1] == '2':
                            agent += 1
            #             0
            #          1
            #       1
            #    0
            # 0
            if state[i][j] == '0' and state[i + 1][j + 1] == '0' and state[i + 4][j + 4] == '0' and\
                    state[i + 2][j + 2] == flag and state[i + 3][j + 3] == flag:
                if i == 0 and state[i][j + 1] != '0' and state[i + 3][j + 4] != '0':
                    if state[i + 2][j + 2] == '1':
                        user += 1
                    elif state[i + 2][j + 2] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i][j + 1] != '0' and state[i + 3][j + 4] != '0':
                        if state[i + 2][j + 2] == '1':
                            user += 1
                        elif state[i + 2][j + 2] == '2':
                            agent += 1

    for i in range(2):
        for j in range(6, 3, -1):
            # 0
            #   0
            #     1
            #       1
            #         0
            if state[i][j] == '0' and state[i + 3][j - 3] == '0' and state[i + 4][j - 4] == '0' and\
                    state[i + 1][j - 1] == flag and state[i + 2][j - 2] == flag:
                if i == 0 and state[i + 2][j - 3] != '0' and state[i + 3][j - 4] != '0':
                    if state[i + 1][j - 1] == '1':
                        user += 1
                    elif state[i + 1][j - 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i + 2][j - 3] != '0' and state[i + 3][j - 4] != '0':
                        if state[i + 1][j - 1] == '1':
                            user += 1
                        elif state[i + 1][j - 1] == '2':
                            agent += 1
            # 0
            #   1
            #     1
            #       0
            #         0
            if state[i][j] == '0' and state[i + 1][j - 1] == '0' and state[i + 4][j - 4] == '0' and\
                    state[i + 2][j - 2] == flag and state[i + 3][j - 3] == flag:
                if i == 0 and state[i][j - 1] != '0' and state[i + 3][j - 4] != '0':
                    if state[i + 2][j - 2] == '1':
                        user += 1
                    elif state[i + 2][j - 2] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i][j - 1] != '0' and state[i + 3][j - 4] != '0':
                        if state[i + 2][j - 2] == '1':
                            user += 1
                        elif state[i + 2][j - 2] == '2':
                            agent += 1

    return agent, user


def checkDefiniteThreeInRow(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    for i in range(6):
        for j in range(3):
            # 0,1,1,1,0
            if state[i][j] == '0' and state[i][j + 1] != '0' and state[i][j + 2] == state[i][j + 1] and \
                    state[i][j + 3] == state[i][j + 1] and state[i][j + 4] == '0':
                if i == 0:
                    if state[i][j + 1] == '1':
                        user += 1
                    elif state[i][j + 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i - 1][j + 4] != '0':
                        if state[i][j + 1] == '1':
                            user += 1
                        elif state[i][j + 1] == '2':
                            agent += 1
    return agent, user


def checkDefiniteThreeInDiagonal(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    #               0
    #           1
    #       1
    #   1
    # 0
    for i in range(2):
        for j in range(3):
            if state[i][j] == '0' and state[i + 4][j + 4] == '0' and state[i + 1][j + 1] != '0' and \
                    state[i + 1][j + 1] == state[i + 2][j + 2] and state[i + 1][j + 1] == state[i + 3][j + 3]:
                if i == 0 and state[i + 3][j + 4] != '0':
                    if state[i + 1][j + 1] == '1':
                        user += 1
                    elif state[i + 1][j + 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i + 3][j + 4] != '0':
                        if state[i + 1][j + 1] == '1':
                            user += 1
                        elif state[i + 1][j + 1] == '2':
                            agent += 1
    # 0
    #   1
    #       1
    #           1
    #               0
    for i in range(2):
        for j in range(6, 3, -1):
            if state[i][j] == '0' and state[i + 4][j - 4] == '0' and state[i + 1][j - 1] != '0' and \
                    state[i + 1][j - 1] == state[i + 2][j - 2] and state[i + 1][j - 1] == state[i + 3][j - 3]:
                if i == 0 and state[i + 3][j - 4] != '0':
                    if state[i + 1][j - 1] == '1':
                        user += 1
                    elif state[i + 1][j - 1] == '2':
                        agent += 1
                else:
                    if state[i - 1][j] != '0' and state[i + 3][j - 4] != '0':
                        if state[i + 1][j - 1] == '1':
                            user += 1
                        elif state[i + 1][j - 1] == '2':
                            agent += 1
    return agent, user


def checkDefiniteFour(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    for i in range(1, 6):
        for j in range(4):
            # 0,1,1,1
            # 0,1,1,1
            if state[i][j] == '0' and state[i][j + 1] != '0' and state[i][j + 1] == state[i][j + 2] and \
                    state[i][j + 1] == state[i][j + 3]:
                if state[i - 1][j] == '0' and state[i - 1][j + 1] == state[i][j + 1] and state[i][j + 1] == \
                        state[i - 1][j + 2] and state[i][j + 1] == state[i - 1][j + 3]:
                    if state[i][j + 1] == '1':
                        user += 1
                    elif state[i][j + 1] == '2':
                        agent += 1
            # 1,1,1,0
            # 1,1,1,0
            if state[i][j] != '0' and state[i][j] == state[i][j + 1] and state[i][j] == state[i][j + 2] and \
                    state[i][j + 3] == '0':
                if state[i - 1][j] == state[i][j] and state[i - 1][j + 1] == state[i][j] and state[i - 1][j + 2] == \
                        state[i][j] and state[i - 1][j + 3] == '0':
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            # 1,0,1,1
            # 1,0,1,1
            if state[i][j] != '0' and state[i][j + 1] == '0' and state[i][j] == state[i][j + 2] and state[i][j] == \
                    state[i][j + 3]:
                if state[i - 1][j] == state[i][j] and state[i - 1][j + 1] == '0' and \
                        state[i][j] == state[i - 1][j + 2] and state[i][j] == state[i - 1][j + 3]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            # 1,1,0,1
            # 1,1,0,1
            if state[i][j] != '0' and state[i][j] == state[i][j + 1] and state[i][j + 2] == '0' and state[i][j] == \
                    state[i][j + 3]:
                if state[i - 1][j] == state[i][j] and state[i - 1][j + 1] == state[i][j] and \
                        state[i - 1][j + 2] == '0' and state[i - 1][j + 3] == state[i][j]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1

    for i in range(1, 3):
        for j in range(4):
            #       0
            #     1 0
            #   1 1
            # 1 1
            # 1
            if state[i + 3][j + 3] == '0' and state[i][j] != '0' and state[i][j] == state[i + 1][j + 1] and \
                    state[i][j] == state[i + 2][j + 2]:
                if state[i + 2][j + 3] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i][j + 1] and state[i - 1][j] == state[i + 1][j + 2]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            #       1
            #     0 1
            #   1 0
            # 1 1
            # 1
            if state[i + 2][j + 2] == '0' and state[i][j] != '0' and state[i][j] == state[i + 1][j + 1] and \
                    state[i][j] == state[i + 3][j + 3]:
                if state[i + 1][j + 2] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i][j + 1] and state[i - 1][j] == state[i + 2][j + 3]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            #       1
            #     1 1
            #   0 1
            # 1 0
            # 1
            if state[i + 1][j + 1] == '0' and state[i][j] != '0' and state[i][j] == state[i + 2][j + 2] and \
                    state[i][j] == state[i + 3][j + 3]:
                if state[i][j + 1] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i + 1][j + 2] and state[i - 1][j] == state[i + 2][j + 3]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            #       1
            #     1 1
            #   1 1
            # 0 1
            # 0
            if state[i][j] == '0' and state[i + 1][j + 1] != '0' and state[i + 1][j + 1] == state[i + 2][j + 2] and \
                    state[i + 1][j + 1] == state[i + 3][j + 3]:
                if state[i - 1][j] == '0' and state[i][j + 1] == state[i + 1][j + 1] and state[i][j + 1] == \
                        state[i + 1][j + 2] and state[i][j + 1] == state[i + 2][j + 3]:
                    if state[i + 1][j + 1] == '1':
                        user += 1
                    elif state[i + 1][j + 1] == '2':
                        agent += 1

    for i in range(1, 3):
        for j in range(6, 2, -1):
            # 0
            # 0 1
            #   1 1
            #     1 1
            #       1
            if state[i + 3][j - 3] == '0' and state[i][j] != '0' and state[i][j] == state[i + 1][j - 1] and \
                    state[i][j] == state[i + 2][j - 2]:
                if state[i + 2][j - 3] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i][j - 1] and state[i - 1][j] == state[i + 1][j - 2]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            # 1
            # 1 0
            #   0 1
            #     1 1
            #       1
            if state[i + 2][j - 2] == '0' and state[i][j] != '0' and state[i][j] == state[i + 1][j - 1] and \
                    state[i][j] == state[i - 3][j - 3]:
                if state[i + 1][j - 2] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i][j - 1] and state[i - 1][j] == state[i + 2][j - 3]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            # 1
            # 1 1
            #   1 0
            #     0 1
            #       1
            if state[i + 1][j - 1] == '0' and state[i][j] != '0' and state[i][j] == state[i + 2][j - 2] and state[i][
                j] == state[i + 3][j - 3]:
                if state[i][j - 1] == '0' and state[i - 1][j] == state[i][j] and \
                        state[i - 1][j] == state[i + 1][j - 2] and state[i - 1][j] == state[i + 2][j - 3]:
                    if state[i][j] == '1':
                        user += 1
                    elif state[i][j] == '2':
                        agent += 1
            # 1
            # 1 1
            #   1 1
            #     1 0
            #       0
            if state[i][j] == '0' and state[i + 1][j - 1] != '0' and state[i + 1][j - 1] == state[i + 2][j - 2] and \
                    state[i + 1][j - 1] == state[i + 3][j - 3]:
                if state[i - 1][j] == '0' and state[i][j - 1] == state[i + 1][j - 1] and state[i][j - 1] == \
                        state[i + 1][j - 2] and state[i][j - 1] == state[i + 2][j - 3]:
                    if state[i + 1][j - 1] == '1':
                        user += 1
                    elif state[i + 1][j - 1] == '2':
                        agent += 1

    return agent, user


def checkThree(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    # check rows
    for i in range(6):
        for j in range(4):
            # 0,1,1,1
            if state[i][j] == '0' and state[i][j + 1] != '0' and state[i][j + 2] == state[i][j + 1] and \
                    state[i][j + 3] == state[i][j + 1]:
                if state[i][j + 1] == '1':
                    user += 1
                elif state[i][j + 1] == '2':
                    agent += 1
            # 1,1,1,0
            if state[i][j] != '0' and state[i][j + 1] == state[i][j] and state[i][j + 2] == state[i][j] and state[i][
                j + 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
    # check columns
    for j in range(7):
        for i in range(3):
            # 0
            # 1
            # 1
            # 1
            if state[i][j] != '0' and state[i + 1][j] == state[i][j] and state[i + 2][j] == state[i][j] and \
                    state[i + 3][j] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
    # check diagonals from the left
    for i in range(3):
        for j in range(4):
            if state[i][j] != '0' and state[i + 1][j + 1] == state[i][j] and state[i + 2][j + 2] == state[i][j] and \
                    state[i + 3][j + 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
            if state[i][j] == '0' and state[i + 1][j + 1] != '0' and state[i + 2][j + 2] == state[i + 1][j + 1] and \
                    state[i + 3][j + 3] == state[i + 1][j + 1]:
                if state[i + 1][j + 1] == '1':
                    user += 1
                elif state[i + 1][j + 1] == '2':
                    agent += 1
    # check diagonals from the right
    for i in range(3):
        for j in range(6, 2, -1):
            if state[i][j] != '0' and state[i + 1][j - 1] == state[i][j] and state[i + 2][j - 2] == state[i][j] and \
                    state[i + 3][j - 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
            if state[i][j] == '0' and state[i + 1][j - 1] != '0' and state[i + 2][j - 2] == state[i + 1][j - 1] and \
                    state[i + 3][j - 3] == state[i + 1][j - 1]:
                if state[i + 1][j - 1] == '1':
                    user += 1
                elif state[i + 1][j - 1] == '2':
                    agent += 1
    return agent, user


def checkTwo(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    # check rows
    for i in range(6):
        for j in range(4):
            # 0,0,1,1
            if state[i][j] == '0' and state[i][j + 1] == '0' and state[i][j + 2] != '0' and \
                    state[i][j + 3] == state[i][j + 2]:
                if state[i][j + 2] == '1':
                    user += 1
                elif state[i][j + 2] == '2':
                    agent += 1
            # 1,1,0,0
            if state[i][j] != '0' and state[i][j + 1] == state[i][j] and state[i][j + 2] == '0' and\
                    state[i][j + 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
            # 0,1,1,0
            if state[i][j] == '0' and state[i][j + 3] == '0' and state[i][j + 1] != '0' and \
                    state[i][j + 2] == state[i][j + 1]:
                if state[i][j + 1] == '1':
                    user += 1
                elif state[i][j + 1] == '2':
                    agent += 1
    # check columns
    for j in range(7):
        for i in range(3):
            # 0
            # 1
            # 1
            if state[i][j] != '0' and state[i + 1][j] == state[i][j] and state[i + 2][j] == '0' and i + 3 < 6:
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
    # check diagonals from the left
    for i in range(3):
        for j in range(4):
            #      0
            #    0
            #  1
            # 1
            if state[i][j] != '0' and state[i + 1][j + 1] == state[i][j] and state[i + 2][j + 2] == '0' and \
                    state[i + 3][j + 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
            #      0
            #    1
            #  1
            # 0
            if state[i][j] == '0' and state[i + 3][j + 3] == '0' and state[i + 1][j + 1] != '0' and \
                    state[i + 2][j + 2] == state[i + 1][j + 1]:
                if state[i + 1][j + 1] == '1':
                    user += 1
                elif state[i + 1][j + 1] == '2':
                    agent += 1
            #       1
            #    1
            #  0
            # 0
            if state[i][j] == '0' and state[i + 1][j + 1] == '0' and state[i + 2][j + 2] != '0' and \
                    state[i + 3][j + 3] == state[i + 2][j + 2]:
                if state[i + 2][j + 2] == '1':
                    user += 1
                elif state[i + 2][j + 2] == '2':
                    agent += 1
    # check diagonals from the right
    for i in range(3):
        for j in range(6, 2, -1):
            # 0
            #  0
            #    1
            #      1
            if state[i][j] != '0' and state[i + 1][j - 1] == state[i][j] and state[i + 2][j - 2] == '0' and \
                    state[i + 3][j - 3] == '0':
                if state[i][j] == '1':
                    user += 1
                elif state[i][j] == '2':
                    agent += 1
            # 0
            #  1
            #    1
            #      0
            if state[i][j] == '0' and state[i + 3][j - 3] == '0' and state[i + 1][j - 1] != '0' and\
                    state[i + 2][j - 2] == state[i + 1][j - 1]:
                if state[i + 1][j - 1] == '1':
                    user += 1
                elif state[i + 1][j - 1] == '2':
                    agent += 1
            # 1
            #   1
            #     0
            #       0
            if state[i][j] == '0' and state[i + 1][j - 1] == '0' and state[i + 2][j - 2] != '0' and\
                    state[i + 3][j - 3] == state[i + 2][j - 2]:
                if state[i + 2][j - 2] == '1':
                    user += 1
                elif state[i + 2][j - 2] == '2':
                    agent += 1
    return agent, user


def minimax(state, k: int, pruning: bool, showTree: bool):
    alpha = -sys.maxsize
    beta = sys.maxsize

    tree = Tree()
    identifier = 1

    def minmax(state, k: int, flag: str, parent):
        nonlocal tree
        nonlocal identifier
        c = 0
        state = decode_state(state)
        if k == 1 and flag == '2':
            maximum = -sys.maxsize
            children = getchildren(state, '2')
            for child in children:
                h = heuristic(child)
                tree.create_node(str(h), parent=parent.identifier)
                if h > maximum:
                    maximum = h
                    c = child
                    parent.tag = "Max " + str(maximum)
            return c, maximum

        if k == 1 and flag == '1':
            minimum = sys.maxsize
            children = getchildren(state, '1')
            for child in children:
                h = heuristic(state)
                tree.create_node(str(h), parent=parent.identifier)
                if h < minimum:
                    minimum = h
                    c = child
                    parent.tag = "Min " + str(minimum)
            return c, minimum

        if flag == '2':
            children = getchildren(state, '2')
            maximum = -sys.maxsize
            for child in children:
                parent_id = parent.identifier
                parent = tree.create_node("Max", identifier, parent)
                identifier += 1
                value = minmax(encode_state(child), k - 1, '1', parent)
                maximum = max(maximum, value[1])
                parent = tree.get_node(parent_id)
                if maximum == value[1]:
                    c = child
                    parent.tag = "Max " + str(maximum)

            return c, maximum

        if flag == '1':
            children = getchildren(state, '1')
            minimum = sys.maxsize
            for child in children:
                parent_id = parent.identifier
                parent = tree.create_node("Min", identifier, parent)
                identifier += 1
                value = minmax(encode_state(child), k - 1, '2', parent)
                minimum = min(minimum, value[1])
                parent = tree.get_node(parent_id)
                if minimum == value[1]:
                    c = child
                    parent.tag = "Min " + str(minimum)

            return c, minimum

    def minmaxPruning(state, k: int, flag: str, alpha, beta, parent):
        nonlocal tree
        nonlocal identifier

        state = decode_state(state)
        c = 0
        if k == 1 and flag == '2':
            maximum = -sys.maxsize
            children = getchildren(state, '2')
            for child in children:
                h = heuristic(child)
                tree.create_node(str(h), parent=parent.identifier)
                if h > maximum:
                    maximum = h
                    c = child
                    parent.tag = "Max " + str(maximum)
                alpha = max(alpha, h)
                if beta <= alpha:
                    break
            return c, maximum

        if k == 1 and flag == '1':
            minimum = sys.maxsize
            children = getchildren(state, '1')
            for child in children:
                h = heuristic(child)
                tree.create_node(str(h), parent=parent.identifier)
                if h < minimum:
                    minimum = h
                    c = child
                    parent.tag = "Min " + str(minimum)
                beta = min(beta, h)
                if beta <= alpha:
                    break
            return c, minimum

        if flag == '2':
            children = getchildren(state, '2')
            maximum = -sys.maxsize
            for child in children:
                parent_id = parent.identifier
                parent = tree.create_node("Max", identifier, parent)
                identifier += 1
                value = minmaxPruning(encode_state(child), k - 1, '1', alpha, beta, parent)
                maximum = max(maximum, value[1])
                alpha = max(alpha, value[1])
                parent = tree.get_node(parent_id)
                if maximum == value[1]:
                    c = child
                    parent.tag = "Max " + str(maximum)

                if beta <= alpha:
                    break
            return c, maximum

        if flag == '1':
            children = getchildren(state, '1')
            minimum = sys.maxsize
            for child in children:
                parent_id = parent.identifier
                parent = tree.create_node("Min", identifier, parent)
                identifier += 1
                value = minmaxPruning(encode_state(child), k - 1, '2', alpha, beta, parent)
                minimum = min(minimum, value[1])
                beta = min(beta, value[1])
                parent = tree.get_node(parent_id)
                if minimum == value[1]:
                    c = child
                    parent.tag = "Min " + str(minimum)

                if beta <= alpha:
                    break

            return c, minimum

    result = minmaxPruning(state, k, '2', alpha, beta, tree.create_node("Max", 0)) if pruning else \
        minmax(state, k, '2', tree.create_node("Max", 0))

    if showTree:
        tree.show()
        file = open("Tree.txt", 'r+')
        file.truncate(0)
        file.close()
        tree.save2file("Tree.txt")

    return result
