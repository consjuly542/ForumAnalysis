
# coding: utf-8

# In[1]:

import json
import os


# In[2]:

class Article:

    def __init__(self):
        self.law = "None"
        self.article = "None"
        self.article_num = "None"
        self.law_num = "None"
        self.flaw_num = "None"
        self.chapter_num = "None"
        self.date = "0000.00.00"
        self.edit_date = "0000.00.00"
        self.law_ID = "None"
        self.article_ID = "None"
        self.article_link = "None"

    def to_dict(self):
        return self.__dict__
    


# In[7]:

def load_data():
    f = open('article_list_laws.txt', 'r')
    data = json.load(f)
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

        print(a.to_dict())

if __name__ == '__main__':
    load_data()


# In[ ]:



