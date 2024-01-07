import copy
import math
import random

playerX = "X"
playerO = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Player who has the next turn on a board.
    taken_places = 0

    for row in board:
        for place in row:
            if place is not None:
                taken_places += 1

    if taken_places % 2 == 0:
        return playerX
    else:
        return playerO


def actions(board):
    # All possible actions (i, j) available on the board.
    possible_actions = set()

    for i, row in enumerate(board):
        for j, place in enumerate(row):
            if place is None:
                possible_action = (i, j)
                possible_actions.add(possible_action)

    return possible_actions


def result(board, action):
    # Board that results from making move (i, j) on the board.
    result_board = copy.deepcopy(board)
    current_player = player(board)
    i = action[0]
    j = action[1]
    if result_board[i][j] is None:
        result_board[i][j] = current_player
        return result_board
    else:
        raise Exception("Illegal action. How did that even happen?!")


def winner(board):
    # Returns the winner, if there is one.
    for row in board:
        if row.count(row[0]) == 3 and row[0] != EMPTY:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[1][1]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    # True if game is over, False otherwise.
    if winner(board) is None:
        taken_places = 0
        for row in board:
            for place in row:
                if place is not None:
                    taken_places += 1
        if taken_places == 9:
            return True
        else:
            return False
    else:
        return True


def utility(board):
    # 1 if X has won the game, -1 if O has won, 0 otherwise.
    if winner(board) == playerX:
        return 1
    elif winner(board) == playerO:
        return -1
    else:
        return 0


def max_value(board):
    # Returns best value of a board
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    # Returns worst value of a board
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


# **********************
# Easy bot
# **********************
def easy(board):
    if terminal(board) is True:
        return None

    stupid_action = None
    val1 = -math.inf
    val2 = math.inf

    if player(board) == playerX:
        for action in actions(board):
            min_val = random.randint(0, 3)
            if min_val > val1:
                val1 = min_val
                stupid_action = action

    else:
        for action in actions(board):
            max_val = random.randint(0, 3)
            if max_val < val2:
                val2 = max_val
                stupid_action = action

    return stupid_action


# **********************
# Medium bot
# **********************
def medium(board):
    if terminal(board) is True:
        return None

    stupid_action = None
    optimal_action = None
    random_generator = random.randint(1, 100)
    val1 = -math.inf
    val2 = math.inf
    val3 = -math.inf
    val4 = math.inf

    if player(board) == playerX:
        for action in actions(board):
            min_val = random.randint(0, 3)
            if min_val > val1:
                val1 = min_val
                stupid_action = action

    else:
        for action in actions(board):
            max_val = random.randint(0, 3)
            if max_val < val2:
                val2 = max_val
                stupid_action = action

    if player(board) == playerX:
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > val3:
                val3 = min_val
                optimal_action = action

    else:
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < val4:
                val4 = max_val
                optimal_action = action

    if random_generator < 33:
        return stupid_action
    else:
        return optimal_action


# **********************
# Hard bot
# **********************
def hard(board):
    if terminal(board) is True:
        return None

    stupid_action = None
    optimal_action = None
    random_generator = random.randint(1, 100)
    val1 = -math.inf
    val2 = math.inf
    val3 = -math.inf
    val4 = math.inf

    if player(board) == playerX:
        for action in actions(board):
            min_val = random.randint(0, 3)
            if min_val > val1:
                val1 = min_val
                stupid_action = action

    else:
        for action in actions(board):
            max_val = random.randint(0, 3)
            if max_val < val2:
                val2 = max_val
                stupid_action = action

    if player(board) == playerX:
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > val3:
                val3 = min_val
                optimal_action = action

    else:
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < val4:
                val4 = max_val
                optimal_action = action

    if random_generator < 10:
        return stupid_action
    else:
        return optimal_action


# **********************
# Impossible bot
# **********************
def minimax(board):
    # Optimal action for the current player on the board.
    if terminal(board) is True:
        return None

    optimal_action = None
    val1 = -math.inf
    val2 = math.inf

    if player(board) == playerX:
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > val1:
                val1 = min_val
                optimal_action = action

    else:
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < val2:
                val2 = max_val
                optimal_action = action

    return optimal_action
