"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn = None
    turns_made = 0

    for row in board:
        for col in row:
            if col == "O" or col == "X":
                turns_made += 1
    
    if turns_made % 2 == 0:
        turn = X
    else:
        turn = O

    return turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in board:
        for col in row:
            if col == EMPTY:
                possible_actions.add((row,col))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)

    board_cp = [row[:] for row in board]
    row, col = action

    if board_cp[row][col] == EMPTY:
        board_cp[row][col] = turn
    else:
        raise Exception('NotValidTurn')

    return board_cp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None

    # Check each row for same sign
    for row in board:
        if row[0] != EMPTY and row[0] == row[1] == row[2]:
            winner = row[0]
    
    # Check each col for same sign
    for col in range(3):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] == board[2][col]:
            winner = board[0][col]

    # Check each diagonal for same sign
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        winner = board[1][1]

    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        winner = board[1][1]
    
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    is_over = False

    if winner(board):
        is_over = True

    if len(actions(board)) == 0:
        is_over = True

    return is_over


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    result = 0

    if win == X:
        result = 1
    
    if win == O:
        result = -1
    
    return result


def maxvalue(v,board):
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = maxvalue()

    return v

def minvalue(board):
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = minvalue()

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Given a state S:
        # Max picks action a in Actions(s) that produces
        # highest value of Min-Value(Result(s,a))

        # Min picks action a in Actions(s) that produces
        # smallest value of Max-Value(Result(s,a))

    optimal_action = None

    # Check current player
    turn = player(board)

    if turn == X:
        maxvalue(board)

    if turn == O:
        minvalue(board)

    return optimal_action
