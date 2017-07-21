#!/usr/bin/python
# -*- coding: utf-8 -*-

from processedDataLoader import loadDataGenerator
import load_file_article
from ArticleStatistics import ArticleStatistics, get_questions
from links_searcher import *
import _pickle as cPickle
import pickle
import operator
from copy import deepcopy as copy
# from link_to_article import link_to_article
from functools import cmp_to_key
import sys
from link_to_article import Link2Article
from datetime import date


def data2dict(s_data):
    data = copy(s_data)
    for i, d in enumerate(data):
        for j, dt in enumerate(data[i].dates):
            data[i].dates[j] = convert_date(dt)
        data[i].last_date = convert_date(data[i].last_date)
        data[i].first_date = convert_date(data[i].first_date)
        data[i].official_article.date = convert_date(data[i].official_article.date)
        data[i].official_article.edit_date = convert_date(data[i].official_article.edit_date)
        # for j, dt in enumerate(data[i].questions):
        #     data[i].questions[j].date = convert_date(dt.date)
        #     data[i].questions[j] = dt.__dict__
        data[i].official_article = d.official_article.__dict__
        data[i] = d.__dict__
    return data


def convert_date(dt):
    if not isinstance(dt, str):
        dt = str(dt)
    parts = re.split(r'\.|\_|\-', dt)
    if len(parts) == 1:
        parts = str(dt).split('.')
    if len(parts[0]) == 4:
        return '.'.join(reversed(parts))
    return str(dt)


def write_current_article_list(articles_list, cnt_visible_article=30):
    with open("./../data/statistics/current_article_list", "wb") as f:
        article_dict = data2dict(copy(articles_list)[:cnt_visible_article])
        cPickle.dump(article_dict, f, protocol=pickle.HIGHEST_PROTOCOL)


# class StatisticsModule(Module):
class StatisticsModule(object):
    def __run__(self, file_origin, file_target):
        pass

    def __init__(self, recompute_statistics=False):
        self.get_article_statistics(recompute_statistics=recompute_statistics)
        # list which users see
        self.cur_articles_list = list(self.article_index.values())
        self.cur_articles_list = [a for a in self.cur_articles_list if a.questions_cnt > 0]
        # ranking list of articles without filters - for fast execution
        self.articles_list_all = list(self.article_index.values())
        self.articles_list_all = [a for a in self.articles_list_all if a.questions_cnt > 0]

        self.is_ranked = False
        self.is_filtered = False
        self.rank_type = None
        # filters list
        self.filters_type = []
        self.filters_data = []

        # default - ranked by cnt_questions, no filters
        self.ranking_articles(rank_type='by_cnt_questions')

    def get_article_index(self):
        """
        Create dictionary {article:article_statistics}
        """
        articles = load_file_article.load_data()
        print ("Count official articles: %d" % len(articles))
        self.article_index = {a.article_ID: ArticleStatistics(a) for a in articles}

        with open("./../data/statistics/article_index", "wb") as f:
            cPickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)

    def get_article_statistics(self, recompute_statistics=True):
        if recompute_statistics:
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

                    sys.stderr.write("\r\t\t\t\tALL LINKS: %d; CAN't MATCH: %d" % (links_cnt, cnt_not_match_links))

            with open("./../data/statistics/article_statistics", "wb") as f:
                cPickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open("./../data/statistics/article_statistics", "rb") as f:
                self.article_index = cPickle.load(f)

    def ranking_articles(self, rank_type='by_cnt_questions', ascending = False):
        if rank_type == 'by_cnt_questions':
            self.cur_articles_list = sorted(self.cur_articles_list, \
                                            key=operator.attrgetter('questions_cnt'), reverse=not ascending)
            self.articles_list_all = sorted(self.articles_list_all, \
                                            key=operator.attrgetter('questions_cnt'), reverse=not ascending)
        elif rank_type == 'by_sum_cnt_answers':
            self.cur_articles_list = sorted(self.cur_articles_list, key=operator.attrgetter('sum_answers_cnt'),
                                            reverse=not ascending)
            self.articles_list_all = sorted(self.articles_list_all, key=operator.attrgetter('sum_answers_cnt'),
                                            reverse=not ascending)
        elif rank_type == 'by_date':
            self.cur_articles_list = sorted(self.cur_articles_list, \
                                            key=operator.attrgetter('last_date'), reverse=not ascending)
            self.articles_list_all = sorted(self.articles_list_all, key=operator.attrgetter('last_date'), \
                                            reverse=not ascending)

        self.is_ranked = True
        self.rank_type = rank_type

        write_current_article_list(self.cur_articles_list)

    # with open("./../data/statistics/current_article_list", "wb") as f:
    # 	pickle.dump(self.cur_articles_list, f, protocol=pickle.HIGHEST_PROTOCOL)


    def add_filter(self, filter_type, filter_data):
        """
        add filter by data or law
        filter_type = 'law' or 'date'
        date = "day-month-year"
        фильтр по дате - оставляю только те статьи,
        упоминание о котором есть позднее указанного числа
        if filter by date: filter_data is string: "year.month.day"
        if filter by law: filter_data - law name (ex. "Гражданский кодекс") -
        -здесь скорее всего должен быть выпадающий список
        """
        if filter_type in self.filters_type:
            pass
        else:
            if filter_type == 'law':
                self.cur_articles_list = [article for article in self.cur_articles_list \
          					if article.official_article.law.strip().lower() == filter_data.strip().lower()]

            if filter_type == 'date':
                date_parts = filter_data.strip().split(".")
                filter_date = date(int(date_parts[2]), \
                                   int(date_parts[1]), \
                                   int(date_parts[0]))

                self.cur_articles_list = [article for article in self.cur_articles_list \
                                          if article.last_date >= filter_date]

            self.filters_type.append(filter_type)
            self.filters_data.append(filter_data)

            write_current_article_list(self.cur_articles_list)

    def cancel_filter(self, filter_type):
        if filter_type in self.filters_type:
            self.filters_data.pop(self.filters_type.index(filter_type))
            self.filters_type.remove(filter_type)

        self.cur_articles_list = self.articles_list_all.copy()
        for i, f in enumerate(self.filters_type):
            self.add_filter(filter_type=f, filter_data=self.filters_data[i])

        write_current_article_list(self.cur_articles_list)

# index = StatisticsModule(recompute_statistics = True)
# index.add_filter(filter_type='law', filter_data = 'гражданский кодекс')

# # print(len(index.article_index))
# # # for idx, k in enumerate(index.article_index.keys()):
# # # 	if idx > 2:
# # # 		break
# # # 	print (k.to_dict())

# with open("./../data/statistics/current_article_list", "rb") as f:
# 	articles = pickle.load(f)

# 	for idx, k in enumerate(articles):
# 		if idx > 1:
# 			break

# 		print (k['official_article']['law'])

# 		print (k['questions_cnt'], len(get_questions(k['questions_filename'])), \
# 			get_questions(k['questions_filename'])[0])
