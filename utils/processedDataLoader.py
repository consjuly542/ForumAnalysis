from Question import Question9111

import json
import os


def load_data(dirpath='../data/processed'):
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
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

                q.answers_href_ref = d['answers_href_ref']
                q.answers_href_txt = d['answers_href_txt']
                q.answers = d['answers']
                q.questionID = d['questionID']

                print(q.to_dict())

if __name__ == '__main__':
    load_data()




