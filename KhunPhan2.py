import numpy as np
import unittest as ut

# This program aims to solve Khun Phan, a riddle where different pieces move around a field.
# Two different representations of the field are used here (for now).
    # One is a 4-by-5 list of lists (5 lists with each having 4 entries) with bool values for whether the field is occupied.
    # The other is an enumeration of all fields from 1 to 20, starting with fields 1-4 in the first row.
    # The pieces are listed in four lists, one for each type, values from 1 to 20 in each list tell the position of the pieces' upper left corners
    # List gets updated on each move, and then sorted to be comparable to past positions
    # Formula to transform matrix index to enumerated position: posin20(i,j) = (i-1) * 4 + j
# TODO: It might be possible to represent everything just with the numbers from the second version, 
# so one long-term goal is to switch the whole computation to that.

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
        if self.t == 1 : 
            return [(self.i, self.j)]
        elif self.t == 2 :
            return [(self.i, self.j), (self.i + 1, self.j)]
        elif self.t == 3 :
            return [(self.i, self.j), (self.i, self.j + 1)]
        else :
            return [(self.i, self.j), (self.i, self.j + 1), 
                    (self.i + 1, self.j), (self.i + 1, self.j + 1)]
        
    # Return list of bool values whether it is possible for a piece to move upwards, to the right, down or to the left
    def getMoves(self, f) :
        if self.t == 1 : 
            return [f.getCell(self.i - 1, self.j), f.getCell(self.i, self.j + 1), f.getCell(self.i + 1, self.j), f.getCell(self.i, self.j - 1)]
        elif self.t == 2 :
            return [f.getCell(self.i - 1, self.j), f.getCell(self.i, self.j + 1) and f.getCell(self.i + 1, self.j + 1), 
                    f.getCell(self.i + 2, self.j), f.getCell(self.i, self.j - 1) and f.getCell(self.i + 1, self.j - 1)]
        elif self.t == 3 :
            return [f.getCell(self.i - 1, self.j) and f.getCell(self.i - 1, self.j + 1), f.getCell(self.i, self.j + 1), 
                    f.getCell(self.i + 1, self.j) and f.getCell(self.i + 1, self.j + 1), f.getCell(self.i, self.j - 1)]
        else :
            return [f.getCell(self.i - 1, self.j) and f.getCell(self.i - 1, self.j + 1), 
                    f.getCell(self.i, self.j + 2) and f.getCell(self.i + 1, self.j + 2),                     
                    f.getCell(self.i + 2, self.j) and f.getCell(self.i + 2, self.j + 1), 
                    f.getCell(self.i, self.j - 1) and f.getCell(self.i + 1, self.j - 1)]


    def getType(self) :
        return self.t

    # Move this piece on a given field in a direction: up(1), right(2), down(3), left(4)
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


# The Khun Phan playing field (maybe rename to 'board'?)
class Field :
    height = 5
    width = 4

    # Initialising the field with a matrix of bool values (True = empty, False = occupied) and a list of the pieces on the field.
    # In order to avoid having to deal with index-out-of-bounds problems, the field is surrounded
    # by a padding of 'False' values, implying that no piece can be put there.
    def __init__(self) :
        self.field = [[False, False, False, False, False, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, False, False, False, False, False]]

    def __repr__(self) -> str :
        return str(np.array(self.field))
    
    def setPieceList(self, list) :
        self.pieceList = list
    
    def getPieceList(self) :
        return self.pieceList

    def setCell(self, i, j, val) :
        self.field[i][j] = val

    def getCell(self, i, j) :
        return self.field[i][j]

    def updatePieceList(self, t, n, d) :
        # How to change the number in the piecelist according to move direction
        pieceListDict = { 1:-4, 2:1, 3:4, 4:-1 }

        self.pieceList[t-1].remove(n - pieceListDict[d])
        self.pieceList[t-1].append(n)
        self.pieceList[t-1].sort()


# ------------------------------------------------------------------------------------------
# Now that we have pieces and a field, this is the controller section working with both.

# Starting position for the original Khun Phan challenge. 
start = [[14,15,18,19], [1,4,13,16], [10], [2]]
# Keep track of all positions that have been reached so far.
positions = []

# Node class to create a search tree. 
# Each node consists of a position and a list of following position, its children.
class Node :
    def __init__(self, position, field, pieces) :
        self.position = position
        self.field = field
        self.pieces = pieces
        self.children = []

    def addChild(self, child) :
        self.children.append(child)

    def getPos(self) :
        return self.position

    def getChildren(self) :
        return self.children


def controller() :
    f,ps = setup(start)
    createTree(f,ps,start)
    
