'''Script for loading question type'''
# -*- coding: utf-8 -*-

from Question import Question9111
from Question import QuestionKlerk

import json
import os
import sys
import glob


def load_data(dirpath='./data/processed'):
    '''
	Loads data Question's type
	
	Parameters:
	-------------
	*dirpath (string): path to directory of file
	
	Returns:
	-------------
	* (list of Question type): list of questions
	'''
    question_list = []
    for filename in os.listdir(dirpath)[:120]:
        filepath = os.path.join(dirpath, filename)
        with open(filepath) as input_file:
            data = json.load(input_file)
            
            #print(data)
            for d in data:
                q = Question9111()
                q.date = d['date']
                q.answers_count = d['answers_count']
                q.views_count = d['views_count']
                q.region = d['region']
                q.themes_list = d['themes_list']

                q.question_title = d['question_title']
                q.question_full = d['question_full']
                q.question_href_ref = d['question_href_ref']
                q.question_href_txt = d['question_href_txt']

                q.answers_href_txt = d['answers_href_txt']
                q.answers_href_ref = d['answers_href_ref']
                q.answers = d['answers']
                q.questionID = d['questionID']
                question_list.append(q)
                
    return question_list

def loadDataGenerator(dirpath = '../data/processed'):
    '''
	Loads data Question's type in generator
	
	Parameters:
	-------------
	*dirpath (string): path to directory of file
	
	Returns:
	-------------
	* (generator of Question type): list of questions
	'''
    listdir = os.listdir(dirpath)
    cur_file = 0
    batch_size = 1
    if "klerk" in listdir:
        listdir.remove("klerk")
    klerk_file = glob.glob('../data/processed/klerk/*', \
        recursive=True)
    print (len(klerk_file))
    listdir += klerk_file
    listdir = listdir
    while cur_file < len(listdir):
        sys.stderr.write("\rPrepare %d / %d files, cur_file: %s" % \
            (cur_file, len(listdir), listdir[cur_file]))
        question_list = []
        for filename in listdir[cur_file:cur_file + batch_size]:

            if filename not in klerk_file:
                filepath = os.path.join(dirpath, filename)
            else:
                filepath = filename

            with open(filepath, encoding = 'utf-8') as input_file:
                data = json.load(input_file)
                
                for d in data:
                    if filename.lower().find("klerk") != -1:
                        q = QuestionKlerk()
                        q.idx = d['idx']
                    else:
                        q = Question9111()
                        q.questionID = d['questionID']

                    q.date = d['date']
                    q.answers_count = d['answers_count']
                    q.views_count = d['views_count']
                    q.region = d['region']
                    q.themes_list = d['themes_list']

                    q.question_title = d['question_title']
                    q.question_full = d['question_full']
                    q.question_href_ref = d['question_href_ref']
                    q.question_href_txt = d['question_href_txt']

                    q.answers_href_ref = d['answers_href_txt']
                    q.answers_href_txt = d['answers_href_ref']
                    q.answers = d['answers']
                    question_list.append(q)

        cur_file += batch_size
        yield question_list

# if __name__ == '__main__':
#     load_data()




