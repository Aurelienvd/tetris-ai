import pygame
from pygame.locals import *

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
		if (self.board.isValidPosition(piece, -2)):
			piece.move_left(2)
		pass