# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import sys
from pygame.locals import *
from agent import *
from board import *


FPS = 60
WINDOWWIDTH = 960
WINDOWHEIGHT = 640
BOXSIZE = 30

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#IA_PARAMS = [-0.510066, 0.760666, -0.35663, -0.184483]
IA_PARAMS = [-0.2548597909717818,0.8675694905501019,-0.8975174536762058,-0.31478386254215707]

#assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color


def main():
	if len(sys.argv) != 2:
		print("Need at least one argument : \n-r for a normal run of the tetris game\n-t to run train the IA")
	elif(sys.argv[1] == "-r"):
		global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
		random.seed(42)
		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
		BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
		BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
		pygame.display.set_caption('Tetromino')
		while True: # game loop
			runGame()
	elif(sys.argv[1] == "-t"):
		agent = TetrisAgent(Board())
		agent.train()

	elif(sys.argv[1] == "-c"):
		agent = TetrisAgent(Board())
		pop, gen = Individual.read()
		agent.train(pop, gen)


def runGame():
	# setup variables for the start of the game
	board = Board()
	agent = TetrisAgent(board)
	agent.setParams(IA_PARAMS)
	lastMoveDownTime = time.time()
	lastMoveSidewaysTime = time.time()
	lastFallTime = time.time()
	movingDown = False # note: there is no movingUp variable
	movingLeft = False
	movingRight = False
	score = 0
	level, fallFreq = calculateLevelAndFallFreq(score)
	fallingPiece = board.getNewPiece()
	nextPiece = board.getNewPiece()
	fallingPiece = agent.best(fallingPiece, nextPiece, False, board)[0]

	while True: # game loop
		if fallingPiece == None:
			# No falling piece in play, so start a new piece at the top
			fallingPiece = nextPiece
			nextPiece = board.getNewPiece()
			lastFallTime = time.time() # reset lastFallTime

			fallingPiece = agent.best(fallingPiece, nextPiece, False, board)[0]	

			if not board.isValidPosition(fallingPiece):
				print(score)
				break # can't fit a new piece on the board, so game over

		checkForQuit()
		# let the piece fall if it is time to fall
		if time.time() - lastFallTime > 0.01:
			# see if the piece has landed
			if not board.isValidPosition(fallingPiece, adjY=1):
				# falling piece has landed, set it on the board
				board.addToBoard(fallingPiece)
				completeLines = board.removeCompleteLines()
				if completeLines != 0:
					board.refreshColHeights(completeLines)
				score += completeLines
				level, fallFreq = calculateLevelAndFallFreq(score)
				fallingPiece = None
			else:
				# piece did not land, just move the piece down
				fallingPiece.move_down()
				lastFallTime = time.time()

		# drawing everything on the screen
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(board)
		drawStatus(score, level)
		drawNextPiece(nextPiece)
		if fallingPiece != None:
			drawPiece(fallingPiece)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()


def terminate():
	pygame.quit()
	sys.exit()


def checkForKeyPress():
	# Go through event queue looking for a KEYUP event.
	# Grab KEYDOWN events to remove them from the event queue.
	checkForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None

def checkForQuit():
	for event in pygame.event.get(QUIT): # get all the QUIT events
		terminate() # terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP): # get all the KEYUP events
		if event.key == K_ESCAPE:
			terminate() # terminate if the KEYUP event was for the Esc key
		pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
	# Based on the score, return the level the player is on and
	# how many seconds pass until a falling piece falls one space.
	level = int(score / 10) + 1
	fallFreq = 0.27 - (level * 0.02)
	return level, fallFreq

def convertToPixelCoords(boxx, boxy):
	# Convert the given xy coordinates of the board to xy
	# coordinates of the location on the screen.
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	# draw a single box (each tetromino piece has four boxes)
	# at xy coordinates on the board. Or, if pixelx & pixely
	# are specified, draw to the pixel coordinates stored in
	# pixelx & pixely (this is used for the "Next" piece).
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
	# draw the border around the board
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

	# fill the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
	# draw the individual boxes on the board
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			drawBox(x, y, board.get(x,y))


def drawStatus(score, level):
	# draw the score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 150, 20)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

	# draw the level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOWWIDTH - 150, 50)
	DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
	shapeToDraw = PIECES[piece.get_shape()][piece.get_rotation()]
	if pixelx == None and pixely == None:
		# if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
		pixelx, pixely = convertToPixelCoords(piece.get_x(), piece.get_y())

	# draw each of the boxes that make up the piece
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[y][x] != BLANK:
				drawBox(None, None, piece.get_color(), pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
	# draw the "next" text
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 200, 80)
	DISPLAYSURF.blit(nextSurf, nextRect)
	# draw the "next" piece
	drawPiece(piece, pixelx=WINDOWWIDTH-200, pixely=100)


if __name__ == '__main__':
	main()