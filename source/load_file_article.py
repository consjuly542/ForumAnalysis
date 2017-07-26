'''Script for loading Article type'''
import json
import os
from Article import Article
from guides import Guide
import _pickle as cPickle
import pickle
    
def load_data():
    '''
	Loads Article type
	
	Parameters:
	------------
	None
	
	Returns:
	----------
	* (list of dictionaries): list of dictionaries, where every article is a dictionary
	'''
    article_list = []
    f = open('../data/article_list_laws.txt', 'r')
    data = json.load(f)
    with open("../data/guide_articles/guides_list", "rb") as f:
        guides_list = cPickle.load(f)
    #print(data)
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

        for guide in guides_list:
            link = guide.get_link(a.article_ID)
            if link:
                a.guide_name = guide.name
                a.guide_link = link
                break

        article_list.append(a)

    f.close()
    return article_list




