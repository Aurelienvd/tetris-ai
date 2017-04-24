import pygame
from pygame.locals import *
from board import *
import time

KEYS = (K_RIGHT, K_LEFT, K_UP)

a = -0.510066
b = 0.760666
c = -0.35663
d = -0.184483

ROT = { 'S': 2,
		'Z': 2,
		'J': 4,
		'L': 4,
		'I': 2,
		'O': 1,
		'T': 4}

class TetrisAgent():

	def __init__(self, board):
		self.board = board

	def best(self, piece, nextPiece, checkForNextPiece=False, board=None):
		
		best = None
		bestScore = None

		nbRot = ROT.get(piece.shape) if not checkForNextPiece else ROT.get(nextPiece.shape)

		for i in range(nbRot):
			workingPiece = (piece.clone() if not checkForNextPiece else nextPiece.clone())
			workingPiece.rotate((workingPiece.get_rotation() + i) % len(PIECES[workingPiece.get_shape()]))

			while (board.isValidPosition(workingPiece, -1)):
				workingPiece.move_left()
			
			while (board.isValidPosition(workingPiece)):
				workingBoard = board.clone()
				pieceSet = workingPiece.clone()
				workingBoard.fallDown(pieceSet)
				workingBoard.addToBoard(pieceSet)

				score = 0

				if(checkForNextPiece):
					score = a*workingBoard.computeAggregate() + b*workingBoard.completeLines() + c*workingBoard.computeHoles() + d*workingBoard.computeBumpiness()
				else:
					score = self.best(piece, nextPiece, True, workingBoard)[1]

				if(bestScore == None or score == None or score > bestScore):
					bestScore = score
					best = workingPiece.clone()
				workingPiece.move_right()

		return [(best.clone() if best != None else piece), bestScore]

		

		