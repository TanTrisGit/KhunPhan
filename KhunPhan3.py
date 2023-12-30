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
            return [b[i-1][j], b[i][j+1] and b[i+1][j+1], b[i+2][j], b[i][j-1] and b[i+1][j-1]]
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
        return copy.deepcopy(self.howDid)
    
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
    # Save solutions in text document
    solutions = open("Solutions.txt", "w")
    solutions.write("These are my solutions for Khun Phan.\n")
    solutions.close()
    node(State(startPosition, []))
    
# Calculate the distance between two pieces
def dist(n1,n2) :
    i1,j1 = getIJ(n1)
    i2,j2 = getIJ(n2)
    return (abs(i1-i2) + abs(j1-j2))

def shouldVisit(pos, howDid) :
    s0 = pos[0][0]
    s1 = pos[0][1]
    s2 = pos[0][2]
    s3 = pos[0][3]

    v0 = pos[1][0]
    v1 = pos[1][1]
    v2 = pos[1][2]
    v3 = pos[1][3]

    h = pos[2][0]

    b = pos[3][0]

    # If the four single squares are in one row, no real movement is possible
    # That is the case if their (sorted) values have a difference of 3 from last to first
    if s3 - s0 == 3 :
        return False
    
    # Also, at least two of the four single squares should always be next to each other
    # elif dist(s0,s1) > 1 and dist(s0,s2) > 1 and dist(s0,s3) > 1 and dist (s1,s2) > 1 and dist(s1,s3) > 1 and dist(s2,s3) > 1 :
    #     return False
      
    # Make sure the big piece actually moves further away from its original position over time
    elif len(howDid) > 400 :
        return False
    else :
        return True

def printToFile(l) :
    solutions = open("Solutions.txt", "a")
    solutions.write("[")
    for part in l :
        solutions.write(str(part))
        solutions.write(",")
        solutions.write("\n")
    solutions.write("]\n")
    solutions.close()


def node(state) :
    curPos = state.getPosition()
    #TESTING. TODO: Remove
    #Testing whether the big square has moved two steps down the board
    # if curPos[3][0] > 12 :
    #     print(curPos)
    # Save in all positions reached
    reached.append(curPos)
    # Add to positions that led to this state
    state.addToHowDid(curPos)
    # Check winning condition
    if curPos[3][0] == 14 : 
        print("Found a solution!")
        printToFile(state.getHowDid())
        return
    for s in state.successorPositions() :
        if s not in reached and shouldVisit(s, state.getHowDid()):
            node(State(s, state.getHowDid()))

run()

 

# All of this seems to be working fine.
# However, the maximum recursion depth is exceeded. 
# Maybe this can be fixed with a better solution for setting up the board than deepcopying the empty board.
# However, I will try to make the system intelligent by not visiting nodes that are probably bad.
# That is what the shouldVisit() method is for.

