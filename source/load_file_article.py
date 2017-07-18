import json
import os
from Article import Article
    
def load_data():
    law_list = []
    f = open('../data/article_list_laws.txt', 'r')
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

        law_list.append(a)

    return law_list

if __name__ == '__main__':
    print(len(load_data()))




