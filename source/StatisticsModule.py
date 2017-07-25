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
from PlotsMaker import plot_dates


def data2dict(s_data):
    """
    Convert list of class to 
    list of dictionary with convert date to one format.

    Parameters
    ------------
    *s_data (list of instance ArticleStatistics)
    
    Returns
    ------------
    *data  (list of dictionary): converted list

    """
    data = copy(s_data)
    for i, d in enumerate(data):
        if d:
            for j, dt in enumerate(data[i].dates):
                data[i].dates[j] = convert_date(dt)
            data[i].last_date = convert_date(data[i].last_date)
            data[i].first_date = convert_date(data[i].first_date)
            data[i].official_article.date = convert_date(data[i].official_article.date)
            data[i].official_article.edit_date = convert_date(data[i].official_article.edit_date)
            data[i].official_article = d.official_article.__dict__
            data[i] = d.__dict__
        else:
            print( d.to_dict())
    return data


def convert_date(dt):
    """
    Convert all date formats to one format

    Parameters
    ------------
    *dt: date to converting
    
    Returns
    ------------
    *q  (string): date in string format
    """
    if not isinstance(dt, str):
        dt = str(dt)
    parts = re.split(r'\.|\_|\-', dt)
    if len(parts) == 1:
        parts = str(dt).split('.')
    if len(parts[0]) == 4:
        return '.'.join(reversed(parts))
    return str(dt)


def write_current_article_list(articles_list, cnt_visible_article=70):
    """
    Writing top = cnt_visible_article articles, 
    which user want to see, to a file.

    Parameters
    -------------
    *articles_list (list of instance ArticleStatistics): all articles
    *cnt_visible_article (int): count of visible articles 
    """
    with open("./../data/statistics/current_article_list", "wb") as f:
        article_dict = data2dict(copy(articles_list)[:cnt_visible_article])
        cPickle.dump(article_dict, f, protocol=pickle.HIGHEST_PROTOCOL)


