import numpy as np
import unittest as ut

# This program aims to solve Khun Phan, a riddle where different pieces move around a board.
# Two different representations of the board are used here (for now).
    # One is a 4-by-5 list of lists (5 lists with each having 4 entries) with bool values for whether the board is occupied.
    # The other is an enumeration of all boards from 1 to 20, starting with fields 1-4 in the first row.
    # The pieces are listed in four lists, one for each type, values from 1 to 20 in each list tell the position of the pieces' upper left corners
    # List gets updated on each move, and then sorted to be comparable to past positions
    # Formula to transform matrix index to enumerated position: posin20(i,j) = (i-1) * 4 + j

# A piece on the Khun Phan board has a type and i/j-coordinates (row/column)
class Piece : 
    def __init__(self, t, i, j) :
        self.t = t # possible types: 1 (1 by 1), 2 (2 by 1), 3 (1 by 2), 4 (2 by 2)
        self.i = i
        self.j = j

    def getI(self) :
        return self.i
    
    def getJ(self) :
        return self.j
    
    # Return a list of (i,j)-tuples of the squares that are being occupied by this piece.
    def occupies(self) :
        match self.t :
            case 1 :
                return [(self.i, self.j)]
            case 2 :
                return [(self.i, self.j), (self.i + 1, self.j)]
            case 3 :
                return [(self.i, self.j), (self.i, self.j + 1)]
            case 4 :
                return [(self.i, self.j), (self.i, self.j + 1), 
                    (self.i + 1, self.j), (self.i + 1, self.j + 1)]
        
    # Return list of bool values whether it is possible for a piece to move upwards, to the right, down or to the left
    def getMoves(self, f) :
        match self.t :
            case 1 : 
                return [f.getCell(self.i - 1, self.j), f.getCell(self.i, self.j + 1), 
                        f.getCell(self.i + 1, self.j), f.getCell(self.i, self.j - 1)]
            case 2 :
                return [f.getCell(self.i - 1, self.j), f.getCell(self.i, self.j + 1) and f.getCell(self.i + 1, self.j + 1), 
                        f.getCell(self.i + 2, self.j), f.getCell(self.i, self.j - 1) and f.getCell(self.i + 1, self.j - 1)]
            case 3 :
                print([f.getCell(self.i - 1, self.j) and f.getCell(self.i - 1, self.j + 1), f.getCell(self.i, self.j + 1), 
                        f.getCell(self.i + 1, self.j) and f.getCell(self.i + 1, self.j + 1), f.getCell(self.i, self.j - 1)])
                return [f.getCell(self.i - 1, self.j) and f.getCell(self.i - 1, self.j + 1), f.getCell(self.i, self.j + 1), 
                        f.getCell(self.i + 1, self.j) and f.getCell(self.i + 1, self.j + 1), f.getCell(self.i, self.j - 1)]
            case 4 :
                return [f.getCell(self.i - 1, self.j) and f.getCell(self.i - 1, self.j + 1), 
                        f.getCell(self.i, self.j + 2) and f.getCell(self.i + 1, self.j + 2),                     
                        f.getCell(self.i + 2, self.j) and f.getCell(self.i + 2, self.j + 1), 
                        f.getCell(self.i, self.j - 1) and f.getCell(self.i + 1, self.j - 1)]


    def getType(self) :
        return self.t

    # Move this piece on a given board in a direction: up(1), right(2), down(3), left(4)
    # TODO: change if-cases to match/case statement (everywhere in this program actually)
    def move(self, dir) :
        if dir == 1 :
            self.i -= 1
        elif dir == 2 :
            self.j += 1
        elif dir == 3 :
            self.i += 1
        elif dir == 4 :
            self.j -= 1


# The Khun Phan playing board 
class Board :
    height = 5
    width = 4

    # Initialising the board with a matrix of bool values (True = empty, False = occupied) and a list of the pieces on the board.
    # In order to avoid having to deal with index-out-of-bounds problems, the board is surrounded
    # by a padding of 'False' values, implying that no piece can be put there.
    def __init__(self) :
        self.board = [[False, False, False, False, False, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, False, False, False, False, False]]

    def __repr__(self) -> str :
        return str(np.array(self.board))
    
    def setPieceList(self, list) :
        self.pieceList = list
    
    def getPieceList(self) :
        return self.pieceList

    def setCell(self, i, j, val) :
        self.board[i][j] = val

    def getCell(self, i, j) :
        return self.board[i][j]

    def updatePieceList(self, t, n, d) :
        # How to change the number in the piecelist according to move direction
        pieceListDict = { 1:-4, 2:1, 3:4, 4:-1 }

        self.pieceList[t-1].remove(n - pieceListDict[d])
        self.pieceList[t-1].append(n)
        self.pieceList[t-1].sort()


