#!/usr/bin/python
# -*- coding: utf-8 -*-

from Article import Article
from Question import Question
#year, month, day
from datetime import date
import _pickle as cPickle
import pickle
from copy import deepcopy as copy
import re
import operator

def convert_date(dt):
    if not isinstance(dt, str):
        dt = str(dt)
    parts = re.split(r'\.|\_|\-', dt)
    if len(parts) == 1:
        parts = str(dt).split('.')
    if len(parts[0]) == 4:
        return '.'.join(reversed(parts))
    return str(dt)

class ArticleStatistics (object):
	"""
	Class for Law Statistics
	"""
	def __init__(self, official_article):
		#official laquww name - instance of class 
		self.official_article = official_article
		#points from link with frequency: 
		#dictionary: {point_num:frequency}
		self.parts_statistics = {}
		self.questions_cnt = 0
		self.sum_answers_cnt = 0
		self.cur_mean_answers = 0
		#filename for quetions
		self.questions_filename = "../data/statistics/article_questions/" + \
						self.official_article.article_ID
		with open(self.questions_filename, "wb") as f:
			pass
		self.dates = []
		self.first_date = None
		self.last_date = None
		#название кодекса
		self.code = self.official_article.law.lower() \
			if self.official_article.law.lower().find(u'кодекс') != -1 else None

	def add_question(self, question, link):
		if link.part_num:
			if link.part_num not in self.parts_statistics:
				self.parts_statistics[link.part_num] = 0
			self.parts_statistics[link.part_num] += 1

		self.questions_cnt += 1
		self.sum_answers_cnt += len(question.answers)

		self.cur_mean_answers = float(self.sum_answers_cnt) / self.questions_cnt

		with open(self.questions_filename, "ab") as f:
			tmp = copy(question)
			tmp.date = convert_date(question.date)
			cPickle.dump(tmp.to_dict(), f, protocol=pickle.HIGHEST_PROTOCOL)

		date_parts = question.date.strip().split("_")
		if len(date_parts) == 1:
			date_parts = question.date.strip().split(".")
			
		# print (date_parts)

		q_date = date(int(date_parts[0]), \
					 int(date_parts[1]), \
					 int(date_parts[2]))
		self.dates.append(q_date)

		if (self.first_date and self.first_date > q_date) or (self.first_date is None):
			self.first_date = q_date
		if (self.last_date and self.last_date < q_date) or (self.last_date is None):
			self.last_date = q_date


	def to_dict(self):
		return self.__dict__


def get_questions(questions_filename):
	"""
	Get list of questions dict from file
	"""
	questions_list = []
	with open(questions_filename, "rb") as f:
		while True:
			try:
				questions_list.append(pickle.load(f))
			except:
				break
	questions_list = sorted(questions_list, key=operator.itemgetter('date'), reverse=True)
	return questions_list





