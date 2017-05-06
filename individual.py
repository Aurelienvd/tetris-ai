class Individual():
	def __init__(self, aggregateParam, compLinesParam, holesParam, bumpParam, fitness):
		self.setParams(aggregateParam, compLinesParam, holesParam, bumpParam, fitness)

	def __repr__(self):
		return self.getFitness().__repr__()

	def setParams(self, aggregateParam, compLinesParam, holesParam, bumpParam, fitness):
		self.setAggregateParam(aggregateParam)
		self.setCompLinesParam(compLinesParam)
		self.setHolesParam(holesParam)
		self.setBumpParam(bumpParam)
		self.setFitness(fitness)

	def getParams(self):
		return [self.aggregateParam, self.compLinesParam, self.holesParam, self.bumpParam]

	def setAggregateParam(self,aggregateParam):
		self.aggregateParam = aggregateParam

	def getAggregateParam(self):
		return self.aggregateParam

	def setCompLinesParam(self, compLinesParam):
		self.compLinesParam = compLinesParam

	def getCompLinesParam(self):
		return self.compLinesParam

	def setHolesParam(self, holesParam):
		self.holesParam = holesParam

	def getHolesParam(self):
		return self.holesParam

	def setBumpParam(self, bumpParam):
		self.bumpParam = bumpParam

	def getBumpParam(self):
		return self.bumpParam

	def setFitness(self, fitness):
		self.fitness = fitness

	def getFitness(self):
		return self.fitness