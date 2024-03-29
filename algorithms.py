import sys
from treelib import Tree
import random


def check_children(state, flag):
    children = getchildren(state, flag)
    agent, user = getScore(state)
    result = 0

    for child in children:
        newAgent, newUser = getScore(child)
        if flag == '1':
            result -= newUser - user
        else:
            result += newAgent - agent
    return result


def heuristic(state: list[list[str]], turn: int) -> int:
    score = getScore(state)
    heu = 1000 * (score[0] - score[1])

    if turn == 1:
        definite_two = checkDefiniteTwo(state)
        heu += 50 * definite_two[0]
        heu -= 1000 * definite_two[1]
        definite_four = checkDefiniteFour(state)
        heu += 1000 * definite_four[0]
        heu -= 1000 * definite_four[1]
        definite_three_in_row = checkDefiniteThreeInRow(state)
        heu += 1000 * definite_three_in_row[0]
        heu -= 1000 * definite_three_in_row[1]
        definite_three_in_diagonal = checkDefiniteThreeInDiagonal(state)
        heu += 1000 * definite_three_in_diagonal[0]
        heu -= 1000 * definite_three_in_diagonal[1]
        three = checkThree(state)
        heu += 10 * three[0]
        heu -= 100 * three[1]
        columns = checkColumn(state)
        heu += 500 * columns[0]
        heu -= 1000 * columns[1]
        two = checkTwo(state)
        heu += 10 * two[0]
        heu -= 100 * two[1]

    else:
        definite_two = checkDefiniteTwo(state)
        heu += 100 * definite_two[0]
        heu -= 50 * definite_two[1]
        definite_four = checkDefiniteFour(state)
        heu += 1000 * definite_four[0]
        heu -= 1000 * definite_four[1]
        definite_three_in_row = checkDefiniteThreeInRow(state)
        heu += 1000 * definite_three_in_row[0]
        heu -= 1000 * definite_three_in_row[1]
        definite_three_in_diagonal = checkDefiniteThreeInDiagonal(state)
        heu += 1000 * definite_three_in_diagonal[0]
        heu -= 1000 * definite_three_in_diagonal[1]
        three = checkThree(state)
        heu += 100 * three[0]
        heu -= 10 * three[1]
        columns = checkColumn(state)
        heu += 1000 * columns[0]
        heu -= 500 * columns[1]
        two = checkTwo(state)
        heu += 100 * two[0]
        heu -= 10 * two[1]
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
    random.shuffle(children)
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


def checkDefiniteTwo(state: list[list[str]]) -> tuple:
    agent = 0
    user = 0
    for i in range(6):
        for j in range(3):
            # 0,0,1,1,0
            if state[i][j] == '0' and state[i][j + 1] == '0' and state[i][j + 2] != '0' and \
                    state[i][j + 3] == state[i][j + 2] and state[i][j + 4] == '0':
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
            if state[i][j] == '0' and state[i][j + 1] != '0' and state[i][j + 2] == state[i][j + 1] and \
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
            if state[i][j] == '0' and state[i + 3][j + 3] == '0' and state[i + 4][j + 4] == '0' and \
                    state[i + 1][j + 1] != '0' and state[i + 2][j + 2] == state[i + 1][j + 1]:
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
            if state[i][j] == '0' and state[i + 1][j + 1] == '0' and state[i + 4][j + 4] == '0' and \
                    state[i + 2][j + 2] != '0' and state[i + 3][j + 3] == state[i + 2][j + 2]:
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
            if state[i][j] == '0' and state[i + 3][j - 3] == '0' and state[i + 4][j - 4] == '0' and \
                    state[i + 1][j - 1] != '0' and state[i + 2][j - 2] == state[i + 1][j - 1]:
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
            if state[i][j] == '0' and state[i + 1][j - 1] == '0' and state[i + 4][j - 4] == '0' and state[i + 2][
                j - 2] != '0' and state[i + 3][j - 3] == state[i + 2][j - 2]:
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


def checkColumn(state: list[list[str]]) -> tuple:
    user = 0
    agent = 0
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
                    if i == 0:
                        user += 9
                    elif state[i - 1][j] != '0':
                        user += 9
                elif state[i][j + 1] == '2':
                    agent += 1
                    if i == 0:
                        agent += 9
                    elif state[i - 1][j] != '0':
                        agent += 9
            # 1,1,1,0
            if state[i][j] != '0' and state[i][j + 1] == state[i][j] and state[i][j + 2] == state[i][j] and \
                    state[i][j + 3] == '0':
                if state[i][j] == '1':
                    user += 1
                    if i == 0:
                        user += 9
                    elif state[i - 1][j + 3] != '0':
                        user += 9
                elif state[i][j] == '2':
                    agent += 1
                    if i == 0:
                        agent += 9
                    elif state[i - 1][j + 3] != '0':
                        agent += 9

            # 1, 0, 1, 1
            if state[i][j] != '0' and state[i][j + 1] == '0' and state[i][j + 2] == state[i][j] and \
                    state[i][j + 3] == state[i][j]:
                if state[i][j] == '1':
                    user += 1
                    if i == 0:
                        user += 9
                    elif state[i - 1][j + 1] != '0':
                        user += 9
                elif state[i][j] == '2':
                    agent += 1
                    if i == 0:
                        agent += 9
                    elif state[i - 1][j + 1] != '0':
                        agent += 9

            # 1, 1, 0, 1
            if state[i][j] != '0' and state[i][j + 1] == state[i][j] and state[i][j + 2] == '0' and \
                    state[i][j + 3] == state[i][j]:
                if state[i][j] == '1':
                    user += 1
                    if i == 0:
                        user += 9
                    elif state[i - 1][j + 2] != '0':
                        user += 9
                elif state[i][j] == '2':
                    agent += 1
                    if i == 0:
                        agent += 9
                    elif state[i - 1][j + 2] != '0':
                        agent += 9

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
            if state[i][j] != '0' and state[i][j + 1] == state[i][j] and state[i][j + 2] == '0' and \
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
            if state[i][j] == '0' and state[i + 3][j - 3] == '0' and state[i + 1][j - 1] != '0' and \
                    state[i + 2][j - 2] == state[i + 1][j - 1]:
                if state[i + 1][j - 1] == '1':
                    user += 1
                elif state[i + 1][j - 1] == '2':
                    agent += 1
            # 1
            #   1
            #     0
            #       0
            if state[i][j] == '0' and state[i + 1][j - 1] == '0' and state[i + 2][j - 2] != '0' and \
                    state[i + 3][j - 3] == state[i + 2][j - 2]:
                if state[i + 2][j - 2] == '1':
                    user += 1
                elif state[i + 2][j - 2] == '2':
                    agent += 1
    return agent, user


