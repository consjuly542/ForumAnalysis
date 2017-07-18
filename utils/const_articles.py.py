
# coding: utf-8

# In[25]:

import urllib
import string
from bs4 import BeautifulSoup, NavigableString
import os
from os import listdir
from os.path import isfile, join
from lxml import html, etree
import sys
import re
import json


# In[35]:

class Article:

    def __init__(self):
        self.law = "None"             #без кавычек
        self.article = "None"         #без кавычек
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
    


# In[50]:

def law(y):
    r = r"\"(.+)\""
    return(re.findall(r, y)[0])


# In[45]:

def law_ID(y):
    r = r"(\d+)"
    return(re.findall(r, y)[0])


# In[29]:

def link_articles(soup):
    tree = html.fromstring(str(soup))
    content = tree.xpath('//li/a/text()')
    ref = tree.xpath('//li/a/@href')
    c = []
    j = 0
    base = "http://www.consultant.ru"
    for i in content:
        c.append((i,base+ref[j]))
        j = j+1
    #return(content, ref)
    return(c)


# In[31]:

def article(articles, articles_list, ID, law, date):
    chapter = 0
    for x in articles:
        
       # print(x)
        if (x[0].find('Глава')+1):
            #print(x[0])
            chapter = chapter+1
            continue
        elif (x[0].find('Статья')+1):
            a = Article()
            a.law = law
            a.law_ID = ID
            a.chapter_num = chapter
            a.date = date
            a.article = x[0]
            a.article_link = x[1]
            r = r"\s(\d+)"
            a.article_num = re.findall(r, str(x[0]))[0]
            a.article_ID = a.law_ID + '_' + a.article_num
            articles_list.append(a.to_dict())
    return(articles_list)


# In[51]:

g = open('links_law.txt', 'r')
f = open('article_list.txt', 'w', encoding='utf-8')
s = 'http://www.consultant.ru/document/cons_doc_LAW_28399/'
x = urllib.request.urlopen(s).read()
soup = BeautifulSoup(x, "lxml")

soup.prettify()

y = soup.title.string

articles_list = []

date = "1993.12.12"

articles = link_articles(soup)

json.dump(article(articles, articles_list, law_ID(s), law(y), date), f)    

  
#print((link_articles(soup)))

f.close()
g.close()


# In[ ]:



