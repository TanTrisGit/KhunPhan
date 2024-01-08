import copy
import numpy as np
from KhunPhan3Visual import drawSolution

# This program attempts to solve the Khun Phan riddle.

# There are 10 pieces on a Khun Phan board, 4 1-by-1, 4 1-by-2, 1 2-by-1 and one 2-by-2 piece.
# These piece types are enumerated 0 to 3.
# These values from 0 to 3 are not to be confused with directions.
# The direction a piece can move in is also represented by these values (0: up, 1: right, 2: down, 3: left)

# The board is represented by a 4-by-5 matrix of bool values with a margin of 1.
# A square is empty if the value in the matrix is 'True', and occupied if the value is 'False'.
# The margin avoids index-out-of-bounds problems by simulating squares that are "always occupied" as a border.
# Also, because of the margin, the indices for row and column start at 1.

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

# The empty board: All squares except the border are empty (=True)
emptyBoard = [[False, False, False, False, False, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, True, True, True, True, False],
              [False, False, False, False, False, False]]

# Starting and winning positions
startPositionA = [[14,15,18,19], [1,4,13,16], [10], [2]]
winningPositionA = [[13,16,17,20],[1,2,3,4],[10],[14]]

startPositionB = [[4,8,11,12],[1,2,3],[13,17],[15]]
winningPositionB = [[1,5,9,10],[2,3,4],[15,19],[13]]

startPositionC = [[1,4,5,8],[13,14,15,16],[10],[2]]
winningPositionC = [[4,8,13,17],[1,14,15,16],[10],[2]]

startPositionD = []
winningPositionD = []

startPositionE = []
winningPositionE = []

startPositionF = []
winningPositionF = []

startPositionG = []
winningPositionG = []

startPositionH = []
winningPositionH = []

startPositionI = []
winningPositionI = []


# Given a position (always in the enumerated representation), return a board
# where all occupied squares are set to False
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
    # Dictionary with the relative distance to an enumerated position in a certain direction (0 to 3)?
    directionDict = {0:-4, 1:1, 2:4, 3:-1}
    newPos = copy.deepcopy(state.getPosition())
    newPos[type].remove(n)
    newPos[type].append(n + directionDict[dir])
    newPos[type] = sorted(newPos[type])
    return newPos

# An instance of this class "State" is a state of the game.
# A game state has three class variables: 
# The position the game is in, the list of positions that led to this position (howDid) and the current board (bool values)
# Apart from getters and setters, it provides a method to get all possible next positions from itself,
# as well as a method that checks whether the current state is a winning position.
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
# Its root node is State(startPositionA, []), the state with the starting position and an empty howDid list.
# The children of a node are the next possible positions.
# Every time a node is created, it is checked for whether it already appears in the list of explored positions ("reached"). 
# If not, its position is added to the list of explored positions.
# Also, the method to test for whether it is a solution to the riddle ("solved") is called.
# If so, the list of positions that led to this state is added to the list of solutions ("solutions").
# If that is not the case, its children are checked by the shouldVisit method.
# If their path (length of howDid list) is not longer than the shortest solution and shorter than 201,
# they will be added at the end of the queue of nodes to visit (breadth first search).

# Set of solutions
solutions = []

# Positions that have been visited
reached = []

# List of nodes that will be visited next
queue = []

# Which version are we playing?
curVariant = 0

# To which depth should we search?
expMaxDepth = 200

# Get positions of the currently played variant (variant 0 to 8, which False (start) or True (win))
def curVariantPos(variant, which) :
    match variant :
        case 0 :
            if which : return winningPositionA
            else : return startPositionA
        case 1 :
            if which : return winningPositionB
            else : return startPositionB        
        case 2 :
            if which : return winningPositionC
            else : return startPositionC
        case 3 :
            if which : return winningPositionD
            else : return startPositionD
        case 4 :
            if which : return winningPositionE
            else : return startPositionE
        case 5 :
            if which : return winningPositionF
            else : return startPositionF
        case 6 :
            if which : return winningPositionG
            else : return startPositionG
        case 7 :
            if which : return winningPositionH
            else : return startPositionH
        case 8 :
            if which : return winningPositionI
            else : return startPositionI

# Mirror a position along the y axis
def mirrorPos(pos) :
    newPos = []
    for type, list in enumerate(pos) :
        newPieces = []
        for e in list :
            match type :
                case 0 | 1 : newPieces.append(((e-1)//4+1)*8 - 3 - e)
                case 2 | 3 : newPieces.append(((e-1)//4+1)*8 - 3 - e - 1)
        newPos.append(sorted(newPieces))
    return newPos

# Mirror all positions in a state (current and howDid)
def mirrorState(state) :
    oldHowDid = copy.deepcopy(state.getHowDid())
    newHowDid = []
    newPos = mirrorPos(copy.deepcopy(state.getPosition()))
    for pos in oldHowDid :
        newHowDid.append(mirrorPos(pos))
    return State(newPos, newHowDid)

# Check whether a new position should be visited
def shouldVisit(pos, howDid) :
    l = len(howDid)
    if l > expMaxDepth or solutions != [] and l > len(min(solutions, key=len)) :
        return False
    else :
        return True

# Have we solved the riddle?
def solved(position) :
    winPos = curVariantPos(curVariant, True)
    if position == winPos : 
        print("\nFound a solution!")
        return True
    else :
        return False

# Create a node in the search tree
def node(state) :
    # Visualize progress
    global expMaxDepth
    if len(queue) > 1 and ((len(state.getHowDid()))%7) == 0 and ((len(state.getHowDid())) < (len(queue[1].getHowDid()))) :
        print(str(int(round(((len(state.getHowDid()))/expMaxDepth)*100, 0))) + "% ", end='', flush=True)
    # Remove state from the queue
    queue.remove(state)
    curPos = state.getPosition()
    # Check whether the position (or a position symmetric to this one) has been reached already
    # If so, return and hence do not investigate this path any further
    if curPos in reached : #or mirrorPos(curPos) in reached:
        return
    # Add current position to reached positions
    reached.append(curPos)
    # Add to positions that led to this state
    state.addToHowDid(curPos)
    # Check winning condition
    if solved(curPos) :
        solutions.append(state.getHowDid())
        # If a solution was found, draw it and save in folder 'images'
        drawSolution(state.getHowDid(), len(solutions))
    # Create child nodes
    for s in state.successorPositions() :
        if shouldVisit(s, state.getHowDid()):
            queue.append(State(s, state.getHowDid()))


# Add starting position to the queue and handle the queue
# Print how many solutions you found to standard out
def run(variant, maxDepth) :
    print("Calculating... ", end='')
    global curVariant
    curVariant = variant
    global expMaxDepth
    expMaxDepth = maxDepth
    startPos = curVariantPos(variant, False)
    queue.append(State(startPos, []))
    while len(queue) > 0 :
        node(queue[0])

run(0, 114)


# ----------------------------------------------------------------------------------------------

# The future:

# Idea: Change calculation: Get rid of Boolean matrix and only look around empty squares
# Make list 1-20, then go through all pieces and remove occupied numbers to get list of two empty squares
# For each empty square, look one and two steps above/left/... for pieces that can move there
# Then, for two empty squares at once, look for these possibilities as well

# KIRILL was here
# New idea: Use integer (or short) as representation of a position (with hashsets)
# Next new idea: Start from BOTH ENDS and try and find matching positions in the middle
# Also, multithreading might actually be possible in Python