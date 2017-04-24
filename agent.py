import pygame
from pygame.locals import *
from board import *
import time

KEYS = (K_RIGHT, K_LEFT, K_UP)

a = -0.510066
b = 0.760666
c = -0.35663
d = -0.184483

class TetrisAgent():

	def __init__(self, board):
		self.board = board

	def best(self, piece, nextPiece, checkForNextPiece=False, board=None):
		
		best = None
		bestScore = None
		board = (self.board if board == None else board)
		
		for i in range(4):
			workingPiece = (piece.clone() if not checkForNextPiece else nextPiece.clone())
			workingPiece.rotate((workingPiece.get_rotation() + i) % len(PIECES[workingPiece.get_shape()]))

			while (board.isValidPosition(workingPiece, -1)):
				workingPiece.move_left()
			
			while (board.isValidPosition(workingPiece)):
				workingBoard = board.clone()
				workingPiece.set_y(0)
				workingBoard.fallDown(workingPiece)
				workingBoard.addToBoard(workingPiece)

				score = 0

				if(checkForNextPiece):
					score = a*workingBoard.computeAggregate() + b*workingBoard.completeLines() + c*workingBoard.computeHoles() + d*workingBoard.computeBumpiness()
				else:
					score = self.best(piece, nextPiece, True, workingBoard)[1]
					#self.score += a*workingBoard.computeAggregate() + b*workingBoard.completeLines() + c*workingBoard.computeHoles() + d*workingBoard.computeBumpiness()
				if(bestScore == None or score > bestScore):
					bestScore = score
					best = workingPiece.clone()
				workingPiece.move_right()
				
		if(best != None):
			best.set_y(0)
		score = (bestScore if best != None else 0)

		return [(best.clone() if best != None else piece),score]
		

		