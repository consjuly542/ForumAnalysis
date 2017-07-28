'''Script for convertation link to article'''
import json
import os
import re
from links_searcher import Link
import pickle
from Article import Article

class Link2Article(object):
    '''
	class Link2Article
	'''

    def __init__(self):
        '''
        Methods:
        -----------
        article_list: loads list of articles
        article_dict: convert list to dict
        '''

        self.article_list = self.load_data()
        self.article_dict = self.list_to_dict(self.article_list)


    def link2article(self, link):
        '''
        Converts link to article

        Parameters:
        ------------
        *link (Link): link for article(law name or law number and article number)

        Returns:
        ------------
        * (Article): article with all information about it
        '''


        article_ID = self.link_to_article_ID(link, self.article_dict)
        if article_ID == None:
            return None
        a = Article()
        a = self.ID_to_Article(article_ID, self.article_list)
        return (a)


    def load_data(self):
        '''
    	Loads Article type
    	
    	Parameters:
    	------------
    	None
    	
    	Returns:
    	----------
    	* (list of dictionaries): list of dictionaries, where every article is a dictionary
    	'''
        f = open('../data/article_list_laws.txt', 'r')
        article_list = []
        data = json.load(f)
        # print(data)
        for d in data:
            a = Article()

            a.law = d['law']
            a.article = d['article']
            a.article_num = d['article_num']
            a.law_num = d['law_num']
            a.flaw_num = d['flaw_num']
            a.chapter_num = d['chapter_num']
            a.date = d['date']
            a.edit_date = d['edit_date']
            a.law_ID = d['law_ID']
            a.article_ID = d['article_ID']
            a.article_link = d['article_link']

            # print(a.to_dict)

            article_list.append(a.to_dict())

        return (article_list)


    def full_codec_name(self, law_name):
        '''
    	Makes full name of codecs
    	
    	Parameters:
    	-------------
    	*law_name (string): abbreviation of codecs
    	
    	Returns: 
    	----------
    	* (string): full name of codecs
    	'''
        if (law_name.find('апк') == 0):
            codec_name = 'арбитражный процессуальный кодекс российской федерации'
        elif (law_name.find('бк') == 0):
            codec_name = 'бюджетный кодекс российской федерации'
        elif (law_name.find('вк') == 0):
            codec_name = 'водный кодекс российской федерации'
        elif (law_name.find('гк') == 0):
            codec_name = 'гражданский кодекс российской федерации'
        elif (law_name.find('жк') == 0):
            codec_name = 'жилищный кодекс российской федерации'
        elif (law_name.find('зк') == 0):
            codec_name = 'земельный кодекс российской федерации'
        elif (law_name.find('кас') == 0):
            codec_name = 'кодекс административного судопроизводства российской федерации'
        elif (law_name.find('кзот') == 0):
            codec_name = 'кодекс законов о труде российской федерации'
        elif (law_name.find('тк') == 0):
            codec_name = 'трудовой кодекс российской федерации'
        elif (law_name.find('коап') == 0):
            codec_name = 'кодекс российской федерации об административных правонарушениях'
        elif (law_name.find('лк') == 0):
            codec_name = 'лесной кодекс российской федерации'
        elif (law_name.find('нк') == 0):
            codec_name = 'налоговый кодекс российской федерации'
        elif (law_name.find('ск') == 0):
            codec_name = 'семейный кодекс российской федерации'
        elif (law_name.find('тк') == 0):
            codec_name = 'трудовой кодекс российской федерации'
        elif (law_name.find('уик') == 0):
            codec_name = 'уголовно-исполнительный кодекс российской федерации'
        elif (law_name.find('упк') == 0):
            codec_name = 'уголовно-процессуальный кодекс российской федерации'
        elif (law_name.find('ук') == 0):
            codec_name = 'уголовный кодекс российской федерации'
        else:
            return (law_name)
        return (codec_name)


    def list_to_dict(self, article_list):
        '''
    	Converts list to dictionary
    	
    	Parameters:
    	-------------
    	*article_list (list of dictionaries): list of dictionaries, where every article is a dictionary
    	
    	Returns:
    	----------
    	* (dictionary of dictionaries of dictionaries): dictionary of laws, where every law is a dictionary with a dictionary of articles
    	'''
        law_dict = {}
        law_ID = article_list[0]['law_ID']
        law_dict[law_ID] = {'law_num': article_list[0]['law_num'], 'law_name': article_list[0]['law'],
                            'law_ID': article_list[0]['law_ID'], 'articles': {}}
        for article in article_list:
            if (law_ID == article['law_ID']):
                law_dict[law_ID]['articles'][article['article_num']] = article
            else:
                law_ID = article['law_ID']
                law_dict[law_ID] = {'law_num': article['law_num'], 'law_name': article['law'],
                                    'law_ID': article['law_ID'], 'articles': {}}
                law_dict[law_ID]['articles'][article['article_num']] = article

        return (law_dict)


    def load_link(self):
        '''
    	Loads Link type
    	
    	Parameters: 
    	-------------
    	None
    	
    	Returns:
    	-----------
    	* (Link): link for article(law name or law number and article number)
    	'''
        with open("./links_example", "rb") as f:
            links_example = pickle.load(f)
            return (links_example)


    def link_to_article_ID(self, link, article_dict):
        '''
    	Gets article ID 
    	
    	Parameters:
    	------------
    	*link (Link): link for article(law name or law number and article number)
    	*article_dict (dictionary of dictionaries of dictionaries): dictionary of laws, where every law is a dictionary with a dictionary of articles
    	
    	Returns:
    	* (string): article ID
    	'''
        article_ID = ''
        number = link.law_num
        name = link.law_name
        article = link.article_num
        ID = self.law_searcher(number, name, article_dict)
        #     print(article_dict[ID]['law_name'])
        if ID == '':
            return None
        for art in article_dict[ID]['articles']:
            #         print(article_dict[ID]['articles'][art]['article_num'])

            if article == article_dict[ID]['articles'][art]['article_num']:
                article_ID = article_dict[ID]['articles'][art]['article_ID']
                break
        if (article_ID == ''):
            return None
        return article_ID


    def law_searcher(self, number, name, a_dict):
        '''
    	Searches law in the dictionary
    	
    	Parameters:
    	-------------
    	*number (string): law number
    	*name (string): law name
    	*a_dict (dictionary of dictionaries of dictionaries): dictionary of laws, where every law is a dictionary with a dictionary of articles
    	
    	Returns:
    	----------
    	* (string): law ID
    	'''
        ID = ''
        if name:
            name = self.full_codec_name(name)
        if number:
            for law in a_dict:
                if number.find(a_dict[law]['law_num']) == 0:
                    number = a_dict[law]['law_num']
                    ID = a_dict[law]['law_ID']
                    break
        elif name:
            for law in a_dict:
                if name == a_dict[law]['law_name'].lower():
                    name = a_dict[law]['law_name']
                    ID = a_dict[law]['law_ID']
                    break
        return (ID)


    def ID_to_Article(self, article_ID, article_list):
        '''
    	Gets article from ID
    	
    	Parameters:
    	-------------
    	*article_ID (string): article ID
    	*article_list (list of dictionaries): list of dictionaries, where every article is a dictionary
    	
    	Returns:
    	---------
    	* (Article): article information
    	'''
        a = Article()
        for art in article_list:
            if article_ID == art['article_ID']:
                a.law = art['law']
                a.article = art['article']
                a.article_num = art['article_num']
                a.law_num = art['law_num']
                a.flaw_num = art['flaw_num']
                a.chapter_num = art['chapter_num']
                a.date = art['date']
                a.edit_date = art['edit_date']
                a.law_ID = art['law_ID']
                a.article_ID = art['article_ID']
                a.article_link = art['article_link']
                break
        return (a)

# def link_to_article(link):
#     article_list = load_data()
#     article_dict = list_to_dict(article_list)
#     article_ID = link_to_article_ID(link, article_dict)
#     if article_ID is None:
#         return None
#     a = Article()
#     a = ID_to_Article(article_ID, article_list)

#     return(a)