# Node class to create a search tree. 
# Each node consists of a position and a list of following positions, its children.
class KP :
    def __init__(self, position, board, pieces) :
        self.position = position
        self.board = board
        self.pieces = pieces
        self.children = []

    def addChild(self, child) :
        self.children.append(child)

    def getPos(self) :
        return self.position
    
    def getBoard(self) :
        return self.board
    
    def getPieces(self) :
        return self.pieces

    def getChildren(self) :
        return self.children


# ------------------------------------------------------------------------------------------
# Now that we have pieces, a playing board and search trees, this is the controller section.


# Starting position for the original Khun Phan challenge. 
start = [[14,15,18,19], [1,4,13,16], [10], [2]]
# Keep track of all positions that have been reached so far.
positions = [[]]

# Create first objects, start search tree.
def controller() :
    khunPhan = setup(start)
    createTree(khunPhan)
    
# Set up a board with pieces
def setup(pos) :
    board = Board()
    pieces = []
    board.setPieceList(pos)
    for k in range(4):
        for x in pos[k] :
            piece = Piece(k+1, (x-1)//4 + 1, (x-1)%4 + 1)
            addPiece(board, piece)
            pieces.append(piece)
    khunPhan = KP(pos, board, pieces)
    return (khunPhan)

def createTree(kp) :  
    positions.append(kp.getPos())
    if len(positions) > 900 : 
        print(positions)
        raise AssertionError("Reached more than 900 different positions!")
    for piece in kp.getPieces() :
        moves = piece.getMoves(kp.getBoard())
        for k, m in enumerate(moves) :
            if m : 
                newKP = newBoard(kp, piece, k+1)
                newPos = newKP.getPos()
                if newPos in positions :
                    print("Position already found.")
                elif newPos[3] == [14] : 
                    print("Solved!\n", newPos)
                    break
                else :
                    newBoard, newPieces = setup(newPos)
                    kp.addChild(createTree(newBoard, newPieces, newPos))

# Add a piece to a board if there is space for it
def addPiece(f, p) :
    occupied = p.occupies()
    for i,j in occupied : 
        if not f.getCell(i,j) :
            raise AssertionError("Tried to add piece in occupied space")
    for i,j in occupied:
        f.setCell(i,j,False)

# Given a game, a piece and a direction, create a new board where the piece has been moved
def newBoard(kp, p, dir) :
    newKP = KP(kp.getPos(), kp.getBoard(), kp.getPieces())
    for newPiece in newKP.getPieces :
        if comparePieces(newPiece, p) :
            newPiece.move(dir)
    match dir, newPiece.getType() :
        case 1,1 :
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 1,2 :
            newKP.getBoard().setCell(newPiece.getI()+2, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 1,3 :
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, False)
        case 1,4 :
            newKP.getBoard().setCell(newPiece.getI()+2, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI()+2, newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, False)
        case 2,1 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 2,2 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), False)
        case 2,3 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, False)
        case 2,4 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()-1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, False)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()+1, False)
        case 3,1 :
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 3,2 :
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), False)
        case 3,3 :
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, False)
        case 3,4 :
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ(), True)
            newKP.getBoard().setCell(newPiece.getI()-1, newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()+1, False)
        case 4,1 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 4,2 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()+1, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), False)
        case 4,3 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+2, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
        case 4,4 :
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ()+2, True)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ()+2, True)
            newKP.getBoard().setCell(newPiece.getI(), newPiece.getJ(), False)
            newKP.getBoard().setCell(newPiece.getI()+1, newPiece.getJ(), False)
    
    newKP.getBoard().updatePieceList(newPiece.getType(), (newPiece.getI() - 1) * 4 + newPiece.getJ(), dir)
    return newKP

def comparePieces(p1, p2) :
    return p1.getType() == p2.getType() and p1.getI() == p2.getI() and p1.getJ() == p2.getJ()

# ------------------------------------------------------------------------------------

controller()
# setup(start)

# board = Board()
# print(board)
# piece1 = Piece(1,4,2)
# piece2 = Piece(2,1,1)
# addPiece(board, piece1)
# addPiece(board, piece2)


# f1 = Board()
# p1 = Piece(1, 1, 1)
# p2 = Piece(1, 3, 4)
# f1.addPiece(p1)
# f1.addPiece(p2)
# print(p1.getMoves(f1))
# p2.move(f1, 1)
# print(f1)
# print(f1.pieceList)
# print("hello, world")


# class Test :
#     def __init__(self, val) :
#         self.val = val

#     def getVal(self) :
#         return self.val

# class Test2:
#     def __init__(self, oval) :
#         self.oval = oval

#     def getVal(self) :
#         return self.oval

# a = Test(1)
# b = Test(3)
# c = Test2(4)
# d = Test2(5)


# match a.getVal(), c.getVal() :
#     case 1,4 :
#         print("it worked")
