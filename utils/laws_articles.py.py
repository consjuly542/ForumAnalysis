'''Script for creating list of articles from popular laws'''
# coding: utf-8

# In[1]:

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


# In[2]:

class Article:
    '''
	class Article
	'''
    def __init__(self):
	    '''
		Methods:
		----------
		law: name of law
		article: name of article
		article_num: number of article
		law_num: number of law
		flaw_num: number of federal law
		chapter_num: number of chapter
		date: date of enactment
		edit_date: date of amendment
		law_ID: ID of law from http://www.consultant.ru
		article_ID: law_ID + '_' + article_num
		article_link: link for page with article from http://www.consultant.ru
		'''
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
	    '''
		Convert Article to dictionary
		'''
        return self.__dict__
    


# In[3]:

def law(y):
    '''
	Searcher law name
	
	Parameters:
	------------
	*y (string): title of html page
	
	Returns:
	-----------
	* (string): result of searching in a srting
	'''
    r = r"\"(.+)\""
    return(re.findall(r, y)[0])


# In[4]:

def law_ID(y):
    '''
	Searcher law ID
	
	Parameters:
	------------
	*y (string): link for law on http://www.consultant.ru
	
	Returns:
	-----------
	* (string): result of searching in a srting
	'''
    r = r"(\d+)"
    return(re.findall(r, y)[0])


# In[5]:

def law_date(y):
    '''
	Searcher law date
	
	Parameters:
	------------
	*y (string): title of html page
	
	Returns:
	-----------
	* (string): result of searching in a srting
	'''
    r = r"от (\d+\.\d+\.\d+)"
    return(re.findall(r, y)[0])


# In[6]:

def date_convert(date):
    '''
	Convert date from 'dd.mm.yyyy' to 'yyyy.mm.dd'
	
	Parameters:
	-------------
	*date (string): date
	
	Returns:
	----------
	* (string): date
	'''
    return(date[6:10]+'.'+date[3:5]+'.'+date[0:2])


# In[7]:

def law_num(y):
    '''
	Searcher law number
	
	Parameters:
	------------
	*y (string): title of html page
	
	Returns:
	-----------
	* (string): result of searching in a srting
	'''
    r = r"N\s(\S+)\s"
    return(re.findall(r, y)[0])


# In[8]:

def link_articles(soup):
    '''
	Gets link for article and title of article from soup
	
	Parameters:
	-------------
	*soup (beautifulSoup type): html code of web-page
	
	Returns:
	---------
	* (list of tuples(string, string)): (title of article, link for article)
	'''
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


# In[9]:

def article(articles, articles_list, ID, law, date, law_num):
    '''
	Makes list of articles
	
	Parameters:
	------------
	*articles (list of tuples(string, string)): (title of article, link for article)
	*articles_list (list of dictionaries): list of articles, where every article is a dictionary
	*ID (string): law ID
	*law (string): law name
	*date (string): date of law enactment
	*law_num (string): law number
	
	Returns:
	-----------
	* (list of dictionaries): list of articles, where every article is a dictionary
    '''
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
            a.law_num = law_num
            a.date = date
            r = r"\d.?\s(.+)"
            article = re.findall(r, x[0])
            if(article == []):
                a.article = 'None'
            else:
                a.article = article[0]
#             a.article = re.findall(r, x[0])[0]
            a.article_link = x[1]
            r = r"\s(\d+)"
            a.article_num = re.findall(r, str(x[0]))[0]
            a.article_ID = a.law_ID + '_' + a.article_num
            articles_list.append(a.to_dict())
    return(articles_list)


# In[11]:
'''
main function
'''
g = open('links_law.txt', 'r')
f = open('article_list_laws.txt', 'w', encoding='utf-8')
articles_list = []
i = 0
s = g.readline()
#s = 'https://www.consultant.ru/document/cons_doc_LAW_305/'
while s:
    print(s)
    x = urllib.request.urlopen(s).read()
    soup = BeautifulSoup(x, "lxml")

    soup.prettify()

    y = soup.title.string
    print(i)
    if ((i==5)|(i==6)|(i==7)|(i==8)):
        date = '1994.11.30'
        num = '51-ФЗ'
        law_name = 'Гражданский кодекс Российской Федерации'
    elif (i==13):
        date = '1971.12.09'
        num = 'None'
        law_name = 'Кодекс законов о труде Российской Федерации'
    elif (i==17):
        date = '1998.07.31'
        num = '146-ФЗ'
        law_name = 'Налоговый кодекс Российской Федерации'
    elif (i==18):
        date = '2000.08.05'
        num = '117-ФЗ'
        law_name = 'Налоговый кодекс Российской Федерации'
    elif (i==29):
        date = '2014.10.04'
        num = '284-ФЗ'
        law_name = 'НК РФ Глава 32. НАЛОГ НА ИМУЩЕСТВО ФИЗИЧЕСКИХ ЛИЦ'
    elif (i==34):
        date = '2006.12.18'
        num = '230-ФЗ'
        law_name = 'ГК РФ Глава 70. АВТОРСКОЕ ПРАВО'
    elif (i==94):
        law_name = 'Об утверждении Перечня видов работ по инженерным изысканиям, по подготовке проектной документации, по строительству, реконструкции, капитальному ремонту объектов капитального строительства'
    else:
        date = law_date(y)
        date = date_convert(date)
        num = law_num(y)
        law_name = law(y)
    
    
    
    articles = link_articles(soup)
    
    article(articles, articles_list, law_ID(s), law_name, date, num)
    print(i)
    i = i+1
    s = g.readline()
    if(s == 95):
        break
#print(law_num(y)) 
#print(len(articles_list))
json.dump(articles_list, f)    

#print(article(articles, articles_list, law_ID(s), law(y), date, law_num(y)))


    
#print((link_articles(soup)))

f.close()
g.close()


# In[ ]:



