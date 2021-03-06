import pygame, time, random
from operator import attrgetter
from pygame.locals import *
from board import *
from individual import *
from multiprocessing import Queue, Process
from collections import Counter

KEYS = (K_RIGHT, K_LEFT, K_UP)

ROT = { 'S': 2,
		'Z': 2,
		'J': 4,
		'L': 4,
		'I': 2,
		'O': 1,
		'T': 4}

N_PROC = 4

W_LB = -1
W_UB = 1
N_GAMES = 5
N_GEN = 1
N_MOVES = 200
POPULATION_SIZE = 100
TOURNAMENT_SIZE = POPULATION_SIZE//10
OFFSPRING_SIZE = int(POPULATION_SIZE*0.28)
MUTATION_RATE = 0.1
NBPARAMS = 4


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

	def train(self, population = [], gen_ = 0):

		self.population = population
		if self.population == []:
			for i in range(POPULATION_SIZE):
				self.population.append(self.generateRandomIndividual())
			self.distributedFitness(self.population, POPULATION_SIZE)
			print("Fitness Done")
		else:
			N_MOVES = 200 + (gen_ - 11) * 10
		gen = gen_ + 1
		for i in range(N_GEN):
			N_MOVES += 10
			print(N_MOVES)
			start = time.time()
			offsprings = [None]*OFFSPRING_SIZE
			for j in range(OFFSPRING_SIZE):
				parents = self.tournamentSelect(TOURNAMENT_SIZE)
				offspring = self.onePointCrossOver(parents[0], parents[1])
				self.mutate(offspring)
				offsprings[j] = offspring
			self.distributedFitness(offsprings, OFFSPRING_SIZE)
			self.nextGeneration(offsprings)
			print("Gen {0} Done".format(gen))
			print(time.time()-start)
			gen = gen + 1

		Individual.write(self.population, gen)

	def generateRandomIndividual(self):
		individual = Individual(random.uniform(W_LB, W_UB), random.uniform(W_LB, W_UB), random.uniform(W_LB, W_UB), random.uniform(W_LB, W_UB), 0)
		return individual

	def distributedFitness(self, population, population_size):
		assert population_size%N_PROC == 0 	# Precond: population_size divisible by N_PROC
		q = Queue()
		chunk_size = population_size//N_PROC

		jobs = []
		for i in range(N_PROC):
			p = Process(target=self.computeFitness, args=(population[i*chunk_size:(i+1)*chunk_size], q))
			jobs.append(p)
			p.start()

		for i in range(N_PROC):
			population[i*chunk_size:(i+1)*chunk_size] = q.get(True)

		for j in jobs:
			j.join()


	def computeFitness(self, population, q = None):
		for individual in population:
			self.setParams(individual.getParams())
			totalScore = 0
			for i in range(N_GAMES):
				self.board = Board()
				fallingPiece = self.board.getNewPiece()
				nextPiece = self.board.getNewPiece()
				score = 0
				currNbPieces = 0
				while(currNbPieces <= N_MOVES and self.board.isValidPosition(fallingPiece)):
					fallingPiece = self.best(fallingPiece, nextPiece, False, self.board)[0]
					self.board.fallDown(fallingPiece)
					self.board.addToBoard(fallingPiece)
					currNbPieces += 1
					score += self.board.removeCompleteLines()
					fallingPiece = nextPiece
					nextPiece = self.board.getNewPiece()
				totalScore += score
			individual.setFitness(totalScore//N_GAMES)
		if (q != None):
			q.put(population)

	def randomSubset(self, iterator, K):
		result = []
		N = 0

		for item in iterator:
			N += 1
			if len( result ) < K:
				result.append( item )
			else:
				s = int(random.random() * N)
				if s < K:
					result[ s ] = item

		return result

	def tournamentSelect(self, K):
		KRandomIndividuals = self.randomSubset(self.population, K)
		fittest1 = max(KRandomIndividuals, key=attrgetter('fitness'))
		KRandomIndividuals.remove(fittest1)
		fittest2 = max(KRandomIndividuals, key=attrgetter('fitness'))
		return (fittest1, fittest2)

	def onePointCrossOver(self, indiv1, indiv2):
		index = random.randint(1, NBPARAMS-1)
		params = indiv1.getParams()[:index] + indiv2.getParams()[index:]
		return Individual(params[0], params[1], params[2], params[3])

	def mutate(self, offspring):
		p = random.uniform(0,1)
		if(p <= MUTATION_RATE):
			paramMutating = random.choice(["aggregateParam", "compLinesParam", "holesParam", "bumpParam"])
			paramValue = getattr(offspring, paramMutating)
			setattr(offspring, paramMutating, paramValue * random.gauss(1, 0.2))

	def nextGeneration(self, offsprings):
		self.population.sort(key=attrgetter('fitness'))
		self.population[:OFFSPRING_SIZE] = offsprings[:]






		

		