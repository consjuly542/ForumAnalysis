#!/usr/bin/python
# -*- coding: utf-8 -*-

from processedDataLoader import loadDataGenerator
import load_file_article
from ArticleStatistics import ArticleStatistics
from links_searcher import *
import pickle
import operator
# from link_to_article import link_to_article
from functools import cmp_to_key
import sys
from link_to_article import Link2Article

def write_current_article_list(articles_list, cnt_visible_article = 30):
	with open("./../data/statistics/current_article_list", "wb") as f:
		pickle.dump(articles_list[:cnt_visible_article], f, protocol=pickle.HIGHEST_PROTOCOL)

# class StatisticsModule(Module):
class StatisticsModule(object):
	def __run__(self, file_origin, file_target):
		pass

	def __init__(self, recompute_statistic = False):
		self.get_article_statistics(recompute_statistic = recompute_statistic)
		#list which users see
		self.cur_articles_list = list(self.article_index.values())
		#ranking list of articles wuthout filters - for fast execution
		self.articles_list_all = list(self.article_index.values())

		self.is_ranked = False
		self.is_filtered = False
		self.rank_type = None
		#filters list
		self.filters_type = []
		self.filters_data = []

		#default - ranked by cnt_questions, no filters
		self.ranking_articles(rank_type = 'by_cnt_questions')

	def get_article_index(self):
		"""
		Create dictionary {article:article_statistics}
		"""
		articles = load_file_article.load_data()
		print ("Count official articles: %d" % len(articles))
		self.article_index = {a.article_ID:ArticleStatistics(a) for a in articles}

		with open("./../data/statistics/article_index", "wb") as f:
			pickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
		
	def get_article_statistics(self, recompute_statistic=True):
		if recompute_statistic:
			self.get_article_index()
			data_generator = loadDataGenerator()
			cnt_not_match_links = 0
			links_cnt = 0
			l2a = Link2Article()
			# log = open("./logs", "w")
			# error_link = []
			for question_batch in data_generator:
				for question in question_batch:

					links = LinksSearcher(question.get_all_text()).get_simple_links()
					for link in links:
						# function from Alexandrina
						article = l2a.link2article(link)
						# print (article)
						if article:
							# print (article.article_ID)
							links_cnt += 1
							self.article_index[article.article_ID].add_question(question, link)
						else:
							cnt_not_match_links += 1
							# log.write(link.link_text + '\n')
							# log.flush()
							# error_link.append(link)
							# print( link.to_dict())
							# if cnt_not_match_links > 20:
							# 	print ("I AM HERE")
							# 	with open("./error_link", "wb") as f:
							# 		pickle.dump(error_link, f, protocol=pickle.HIGHEST_PROTOCOL)
							# 	return 

					sys.stderr.write("\r\t\tALL LINKS: %d; CAN't MATCH: %d" % (links_cnt, cnt_not_match_links))

			with open("./../data/statistics/article_statistics", "wb") as f:
				pickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
		else:
			with open("./../data/statistics/article_statistics", "rb") as f:
				self.article_index = pickle.load(f)

	def ranking_articles(self, rank_type = 'by_cnt_questions'):
		if rank_type == 'by_cnt_questions':
			self.cur_articles_list = sorted(self.cur_articles_list, \
									key = operator.attrgetter('questions_cnt'), reverse = True)
			self.articles_list_all = sorted(self.article_index.values(), \
									key = operator.attrgetter('questions_cnt'), reverse = True)
		elif rank_type == 'by_sum_cnt_answers':
			self.cur_articles_list = sorted(self.cur_articles_list, key=operator.attrgetter('sum_answers_cnt'), reverse=True)
			self.articles_list_all = sorted(self.article_index.values(), key=operator.attrgetter('sum_answers_cnt'), reverse=True)
		elif rank_type == 'by_date':
			self.cur_articles_list = sorted(self.cur_articles_list, key=operator.attrgetter('last_date'), inverse=True)
			self.articles_list_all = sorted(self.article_index.values(), key=operator.attrgetter('last_date'), inverse=True)

		self.is_ranked = True
		self.rank_type = rank_type

		write_current_article_list(self.cur_articles_list)
		# with open("./../data/statistics/current_article_list", "wb") as f:
		# 	pickle.dump(self.cur_articles_list, f, protocol=pickle.HIGHEST_PROTOCOL)


	# def add_filter(self, filter_type, filter_data):
	# 	"""
	# 	add filter by data or law
	# 	filter_type = 'law' or 'date'
	# 	фильтр по дате - оставляю только те статьи, 
	# 	упоминание о котором есть позднее указанного числа
	# 	if filter by date: filter_data is string: "year.month.day"
	# 	if filter by law: filter_data - law name (ex. "Гражданский кодекс") - 
	# 	-здесь скорее всего должен быть выпадающий список
	# 	"""
	# 	if filter_type in self.filters:
	# 		pass
	# 	else:
	# 		self.cur_articles_list = [article for art]

	# def cancel_filter(self, filter_type):
	# 	self.filters_data.pop(self.filters_type.index(filter_type))
	# 	self.filters_type.remove(filter_type)

	# 	self.cur_articles_list = self.articles_list_all.copy()
	# 	for i, f in enumerate(self.filters_type):
	# 		self.add_filter(filter_type = f)



index = StatisticsModule(recompute_statistic=True)
# print(len(index.article_index))
# # for idx, k in enumerate(index.article_index.keys()):
# # 	if idx > 2:
# # 		break
# # 	print (k.to_dict())

# with open("./../data/statistics/current_article_list", "rb") as f:
# 	articles = pickle.load(f)

# 	for idx, k in enumerate(articles):
# 		if idx > 1:
# 			break
# 		print (k.to_dict()['questions_cnt'])