from processedDataLoader import loadDataGenerator
import load_file_article
from ArticleStatistics import ArticleStatistics
from links_searcher import *
import pickle

# class StatisticsModule(Module):
class StatisticsModule(object):

	def get_article_index(self):
		"""
		Create dictionary {article:article_statistics}
		"""
		articles = load_file_article.load_data()
		self.article_index = {a:ArticleStatistics(a) for a in articles}

		with open("./../data/statistics/article_index", "wb") as f:
			pickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
		
	def get_article_statistics(self, recompute_statistic = True):
		if recompute_statistic:
			__get_article_index()
			data_generator = loadDataGenerator()
			for question_batch in data_generator:
				for question in question_batch:

					links = LinksSearcher(question.get_all_text()).get_simple_links()
					for link in links:
						#function from Alexandrina
						article = link2article(link)
						self.article_index[article].add_question(question)

			with open("./../data/statistics/article_statistics", "wb") as f:
				pickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
		else:

			with open("./../data/statistics/article_statistics", "rb") as f:
				self.article_index = pickle.load_data(f)

index = StatisticsModule()
index.get_article_index()
print(len(index.article_index))
for idx, k in enumerate(index.article_index.keys()):
	if idx > 2:
		break
	print (k.to_dict())

index.get_article_statistics()