import copy
import numpy as np
from PIL import Image, ImageDraw

# This program attempts to solve the Khun Phan riddle.

# There are 10 pieces on a Khun Phan board, 4 1-by-1, 4 1-by-2, 1 2-by-1 and one 2-by-2 piece.
# These piece types are enumerated 0 to 3.

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

# List of solutions
solutions = []

# Positions that have been visited
reached = []

def run() :
    node(State(startPosition, []))
    
# The following methods are trying to make the search more efficient.
# However, they are pretty bad.
# New idea: Calculate the "minimum move distance" between two positions.
# If a position could have been reached quicker, cut current branch of the search tree.
    
# How many moves is the quickest way from one position to the other?
    
# Check whether there are unnecessary steps leading to the current position


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
    
    # Any path that is longer than the shortest solution is cut
    elif len(solutions) > 0 and len(howDid) > len(min(solutions, key=len)) :
        return False
    else :
        return True

def node(state) :
    curPos = state.getPosition()
    reached.append(curPos)
    # Add to positions that led to this state
    state.addToHowDid(curPos)
    # Check winning condition
    if curPos[3][0] == 14 : 
        print("Found a solution!")
        solutions.append(state.getHowDid())
        return
    for s in state.successorPositions() :
        if s not in reached and shouldVisit(s, state.getHowDid()):
            node(State(s, state.getHowDid()))

run()

# --------------------------------------------------------------------------------------
# Visualisation of solutions:

size = 10
padding = 2
margin = 30
boardlength = size*5 + margin
boardwidth = size*4 + margin
boardsPerRow = 30
piececolor = (191,153,114)
boardcolor = (164,116,73)
imagecolor = (144,96,53)

for index, solution in enumerate(solutions) :

    im = Image.new('RGB', (boardsPerRow * boardwidth + 20, ((len(solution) + 3*boardsPerRow)//(boardsPerRow-1))*boardwidth), (50,50,50))
    draw = ImageDraw.Draw(im)

for index, solution in enumerate(solutions) :

    im = Image.new('RGB', (boardsPerRow * boardwidth + 20, ((len(solution) + 3*boardsPerRow)//(boardsPerRow-1))*boardwidth), (50,50,50))
    draw = ImageDraw.Draw(im)

    for i, step in enumerate(solution) :
        fieldULX = (i%boardsPerRow)*boardwidth + size/2
        fieldULY = (i//boardsPerRow)*boardlength + size/2
        draw.rectangle((fieldULX, fieldULY, fieldULX + 5*size, fieldULY + 6*size), fill=boardcolor)
        for type, pos in enumerate(step) :
            for n in pos :
                y,x = getIJ(n)
                upLeftX = (i%boardsPerRow) * boardwidth + x*size
                upLeftY = (i//boardsPerRow)* boardlength + y*size
                match type :
                    case 0 :
                        lowRightX = upLeftX + size
                        lowRightY = upLeftY + size
                        color = (255,255,255)
                    case 1 :
                        lowRightX = upLeftX + size
                        lowRightY = upLeftY + 2*size
                        color = (255,0,0)
                    case 2 :
                        lowRightX = upLeftX + 2*size
                        lowRightY = upLeftY + size
                        color = (255,0,0)
                    case 3 :
                        lowRightX = upLeftX + 2*size
                        lowRightY = upLeftY + 2*size   
                        color = (0,255,150)

                draw.rectangle((upLeftX, upLeftY, lowRightX, lowRightY), fill=color, outline=(0, 0, 0))
                # draw.ellipse((upLeftX + padding, upLeftY + padding, lowRightX - padding, lowRightY - padding), fill=color, outline=(0, 0, 0))

    path = "images/solution" + str(index) + ".jpg"
    im.save(path, quality=95)

# So far, so good. The program does indeed find a solution and the visualisation allows me to 
# test it. It actually works!.
# The next step. however, must be to make the search more efficient.
# One idea is to implement a breadth-first-search and end the search as soon as a solution has been found.
# That would ensure the shortest possible solution is found. 
# However, it might be computationally too involved.
# TODO: Implement and test BFS.