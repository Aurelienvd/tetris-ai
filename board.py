import random
from piece import *

BOARDWIDTH = 10
BOARDHEIGHT = 20
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
BLANK = '.'

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)

S_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '..OO.',
					 '.OO..',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '...O.',
					 '.....']]

Z_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '..OO.',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '.O...',
					 '.....']]

I_SHAPE_TEMPLATE = [['..O..',
					 '..O..',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 'OOOO.',
					 '.....',
					 '.....']]

O_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '.OO..',
					 '.....']]

J_SHAPE_TEMPLATE = [['.....',
					 '.O...',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..OO.',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '...O.',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '.OO..',
					 '.....']]

L_SHAPE_TEMPLATE = [['.....',
					 '...O.',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '..OO.',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '.O...',
					 '.....'],
					['.....',
					 '.OO..',
					 '..O..',
					 '..O..',
					 '.....']]

T_SHAPE_TEMPLATE = [['.....',
					 '..O..',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '..O..',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '..O..',
					 '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
		  'Z': Z_SHAPE_TEMPLATE,
		  'J': J_SHAPE_TEMPLATE,
		  'L': L_SHAPE_TEMPLATE,
		  'I': I_SHAPE_TEMPLATE,
		  'O': O_SHAPE_TEMPLATE,
		  'T': T_SHAPE_TEMPLATE}

class Board():

	def __init__(self, oboard = None):
		self.board = [[BLANK]*BOARDHEIGHT for i in range(BOARDWIDTH)]
		if (oboard != None):
			for i in range(BOARDWIDTH):
				for j in range(BOARDHEIGHT):
					self.board[i][j] = oboard[i][j]

	def get(self,x,y):
		return self.board[x][y]

	def isOnBoard(self, x, y):
		return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

	def addToBoard(self, piece, colHeights):
		# fill in the board based on piece's location, shape, and rotation
		lastXPos = -1
		for x in range(TEMPLATEWIDTH):
			for y in range(TEMPLATEHEIGHT):
				if PIECES[piece.get_shape()][piece.get_rotation()][y][x] != BLANK:
					nextYPos = y + piece.get_y()
					nextXPos = x + piece.get_x()
					if lastXPos != nextXPos:
						colHeights[nextXPos] = BOARDHEIGHT - nextYPos
						lastXPos = nextXPos
					self.board[nextXPos][nextYPos] = piece.get_color()

	def getNewPiece(self):
		# return a random new piece in a random rotation and color
		shape = random.choice(list(PIECES.keys()))
		newPiece = Piece(shape, random.randint(0, len(PIECES[shape])-1), int(BOARDWIDTH/2)-int(TEMPLATEWIDTH/2), -2, random.randint(0, len(COLORS)-1))
		return newPiece

	def isValidPosition(self, piece, adjX=0, adjY=0):
		# Return True if the piece is within the board and not colliding
		for x in range(TEMPLATEWIDTH):
			for y in range(TEMPLATEHEIGHT):
				isAboveBoard = y + piece.get_y() + adjY < 0
				if isAboveBoard or PIECES[piece.get_shape()][piece.get_rotation()][y][x] == BLANK:
					continue
				if not self.isOnBoard(x + piece.get_x() + adjX, y + piece.get_y() + adjY):
					return False
				if self.board[x + piece.get_x() + adjX][y + piece.get_y() + adjY] != BLANK:
					return False
		return True

	def isCompleteLine(self, y):
		# Return True if the line filled with boxes with no gaps.
		for x in range(BOARDWIDTH):
			if self.board[x][y] == BLANK:
				return False
		return True

	def removeCompleteLines(self):
		# Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
		numLinesRemoved = 0
		y = BOARDHEIGHT - 1 # start y at the bottom of the board
		while y >= 0:
			if self.isCompleteLine(y):
				# Remove the line and pull boxes down by one line.
				for pullDownY in range(y, 0, -1):
					for x in range(BOARDWIDTH):
						self.board[x][pullDownY] = self.board[x][pullDownY-1]
				# Set very top line to blank.
				for x in range(BOARDWIDTH):
					self.board[x][0] = BLANK
				numLinesRemoved += 1
				# Note on the next iteration of the loop, y is the same.
				# This is so that if the line that was pulled down is also
				# complete, it will be removed.
			else:
				y -= 1 # move on to check next row up
		return numLinesRemoved

	def computeHoles(self):
		L = 0
		for x in range(BOARDWIDTH):
			for y in range(BOARDHEIGHT):
				if self.board[x][y] == BLANK:
					for yAbove in self.board[x][:y]:
						if yAbove != BLANK:
							L += 1
							break
		return L

	def computeBumpiness(self, colHeights):
		b = 0
		for i in range(len(colHeights)-1):
			b += abs(colHeights[i+1] - colHeights[i])
		return b

	def refreshColHeights(self, completeLines, colHeights):
		for i in range(len(colHeights)):
			res = colHeights[i] - completeLines
			if res <= 0:
				colHeights[i] = 0 
			else:
				colHeights[i] = res

	def fallDown(self, piece):
		while(self.isValidPosition(piece, 0, -1)):
			piece.move_down()

	def clone(self):
		return Board(self)