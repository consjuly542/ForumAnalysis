from processedDataLoader import loadDataGenerator

class StatisticsModule(Module):
	def get_laws_statistics(self):
		data_generator = loadDataGenerator()
		for data in data_generator: