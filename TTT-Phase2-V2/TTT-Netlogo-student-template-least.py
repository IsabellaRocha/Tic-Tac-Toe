# TicTacToe - perfect competitor code outline

# Below, any  variable called "board" contains a board layout string of 9 chars or 'x', 'o' and '_'
# AllBoards is a dictionary of all boards
# key = board, value = the Tboard instance

import sys

AllBoards = {}

wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

class Tboard:

    def __init__(self,board,lastmove):
        '''lastmove is the move that led to this board'''
        self.board = board
        self.lastmove = lastmove  # the move (0-8) that led to this board, None if this is the root board

        self.player,self.opponent = WhoseMove(board)

        # state is 'x' if this board is or will be a win for 'x' if the best moves are taken
        # state is 'o' if win for 'o'
        # state is None if we haven't figured this out yet
        self.state = None

        # moves_to_state is how many moves from here to the state if best moves are taken
        # moves_to_state == 0 if this board is actually a final board in the game
        # moves_to_state == None if we haven't figure this out yet
        self.moves_to_state = None

        # best_move is the best next move (0-8) to lead to a win, or if not,
        #   at least a draw, or, sadly, a necessary loss
        #  or -1 if this is a final board
        self.best_move = None
        self.minmax = 0
        self.children = [] # list of child Tboards


def FigureItOut(board):
    '''returns a list: best_move, moves_to_state, and state
    best_move (0-8) is, you know, the best move, unless moves_to_state == 0
    if moves_to_state == 0 then we're at the end of the game
    and state is the expected final state: 'x', 'o', or 'd', for X-winning, O-winning, or Draw'''
    AllBoards.clear()

    root = Tboard(board,None)
    AllBoards[board] = root

    # Step 1:
    # Create the board tree starting from this root.
    FindAllBoards(root)

    # Step 2:
    # now traverse the game tree (depth first), filling in best_move, moves_to_state and state
    #o wants to take the path with the minimum values, which is at the beginning of the children array, whereas x wants to maximize its score
    root.minmax, root.moves_to_state = CalcBestMove(root)
    if root.player == "x":
        root.best_move = root.children[len(root.children) - 1].lastmove
        if root.minmax > 0:
            root.state = root.player
        if root.minmax < 0:
            root.state = root.opponent
        if root.minmax == 0:
            root.state = "d"
    if root.player == "o":
        root.best_move = root.children[0].lastmove
        if root.minmax > 0:
            root.state = root.opponent
        if root.minmax < 0:
            root.state = root.player
        if root.minmax == 0:
            root.state = "d"
    return [root.best_move, root.moves_to_state, root.state]

def FindAllBoards(board_node):
    ''' Constructs the subtree of boards leading from board_node and puts all such boards (layouts)
    into the dictionary AllBoards.  Uses AllBoards to prevent dublicate boards.  This should
    create a tree of maximum 5478 boards if we start from the empty board.  But usually we won't
    start from the empty board'''

    if board_node in AllBoards:
        return

    AllBoards[board_node.board] = board_node

    # is this a final board?
    endboard = IsEndBoard(board_node.board)  # returns 'x' or 'o' or 'd' if final, else None
    if endboard is not None:   # this board is a win for 'x' or 'o' or a draw
        board_node.state = endboard
        board_node.moves_to_state = 0
        board_node.best_move = -1
        return

    # Now recurse through all the children:
    this_board = board_node.board
    player = board_node.player
    for i in range(9):
        if this_board[i] == '_':
            child_board = this_board[:i]+player+this_board[i+1:]
            child_node = Tboard(child_board,i)
            board_node.children.append(child_node)
            FindAllBoards(child_node)
    return

def CalcBestMove(board_node):
    '''  updates this board_node with correct values for state, moves_to_state, and best_move
    (This is the engine.)'''
    if board_node.state == None:
        for child in board_node.children:
            child.minmax, child.moves_to_state = CalcBestMove(child)
        board_node.children = sorted(board_node.children, key = lambda x: x.minmax)
        if board_node.player == "x":
            newMinmax = board_node.children[len(board_node.children) - 1].minmax
            newMoves = board_node.children[len(board_node.children) - 1].moves_to_state + 1
            return newMinmax, newMoves
        if board_node.player == "o":
            newMinmax = board_node.children[0].minmax
            newMoves = board_node.children[0].moves_to_state + 1
            return newMinmax, newMoves
    elif board_node.state == "x":
        return 1, 0
    elif board_node.state == "o":
        return -1, 0
    else:
        return 0, 0



def WhoseMove(board):
    '''returns the player (either 'x' or 'o') and also opponent'''
    if board.count('x') == board.count('o'):
        return ['x','o']
    return ['o', 'x']

def IsEndBoard(board):
    for awin in wins:
        if board[awin[0]] != '_' and board[awin[0]] == board[awin[1]] and board[awin[1]] == board[awin[2]]:
            return board[awin[0]]
    if board.count('_') == 0:
        return 'd'
    return None

def PrintBoardNode(node):
    '''for debugging'''
    print('layout',node.board)
    print('last_move',node.lastmove)
    print('player',node.player)
    print('state',node.state)
    print('moves_to_state',node.moves_to_state)
    print('best_move',node.best_move)
    for child_node in node.children:
        print('child',child_node.lastmove,child_node.board)

def main():
    output = sys.argv[1]
    board = sys.argv[2]
    Positions = ('Top-left','Top-center','Top-right','Middle-left','Middle-center',\
                 'Middle-right','Bottom-left','Bottom-center','Bottom-right')
    bestmove, movestostate, stateofboard = FigureItOut(board)
    s = '%d\n' % bestmove
    s += 'Position: %s\n' % Positions[int(bestmove)]
    if stateofboard == None:
        s += "Don't know how many moves to anything...\n"
    else:
        if stateofboard == "x" or stateofboard == "o":
            s += "%s wins in %d moves" % (stateofboard, movestostate)
        else:
            s += "Draw in %d moves" % movestostate
    print(s)
    print(output)
    f = open(output,'w')
    f.write(s)
    f.close()

main()
