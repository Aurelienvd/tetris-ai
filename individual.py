class Individual():
	def __init__(self, aggregateParam, compLinesParam, holesParam, bumpParam, fitness = 0):
		self.setParams(aggregateParam, compLinesParam, holesParam, bumpParam, fitness)

	def __repr__(self):
		return self.getParams().__repr__()

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

	def __str__(self):
		string = ",".join(self.getParams()) + "\n"
		return string

	@staticmethod
	def write(individuals, filename = "individuals.sv"):
		with open(filename, "w") as f:
			for individuals in individuals:
				f.write(str(i))


	@staticmethod
	def read(filename = "individuals.sv"):
		individuals = []
		with open(filename, "r") as f:
			individuals = f.readlines()
		individuals = [(i.strip()).split(",") for i in individuals]
		for i in range(len(individuals)):
			params = individuals[i]
			individuals[i] = Individual(params[0], params[1], params[2], params[3])
		return individuals


