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

	def best(self, piece, nextPiece):
		# dummy behavior just to check if it works properly.
		best = None
		bestScore = None
		workingPiece = piece.clone()
		
		
		for i in range(4):
			#may be fucked up here
			workingPiece.rotate((workingPiece.get_rotation() + 1) % len(PIECES[workingPiece.get_shape()]))
			
			workingBoard = self.board.clone()

			while (workingBoard.isValidPosition(piece, -1)):
				workingPiece.move_left(1)
			
			while (workingBoard.isValidPosition(piece, 0, 1)):

				
				workingBoard.fallDown(workingPiece)

				score = 0
				completedLines = workingBoard.removeCompleteLines()
				workingBoard.refreshColHeights(completedLines)

				score = a*workingBoard.computeAggregate() + b*completedLines + c*workingBoard.computeHoles() + d*workingBoard.computeBumpiness()

				if(score > bestScore or bestScore == None):
					bestScore = score
					best = workingPiece.clone()

				workingPiece.move_right(1)

		piece = best.clone()

		