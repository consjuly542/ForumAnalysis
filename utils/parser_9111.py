# -*- coding: utf-8 -*-
import codecs
from lxml import html, etree
import string
import time
import json
from datetime import datetime
import sys
import re
from w3lib.html import remove_tags

import os
from os import listdir
from os.path import isfile, join
import rarfile
import re

import argparse

from Question import Question9111

def time_str():
    return ('%s' % datetime.now().replace(microsecond=0)).replace(' ','_')

def make_question_card(text):
    trantab = str.maketrans(dict.fromkeys('\n\r\t'))

    tree = html.fromstring(text)

    region_txt = tree.xpath('//div[@class = "info-statistik"]/text()')
    region = region_txt[0].translate(trantab)[:-1].replace('\xa0', '')

    question_title = tree.xpath('//h1[@class = "q-main__body-title"]/text()')[0]

    question_main_body_href_txt = tree.xpath('//div[@class = "q-main__body"]/p/a/text()')

    question_main_body_href_ref = tree.xpath('//div[@class = "q-main__body"]/p/a/@href')

    question_html = tree.xpath('//div[@class = "q-main__body"]')
    question_txt = ""
    for q_html in question_html:
        r = remove_tags(etree.tostring(q_html, encoding='utf-8')).replace('&#13;', '')
        question_txt = question_txt + r.translate(trantab)

    views_txt = tree.xpath('//div[@class = "info__q-number"]/div[@class = "info-statistik"]/text()')
    views = ''
    if (views_txt != []):
        views = [int(s) for s in views_txt[0].split() if s.isdigit()][0]

    ur_ans_txt = tree.xpath('//h2[@class = "ur_ans"]/text()')
    ur_ans = [int(s) for s in ur_ans_txt[0].split() if s.isdigit()][0]

    answers_html = tree.xpath('//div[@class = "a-main__body-txt"][@itemprop = "text"]/p')
    answers_txt = []
    for ans_html in answers_html:
        r = remove_tags(etree.tostring(ans_html, encoding='utf-8')).replace('&#13;', '')
        answers_txt.append(r.translate(trantab))

    answers_href_txt = tree.xpath('//div[@class = "a-main__body-txt"][@itemprop = "text"]/p/a/text()')

    answers_href_ref = tree.xpath('//div[@class = "a-main__body-txt"][@itemprop = "text"]/p/a/@href')

    theme = tree.xpath('//span[@class = "breadcrumbs-link breadcrumbs-link__text"]/text()')

    q = Question9111()
    q.region = region
    q.question_title = question_title
    q.question_full = question_txt
    q.question_href_ref = question_main_body_href_ref
    q.question_href_txt = question_main_body_href_txt
    q.views_count = views
    q.answers_count = ur_ans
    q.answers_href_txt = answers_href_ref
    q.answers_href_ref = answers_href_txt
    q.themes_list = theme[1:]
    q.answers = answers_txt

    return q

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('num', type=int, default=None)
    args = parser.parse_args()
    num = int(args.num)

    dirpath = '../../9111/2017_'
    xpath= './tmp'+str(num)+'.txt'

    answers_list = []
    i = 0
    j = 0
    print(time_str())

    filepath = dirpath + str(num) + '.rar'
    with rarfile.RarFile(filepath) as opened_rar:
        for f in opened_rar.infolist():
            if(f.filename.count('/') == 2):
                text = opened_rar.read(f, 'r')
                out = codecs.open(xpath, "wb")
                out.write(text)
                out.close()
                text = codecs.open(xpath, "r", "utf-8").read()
                q = make_question_card(text)
                q.date = re.search( r'(\d{4}_\d+_\d+)', f.filename).group(1)
                q.questionID = re.search( r'(q\d+)', f.filename).group(1)
                answers_list.append(q.to_dict())
                i = i + 1
                if(i == 2000):
                    print(f.filename, j, time_str())
                    with open('data_'+str(num)+'_'+str(j), 'w') as outfile:
                        json.dump(answers_list, outfile)
                    i = 0
                    j = j + 1
                    answers_list = []

if __name__=='__main__':
    main()