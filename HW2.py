#! /usr/bin/python3

Boards = {}
cliques = [
[0, 1, 2],\
[3, 4, 5],\
[6, 7, 8],\
[0, 3, 6],\
[1, 4, 7],\
[2, 5, 8],\
[0, 4, 8],\
[2, 4, 6]\
]

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None
        self.children = []

def CreateAllBoards(layout):
    if layout not in Boards.keys():
        Boardx = BoardNode(layout)
        win = False
        idx = 0
        while not win and idx < 8:
            if layout[cliques[idx][0]] != '_':
                if layout[cliques[idx][0]] == layout[cliques[idx][1]] and layout[cliques[idx][1]] == layout[cliques[idx][2]]:
                    win = True
                    break
            idx += 1
        if not win:
            if '_' not in layout:
                Boardx.endState = 'Draw'
            else:
                turn = layout.count('_')
                if turn % 2 == 0:
                    turn = 'O'
                else:
                    turn = 'X'
                empty = []
                for i in range(9):
                    if layout[i] == '_':
                        empty.append(i)
                children = []
                for e in empty:
                    child = layout[:e] + turn + layout[e+1:]
                    children.append(CreateAllBoards(child))
                Boardx.children = children
        else:
            Boardx.endState = layout[cliques[idx][0]]
        Boards[layout] = Boardx
    return layout

def main():
    CreateAllBoards("_________")
    Xwins = 0
    Owins = 0
    Draws = 0
    Not_End = 0
    Children = 0
    for x in Boards:
        status = Boards[x].endState
        if status == None:
            Not_End += 1
        if status == 'X':
            Xwins += 1
        if status == 'O':
            Owins += 1
        if status == 'Draw':
            Draws += 1
        n = len(Boards[x].children)
        Children += n
    print(" Number of Boards: " + str(len(Boards)) + "\n Xwins: " + str(Xwins) + "\n Owins: " + str(Owins) + "\n Draws: " + str(Draws) + "\n Not End of Game: " + str(Not_End) + "\n Children: " + str(Children))
    return 0

main()