def minimax(state, k: int, pruning: bool, showTree: bool):
    alpha = float('-inf')
    beta = float('inf')

    tree = Tree()
    identifier = 0

    def minmax(state, k: int, flag: str, parent):
        nonlocal tree
        nonlocal identifier
        c = 0
        state = decode_state(state)

        if is_full(state):
            score = getScore(state)
            h = score[0] - score[1]
            tree.create_node(str(h), parent=parent.identifier)
            identifier += 1
            parent.tag = "Max " + str(h) if flag == '2' else "Min " + str(h)
            return state, h

        if k == 1 and flag == '2':
            maximum = -sys.maxsize
            children = getchildren(state, '2')
            for child in children:
                h = heuristic(child, 1)
                tree.create_node(str(h) + ' state= ' + child.__str__(), parent=parent.identifier)
                identifier += 1
                if h > maximum:
                    maximum = h
                    c = child
                    parent.tag = "Max " + str(maximum) + ' state= ' + c.__str__()
            return c, maximum

        if k == 1 and flag == '1':
            minimum = sys.maxsize
            children = getchildren(state, '1')
            for child in children:
                h = heuristic(child, 2)
                tree.create_node(str(h) + ' state= ' + child.__str__(), parent=parent.identifier)
                identifier += 1
                if h < minimum:
                    minimum = h
                    c = child
                    parent.tag = "Min " + str(minimum) + ' state= ' + c.__str__()
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
                    parent.tag = "Max " + str(maximum) + ' state= ' + c.__str__()

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
                    parent.tag = "Min " + str(minimum) + ' state= ' + c.__str__()

            return c, minimum

    def minmaxPruning(state, k: int, flag: str, alpha, beta, parent):
        nonlocal tree
        nonlocal identifier

        state = decode_state(state)

        if is_full(state):
            score = getScore(state)
            h = score[0] - score[1]
            tree.create_node(str(h), parent=parent.identifier)
            identifier += 1
            parent.tag = "Max " + str(h) + ' alpha= ' + str(alpha) + ' beta= ' + str(
                beta) + ' state= ' + state.__str__() if flag == '2' else "Min " + str(h) + ' alpha= ' + str(
                alpha) + ' beta= ' + str(beta) + ' state= ' + state.__str__()
            return state, h

        c = 0
        if k == 1 and flag == '2':
            maximum = -sys.maxsize
            children = getchildren(state, '2')
            for child in children:
                h = heuristic(child, 1)
                alpha = max(alpha, h)
                tree.create_node(
                    str(h) + ' alpha= ' + str(alpha) + ' beta= ' + str(beta) + ' state= ' + child.__str__(),
                    parent=parent.identifier)
                identifier += 1
                if h > maximum:
                    maximum = h
                    c = child
                    parent.tag = "Max " + str(maximum) + ' alpha= ' + str(alpha) + ' beta= ' + str(
                        beta) + ' state= ' + c.__str__()
                if beta <= alpha:
                    break
            return c, maximum

        if k == 1 and flag == '1':
            minimum = sys.maxsize
            children = getchildren(state, '1')
            for child in children:
                h = heuristic(child, 2)
                beta = min(beta, h)
                tree.create_node(
                    str(h) + ' alpha= ' + str(alpha) + ' beta= ' + str(beta) + ' state= ' + child.__str__(),
                    parent=parent.identifier)
                identifier += 1
                if h < minimum:
                    minimum = h
                    c = child
                    parent.tag = "Min " + str(minimum) + ' alpha= ' + str(alpha) + ' beta= ' + str(
                        beta) + ' state= ' + c.__str__()
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
                alpha = max(alpha, maximum)
                parent = tree.get_node(parent_id)
                if maximum == value[1]:
                    c = child
                    parent.tag = "Max " + str(maximum) + ' alpha= ' + str(alpha) + ' beta= ' + str(
                        beta) + ' state= ' + child.__str__()

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
                beta = min(beta, minimum)
                parent = tree.get_node(parent_id)
                if minimum == value[1]:
                    c = child
                    parent.tag = "Min " + str(minimum) + ' alpha= ' + str(alpha) + ' beta= ' + str(
                        beta) + ' state= ' + child.__str__()

                if beta <= alpha:
                    break

            return c, minimum

    result = minmaxPruning(state, k, '2', alpha, beta, tree.create_node("Max", -1)) if pruning else \
        minmax(state, k, '2', tree.create_node("Max", -1))

    if showTree:
        file = open("Tree.txt", 'r+')
        file.truncate(0)
        file.close()
        tree.save2file("Tree.txt")

    return [result, identifier]
