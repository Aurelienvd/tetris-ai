import pygame
from pygame.locals import *
from board import *

KEYS = (K_RIGHT, K_LEFT, K_UP)

a = -0.510066
b = 0.760666
c = -0.35663
d = -0.184483

class TetrisAgent():

	def __init__(self, board):
		self.board = board
		self.score = 0

	def best(self, piece, nextPiece, checkForNextPiece=False):
		
		best = None
		bestScore = None
		
		for i in range(4):
			workingPiece = (piece.clone() if not checkForNextPiece else nextPiece.clone())
			workingPiece.rotate((workingPiece.get_rotation() + i) % len(PIECES[workingPiece.get_shape()]))

			while (self.board.isValidPosition(workingPiece, -1)):
				workingPiece.move_left()
			
			while (self.board.isValidPosition(workingPiece)):
				workingBoard = self.board.clone()
				workingPiece.set_y(0)
				workingBoard.fallDown(workingPiece)
				workingBoard.addToBoard(workingPiece)

				self.score = 0
				completedLines = workingBoard.removeCompleteLines()
				workingBoard.refreshColHeights(completedLines)

				if(checkForNextPiece):
					self.score = a*workingBoard.computeAggregate() + b*completedLines + c*workingBoard.computeHoles() + d*workingBoard.computeBumpiness()
				else:
					self.score = self.best(piece, nextPiece, True)

				if(bestScore == None or self.score > bestScore):
					self.bestScore = self.score
					best = workingPiece.clone()

				workingPiece.move_right()
		if(best != None):
			best.set_y(0)
		self.score = (bestScore if best != None else 0)

		return (best.clone() if best != None else piece)
		

		