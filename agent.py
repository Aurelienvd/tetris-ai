import pygame, time, random
from pygame.locals import *
from board import *
from individual import *

KEYS = (K_RIGHT, K_LEFT, K_UP)

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

	def setParams(self, paramList):
		self.setAggregateParam(paramList[0])
		self.setCompLinesParam(paramList[1])
		self.setHolesParam(paramList[2])
		self.setBumpParam(paramList[3])

	def setAggregateParam(self,aggregateParam):
		self.aggregateParam = aggregateParam

	def setCompLinesParam(self, compLinesParam):
		self.compLinesParam = compLinesParam

	def setHolesParam(self, holesParam):
		self.holesParam = holesParam

	def setBumpParam(self, bumpParam):
		self.bumpParam = bumpParam


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
					score = self.aggregateParam*workingBoard.computeAggregate() + self.compLinesParam*workingBoard.completeLines() + self.holesParam*workingBoard.computeHoles() + self.bumpParam*workingBoard.computeBumpiness()
				else:
					score = self.best(piece, nextPiece, True, workingBoard)[1]

				if(bestScore == None or score == None or score > bestScore):
					bestScore = score
					best = workingPiece.clone()
				workingPiece.move_right()

		return [(best.clone() if best != None else piece), bestScore]



		########## Evolution Algorithm ##########

	def train(self):
		individual = self.generateRandomIndividual()

	def generateRandomIndividual(self):
		individual = Individual(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), 0)
		return individual

	def computeFitness(self, population, nbGames, maxNbPieces):
		for individual in population:
			self.board = Board()
			agent.setParams(individual.getParams())
			totalScore = 0
			for i in nbGames:
				fallingPiece = board.getNewPiece()
				nextPiece = board.getNewPiece()
				score = 0
				currNbPieces = 0
				while(currNbPieces <= maxNbPieces and not board.isValidPosition(fallingPiece)):
					fallingPiece = this.best(fallingPiece, nextPiece, False, self.board)[0]
					self.board.fallDown(fallingPiece)
					self.board.addToBoard(fallingPiece)
					score += self.board.removeCompleteLines()
					fallingPiece = nextPiece
					nextPiece = self.board.getNewPiece()
				totalScore += score
			individual.setFitness(totalScore)





		

		