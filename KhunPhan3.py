import copy
import numpy as np

# This program attempts to solve the Khun Phan riddle.

# There are 10 pieces on a Khun Phan board, 4 1-by-1, 4 1-by-2, 1 2-by-1 and one 2-by-2 piece.
# These piece types are enumerated 0 to 3.

# The board is represented by a 4-by-5 matrix of bool values with a padding of 1.
# An square is empty if the value in the matrix is 'True', and occupied if the value is 'False'.
# The padding avoids index-out-of-bounds problems by simulating squares that are "always occupied" as a border.
# Also, because of the padding, the indices for row and column start at 1.

# The progression of the game is represented by games states. Each state is one position of pieces.
# The state also saves the list of positions that led to the current one (how did we get here? = howDid)
# Piece positions are saved using a different representation of the board, an enumeration from 1 to 20.
# The upper left corner of the board is the 1, the first row are the numbers 1 to 4, and so on.
# Each position is a list of four lists, one for each piece type.

# In order to find a way to solve the riddle, positions are saved in nodes of a search tree.
# Beginning with the starting position as root node, all possible following positions are its child nodes.
# A list of positions that have already been reached is saved globally.
# If a potential child of a node is a position that has already been reached, the child node is not created.


# Formula to transform the enumerated position into matrix coordinates
def getIJ(n) :
    return ((n-1)//4 + 1, (n-1)%4 + 1)

# Formula to transform matrix coordinates into the enumerated position
def getN(i,j) :
    return ((i-1)*4 + j)

emptyBoard = [[False, False, False, False, False, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, False, False, False, False, False]]

startPosition = [[14,15,18,19], [1,4,13,16], [10], [2]]

def setupBoard(position) :
    board = copy.deepcopy(emptyBoard)
    for type, list in enumerate(position) :
        for n in list : 
            for i,j in occupies(type, n) :
                board[i][j] = False
    return board

# List of squares occupied by a piece of a certain type
def occupies(type, n) :
    i,j = getIJ(n)
    match type :
        case 0 : return [(i,j)]
        case 1 : return [(i,j), (i+1,j)]
        case 2 : return [(i,j), (i,j+1)]
        case 3 : return [(i,j), (i, j+1), (i+1, j), (i+1, j+1)]


# List of 4 bool values (up, right, down, left) indicating empty squares around a given piece
def lookAround(state, type, n) :
    i,j = getIJ(n)
    b = state.getBoard()
    match type :
        case 0 :
            return [b[i-1][j], b[i][j+1], b[i+1][j], b[i][j-1]]
        case 1 : 
            return [b[i-1][j], b[i][j+1] and b[i+1][j+1], b[i+1][j], b[i][j-1] and b[i+1][j-1]]
        case 2 :
            return [b[i-1][j] and b[i-1][j+1], b[i][j+2], b[i+1][j] and b[i+1][j+1], b[i][j-1]]
        case 3 :
            return [b[i-1][j] and b[i-1][j+1], b[i][j+2] and b[i+1][j+2],
                    b[i+2][j] and b[i+2][j+1], b[i][j-1] and b[i+1][j-1]]

# Given a piece's position, its type and the direction it shall move in, calculate the emerging position
def newPos(state, n, type, dir) :
    # What is the relative distance to an enumerated position in a certain direction?
    directionDict = {0:-4, 1:1, 2:4, 3:-1}
    newPos = copy.deepcopy(state.getPosition())
    newPos[type].remove(n)
    newPos[type].append(n + directionDict[dir])
    newPos[type] = sorted(newPos[type])
    return newPos


class State :

    def __init__(self, position, howDid) :
        self.position = position
        self.howDid = howDid
        self.board = setupBoard(position)

    def __repr__(self) :
        return str(np.array(self.position))
    
    def getPosition(self) :
        return self.position
    
    def getHowDid(self) :
        return self.howDid
    
    def getBoard(self) :
        return self.board
    
    def addToHowDid(self, position) :
        self.howDid.append(position)

    # List of all positions reachable in one move
    def successorPositions(self) :
        successors = []
        for type, x in enumerate(self.position) :
            for n in x :
                for dir, b in enumerate(lookAround(self, type, n)) :
                    if b : successors.append(newPos(self, n, type, dir))
        return successors


# Now we have everything we need for the search tree. 
# Its root node is State(startPosition).
# The children of a node are the successors of its state.
# Every time a node is created, its position is added to the list of explored positions.
# Also, it must be tested for whether it is a solution to the riddle.
# If so, the list of positions that led to this state is returned as a solution to the riddle and the algorithm stops.
# If that is not the case, its children are created as new nodes if their position has not yet been reached.

# Positions that have been visited
reached = []

def run() :
    node(State(startPosition, []))

def node(state) :
    curPos = state.getPosition()
    if curPos[3] != [2] :
        print(curPos)
    # Save in all positions reached
    reached.append(curPos)
    # Save in all positions that led to this state
    state.addToHowDid(curPos)
    # Check winning condition
    if curPos[3] == [14] : 
        print("Found a solution!")
        print(state.getHowDid())
        return
    for s in state.successorPositions() :
        if s not in reached :
            node(State(s, state.getHowDid()))

run()
            
# n = State([[14, 15, 18, 19], [1, 4, 13, 16], [11], [2]], [])
# print(n.successorPositions())