class StatisticsModule(object):
    """
    Module for agregate statistics.

    Attributes
    ------------
    *cur_articles_list (list of ArticleStatistics) 
                - list of articles with ranling and filters
    *articles_list_all (list of ArticleStatistics)
                - list of articles with ranking without filters
                (for fast execution)
    *filters_type (list of string)
                - list of applied filters
    *filters_data (list of string)
                -list of data for applied filters

    Methods
    ----------
    *get_article_index() - build empty index from official article
    *get_article_statistics() - agregate staticstics from both forums
    *ranking_articles() - ranking articles with given type
    *get_graphics() - creation plot of interest for each article
    *add_filter() - add filter with given data and type
    *cancel_filter() - cancel filter with given type
    """
    def __run__(self, file_origin, file_target):
        pass

    def __init__(self, recompute_statistics=False):
        """
        Initiation of module.

        Parameters
        ------------
        *recompute_statistics(boolean): if True, statistics are calculated again,
                                    if False, statistics are loaded from file
        
        """
        self.get_article_statistics(recompute_statistics=recompute_statistics)
        # list which users see
        self.cur_articles_list = list(self.article_index.values())
        self.cur_articles_list = [a for a in self.cur_articles_list if a.questions_cnt > 0]
        # ranking list of articles without filters - for fast execution
        self.articles_list_all = list(self.article_index.values())
        self.articles_list_all = [a for a in self.articles_list_all if a.questions_cnt > 0]

        # filters list
        self.filters_type = []
        self.filters_data = []

        with open("../data/processed_articles/guide_article_ID", "rb") as f:
            self.ids_in_guides = cPickle.load(f)

        # print (len(self.ids_in_guides))

        # default - ranked by cnt_questions, no filters
        # self.ranking_articles(rank_type='by_cnt_questions')

    def get_article_index(self):
        """
        Create dictionary {article:article_statistics} -
        Empty index for future statistics
        """
        articles = load_file_article.load_data()
        print ("Count official articles: %d" % len(articles))
        self.article_index = {a.article_ID: ArticleStatistics(a) for a in articles}

        with open("./../data/statistics/article_index", "wb") as f:
            cPickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)

    def get_article_statistics(self, recompute_statistics=True):
        """
        Agregate statistics from both forum.
        """
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

                    sys.stderr.write("\r\t\t\t\t\tALL LINKS: %d; CAN't MATCH: %d" % (links_cnt, cnt_not_match_links))

            with open("./../data/statistics/article_statistics", "wb") as f:
                cPickle.dump(self.article_index, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open("./../data/statistics/article_statistics", "rb") as f:
                self.article_index = cPickle.load(f)

    def apply_rank_and_filters(self, rank_type = 'by_cnt_questions', ascending = False, filters_list = {}):
        """
        filters_list = [{'filter_type': (string), 'filter_data': (string)}]
        """
        print (rank_type, ascending, filters_list)
        cnt_visible_article = 70
        new_articles_list = copy(self.cur_articles_list)
        new_articles_list = self.ranking_articles(new_articles_list, rank_type, ascending)
        # print new_articles_list
        for filt in filters_list:
            new_articles_list = self.add_filter(new_articles_list, filt['filter_type'], filt['filter_data'])

        return new_articles_list[:cnt_visible_article]


    def ranking_articles(self, articles_list, rank_type='by_cnt_questions', ascending = False):
        if rank_type == 'by_cnt_questions':
            articles_list = sorted(articles_list, \
                                            key=operator.attrgetter('questions_cnt'), reverse=not ascending)
            articles_list = sorted(articles_list, \
                                            key=operator.attrgetter('questions_cnt'), reverse=not ascending)
        elif rank_type == 'by_sum_cnt_answers':
            articles_list = sorted(articles_list, key=operator.attrgetter('sum_answers_cnt'),
                                            reverse=not ascending)
            articles_list = sorted(articles_list, key=operator.attrgetter('sum_answers_cnt'),
                                            reverse=not ascending)
        elif rank_type == 'by_date':
            articles_list = sorted(articles_list, \
                                            key=operator.attrgetter('last_date'), reverse=not ascending)
            articles_list = sorted(articles_list, key=operator.attrgetter('last_date'), \
                                            reverse=not ascending)

        return articles_list
        # write_current_article_list(self.cur_articles_list)

    def get_graphics(self, dirpath = "../app/static/article_pics/"):
        with open("./../data/statistics/article_statistics", "rb") as f:
            self.article_index = cPickle.load(f)

        for idx, article_ID in enumerate(self.article_index.keys()):
            sys.stderr.write("\r %d / %d" % (idx, len(list(self.article_index.keys()))))
            if len(self.article_index[article_ID].dates) >= 1:
                # print (self.article_index[article_ID].dates[:10])
                plot_dates(self.article_index[article_ID].dates, dirpath + article_ID)



    def add_filter(self, articles_list, filter_type, filter_data):
        """
        add filter by data or law
        filter_type = 'law' or 'date' or 'not_in_guide'
        date = "day-month-year"
        фильтр по дате - оставляю только те статьи,
        упоминание о котором есть позднее указанного числа
        фильтр 'not_in_guide' - отсеивает те, на которые есть ссылки из путеводителей
        if filter by date: filter_data is string: "year.month.day"
        if filter by law: filter_data - law name (ex. "Гражданский кодекс") -
        """

        # if filter_type in self.filters_type:
            # pass
        # else:
        if filter_type == 'law':
            articles_list = [article for article in articles_list \
      					if article.official_article.law.strip().lower() == filter_data.strip().lower()]

        if filter_type == 'date':
            date_parts = filter_data.strip().split(".")
            filter_date = date(int(date_parts[2]), \
                               int(date_parts[1]), \
                               int(date_parts[0]))

            articles_list = [article for article in articles_list \
                                      if article.last_date >= filter_date]

        if filter_type == 'notInGuide' and filter_data == "0":
            articles_list = [article for article in articles_list\
                                     if article.official_article.article_ID not in self.ids_in_guides]
            print( len(articles_list))


        self.filters_type.append(filter_type)
        self.filters_data.append(filter_data)

        return articles_list
            # write_current_article_list(self.cur_articles_list)

    def cancel_filter(self, filter_type):
        if filter_type in self.filters_type:
            self.filters_data.pop(self.filters_type.index(filter_type))
            self.filters_type.remove(filter_type)

        self.cur_articles_list = self.articles_list_all.copy()
        for i, f in enumerate(self.filters_type):
            self.add_filter(filter_type=f, filter_data=self.filters_data[i])

        write_current_article_list(self.cur_articles_list)

# index = StatisticsModule(recompute_statistics = True)
# index = StatisticsModule(recompute_statistics = False)

# index = StatisticsModule(recompute_statistics = False).get_graphics()
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