def createTree(f, ps, pos) :  
    print(f.getPieceList())
    positions.append(pos)
    if len(positions) > 1024 : 
        raise AssertionError("Reached more than 1024 different positions!")
    node = Node(pos, f, ps)
    for piece in ps :
        moves = piece.getMoves(f)
        for k, m in enumerate(moves) :
            if m : 
                newPos = move(f, piece, k+1)
                if newPos in positions :
                    print("Position already found.")
                elif newPos[3] == [14] : 
                    print("Solved!\n", newPos)
                else :
                    print("Creating new node.")
                    node.addChild(createTree(setup(newPos), newPos))

# Set up a field with pieces
def setup(pos) :
    field = Field()
    pieces = []
    for k in range(4):
        for x in pos[k] :
            piece = Piece(k+1, (x-1)//4 + 1, (x-1)%4 + 1)
            addPiece(field, piece)
            pieces.append(piece)
    field.setPieceList(pos)
    return (field, pieces)

def addPiece(f, p) :
    occupied = p.occupies()
    for i,j in occupied : 
        if not f.getCell(i,j) :
            raise AssertionError("Tried to add piece in occupied space")
    for i,j in occupied:
        f.setCell(i,j,False)

def move(f, p, dir) :
    p.move(dir)
    match dir, p.getType() :
        case 1,1 :
            f.setCell(p.getI()+1, p.getJ(), True)
            f.setCell(p.getI(), p.getJ(), False)
        case 1,2 :
            f.setCell(p.getI()+2, p.getJ(), True)
            f.setCell(p.getI(), p.getJ(), False)
        case 1,3 :
            f.setCell(p.getI()+1, p.getJ(), True)
            f.setCell(p.getI()+1, p.getJ()+1, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI(), p.getJ()+1, False)
        case 1,4 :
            f.setCell(p.getI()+2, p.getJ(), True)
            f.setCell(p.getI()+2, p.getJ()+1, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI(), p.getJ()+1, False)
        case 2,1 :
            f.setCell(p.getI(), p.getJ()-1, True)
            f.setCell(p.getI(), p.getJ(), False)
        case 2,2 :
            f.setCell(p.getI(), p.getJ()-1, True)
            f.setCell(p.getI()+1, p.getJ()-1, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI()+1, p.getJ(), False)
        case 2,3 :
            f.setCell(p.getI(), p.getJ()-1, True)
            f.setCell(p.getI(), p.getJ()+1, False)
        case 2,4 :
            f.setCell(p.getI(), p.getJ()-1, True)
            f.setCell(p.getI()+1, p.getJ()-1, True)
            f.setCell(p.getI(), p.getJ()+1, False)
            f.setCell(p.getI()+1, p.getJ()+1, False)
        case 3,1 :
            f.setCell(p.getI()-1, p.getJ(), True)
            f.setCell(p.getI(), p.getJ(), False)
        case 3,2 :
            f.setCell(p.getI()-1, p.getJ(), True)
            f.setCell(p.getI()+1, p.getJ(), False)
        case 3,3 :
            f.setCell(p.getI()-1, p.getJ(), True)
            f.setCell(p.getI()-1, p.getJ()+1, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI(), p.getJ()+1, False)
        case 3,4 :
            f.setCell(p.getI()-1, p.getJ(), True)
            f.setCell(p.getI()-1, p.getJ()+1, True)
            f.setCell(p.getI()+1, p.getJ(), False)
            f.setCell(p.getI()+1, p.getJ()+1, False)
        case 4,1 :
            f.setCell(p.getI(), p.getJ()+1, True)
            f.setCell(p.getI(), p.getJ(), False)
        case 4,2 :
            f.setCell(p.getI(), p.getJ()+1, True)
            f.setCell(p.getI()+1, p.getJ()+1, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI()+1, p.getJ(), False)
        case 4,3 :
            f.setCell(p.getI(), p.getJ()+2, True)
            f.setCell(p.getI(), p.getJ(), False)
        case 4,4 :
            f.setCell(p.getI(), p.getJ()+2, True)
            f.setCell(p.getI()+1, p.getJ()+2, True)
            f.setCell(p.getI(), p.getJ(), False)
            f.setCell(p.getI()+1, p.getJ(), False)

    print(p.getType(), (p.getI() - 1) * 4 + p.getJ())
    f.updatePieceList(p.getType(), (p.getI() - 1) * 4 + p.getJ(), dir)
    return f.pieceList


# ------------------------------------------------------------------------------------

controller()
# setup(start)

# field = Field()
# print(field)
# piece1 = Piece(1,4,2)
# piece2 = Piece(2,1,1)
# addPiece(field, piece1)
# addPiece(field, piece2)


# f1 = Field()
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
