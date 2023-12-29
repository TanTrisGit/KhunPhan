import numpy as np

# This program aims to solve Khun Phan, a riddle where different pieces move around a field.
# Two different representations of the field are used here (for now).
# One is a 4-by-5 list of lists (5 lists with each having 4 entries) with bool values for whether the field is occupied.
# The other is an enumeration of all fields from 1 to 20, starting with fields 1-4 in the first row.
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
    # TODO: swap f.field with f.getCell (good practice to use getter methods)
    def getMoves(self, f) :
        if self.t == 1 : 
            return [f.field[self.i - 1][self.j], f.field[self.i][self.j + 1], f.field[self.i + 1][self.j], f.field[self.i][self.j - 1]]
        elif self.t == 2 :
            return [f.field[self.i - 1][self.j], f.field[self.i][self.j + 1] and f.field[self.i + 1][self.j + 1], 
                    f.field[self.i + 2][self.j], f.field[self.i][self.j - 1] and f.field[self.i + 1][self.j - 1]]
        elif self.t == 3 :
            return [f.field[self.i - 1][self.j] and f.field[self.i - 1][self.j + 1], f.field[self.i][self.j + 1], 
                    f.field[self.i + 1][self.j] and f.field[self.i + 1][self.j + 1], f.field[self.i][self.j - 1]]
        else :
            return [f.field[self.i - 1][self.j] and f.field[self.i - 1][self.j + 1], 
                    f.field[self.i][self.j + 2] and f.field[self.i + 1][self.j + 2],                     
                    f.field[self.i + 2][self.j] and f.field[self.i + 2][self.j + 1], 
                    f.field[self.i][self.j - 1] and f.field[self.i + 1][self.j - 1]]

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

    def getType(self) :
        return self.t

class Field :
    height = 5
    width = 4

    def __init__(self) :
        self.field = [[False, False, False, False, False, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, True, True, True, True, False],
                      [False, False, False, False, False, False]]
        self.pieceList = [[], [], [], []]

    def __repr__(self) -> str:
        return str(np.array(self.field))
    
    def setCell(self, i, j, val) :
        self.field[i][j] = val

    def getCell(self, i, j) :
        return self.field[i][j]

    def updatePieceList(self, t, n) :

        # How to change the number in the piecelist according to move direction and piece type
        pieceListDict = { 1:-4, 2:1, 3:4, 4:-1 }

        self.pieceList[t-1].remove(n)
        self.pieceList[t-1].append(n+pieceListDict(t))
        self.pieceList[t-1].sort()

    def getPieceList(self) :
        return self.pieceList

    def setPieceList(self, list) :
        self.pieceList = list

    # Represent the field with values from 1 to (width * height) (20 in this case)
    # Have a list of four lists, one for each type, with the values where the upper left corners of such pieces are
    # Needs to be updated on each move, and then sorted to be comparable to past positions
    # Formula: posin20(i,j) = (i-1) * 4 + j


# --------------------------------------------------------------

# Starting position for the original Khun Phan challenge. 
# In the first list, the positions of pieces of the first type are saved and so on.    
start = [[14,15,18,19], [1,4,13,16], [10], [2]]
positions = []

# Node class to create a search tree. 
# Each node consists of a position and a list of following position, its children.
class Node :
    def __init__(self, position) :
        self.position = position
        self.children = []

def controller() :
    f,p = setup(start)
    positions.append(start)

    #TODO: Create search tree
    for piece in p :
        moves = piece.getMoves(f)
        for k, move in enumerate(moves) :
            if move : 
                move(f, piece, k+1)

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
            #TODO: Find correct exception name
            raise ValueError("Tried to add piece in occupied space")
        for i,j in occupied:
            f.setCell(i,j,False)

def move(f,  p, dir) :
    if dir == 1 :
        if p.getType() == 1 :
            p.move(dir)
            f.setCell(p.getI(), p.getJ(), True)
            f.setCell(p.getI()-1, p.getJ(), False)
        # elif
    elif dir == 2 :
        pass
    elif dir == 3 :
        pass
    else :
        pass
    f.updatePieceList(p.getType(), (p.getI() - 1) * 4 + p.getJ())
    return f.pieceList

# f1 = Field()
# p1 = Piece(1, 1, 1)
# p2 = Piece(1, 3, 4)
# f1.addPiece(p1)
# f1.addPiece(p2)
# print(p1.getMoves(f1))
# p2.move(f1, 1)
# print(f1)
# print(f1.pieceList)
