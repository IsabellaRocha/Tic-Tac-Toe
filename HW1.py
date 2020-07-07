#! /usr/bin/python3

import copy
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

Rot90 = [6,3,0,7,4,1,8,5,2]
Rot180 = [8,7,6,5,4,3,2,1,0]
Rot270 = [2,5,8,1,4,7,0,3,6]
VertFlip= [2,1,0,5,4,3,8,7,6]
Transformations = [[Rot90],[Rot180],[Rot270],[VertFlip],[Rot90,VertFlip],[Rot180,VertFlip],[Rot270,VertFlip]]

def win(board):
    for clique in cliques:
        if board[clique[1]] != '_':
            if board[clique[0]] == board[clique[1]] and board[clique[1]] == board[clique[2]]:
                return True
    return False


def calculate():
    boards = set()
    boards.add("_________") #Cannot add lists to sets
    total = 0
    XWins = 0
    OWins = 0
    Draws = 0
    open = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for X1 in open:
        board9 = ['_', '_', '_', '_', '_', '_', '_', '_', '_']
        open9 = copy.copy(open)
        board9[X1] = 'X'
        open9.remove(X1)
        set9 = ''.join(board9) #Must make string to add to set
        boards.add(set9)
        for O1 in open9:
            board8 = copy.copy(board9)
            open8 = copy.copy(open9)
            board8[O1] = 'O'
            open8.remove(O1)
            set8 = ''.join(board8)
            boards.add(set8)
            for X2 in open8:
                board7 = copy.copy(board8)
                open7 = copy.copy(open8)
                board7[X2] = 'X'
                open7.remove(X2)
                set7 = ''.join(board7)
                boards.add(set7)
                for O2 in open7:
                    board6 = copy.copy(board7)
                    open6 = copy.copy(open7)
                    board6[O2] = 'O'
                    open6.remove(O2)
                    set6 = ''.join(board6)
                    boards.add(set6)
                    for X3 in open6:
                        board5 = copy.copy(board6)
                        open5 = copy.copy(open6)
                        board5[X3] = 'X'
                        open5.remove(X3)
                        set5 = ''.join(board5)
                        boards.add(set5)
                        if win(board5):
                            total += 1
                            XWins += 1
                        else:
                            for O3 in open5:
                                board4 = copy.copy(board5)
                                open4 = copy.copy(open5)
                                board4[O3] = 'O'
                                open4.remove(O3)
                                set4 = ''.join(board4)
                                boards.add(set4)
                                if win(board4):
                                    total += 1
                                    OWins += 1
                                else:
                                    for X4 in open4:
                                        board3 = copy.copy(board4)
                                        open3 = copy.copy(open4)
                                        board3[X4] = 'X'
                                        open3.remove(X4)
                                        set3 = ''.join(board3)
                                        boards.add(set3)
                                        if win(board3):
                                            total += 1
                                            XWins += 1
                                        else:
                                            for O4 in open3:
                                                board2 = copy.copy(board3)
                                                open2 = copy.copy(open3)
                                                board2[O4] = 'O'
                                                open2.remove(O4)
                                                set2 = ''.join(board2)
                                                boards.add(set2)
                                                if win(board2):
                                                    total += 1
                                                    OWins += 1
                                                else:
                                                    board2[open2[0]] = 'X'
                                                    set1 = ''.join(board2)
                                                    boards.add(set1)
                                                    if win(board2):
                                                        XWins += 1
                                                    else:
                                                        Draws += 1
                                                    total += 1
    return total, XWins, OWins, Draws, len(boards), boards

def transform(boards):
    irreducible = set()
    arr = list(boards)
    for idx in range(len(boards)):
        board = arr[idx]
        transforms = [""] * 7
        for i in range(9):
            transforms[0] += board[Rot90[i]]
            transforms[1] += board[Rot180[i]]
            transforms[2] += board[Rot270[i]]
            transforms[3] += board[VertFlip[i]]
        for x in range(9):
            transforms[4] += transforms[0][VertFlip[x]]
            transforms[5] += transforms[1][VertFlip[x]]
            transforms[6] += transforms[2][VertFlip[x]]
        if transforms[0] not in irreducible and transforms[1] not in irreducible and transforms[2] not in irreducible and transforms[3] not in irreducible and transforms[4] not in irreducible and transforms[5] not in irreducible and transforms[6] not in irreducible:
            irreducible.add(board)
    return len(irreducible)

def main():
    Total, XWins, OWins, Draws, Configurations, boards = calculate()
    print("Games: "+ str(Total) + "\nXWins: " + str(XWins) + "\nOWins: " + str(OWins) + "\nDraws: " + str(Draws) + "\nConfigurations: " + str(Configurations))
    print("Irreducible: " + str(transform(boards)))

main()
