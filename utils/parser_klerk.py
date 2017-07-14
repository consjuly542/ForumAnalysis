''' Script for Klerk forum data parsing '''

import argparse
import os
from os import path
import re
import string
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import simplejson as json

from Question import QuestionKlerk as Q

def time_str():
    ''' Returns a datetime string '''
    return ('%s' % datetime.now().replace(microsecond=0)).replace(' ', '_')

def get_topic_title(soup):
    '''
    Gets topic title from thread page

    Parameters
    ------------
    * soup (beautifulSoup object): thread page

    Returns
    ------------
    * (string): topic title
    '''
    title = soup.find_all('span', {'class': 'threadtitle'})
    if not title:
        return None
    children = title[0].find_all('a')
    if not children:
        return None
    return children[0].text


def get_date(soup):
    '''
    Gets topic creation date from thread page in YYYY.MM.DD format

    Parameters
    ------------
    * soup (beautifulSoup object): thread page

    Returns
    ------------
    * (string): topic creation date
    '''
    container = soup.find_all('li', {'class': 'postcontainer'})
    if not container:
        return None
    container = container[0]
    date = container.find_all('span', {'class': 'date'})[0].text
    date = date.split(',')[0]
    date = '.'.join(reversed(date.split('.')))
    return date

def get_answers_count(soup):
    '''
    Gets number of answers in thread from thread page

    Parameters
    ------------
    * soup (beautifulSoup object): thread page

    Returns
    ------------
    * (int): number of answers
    '''
    poststats = soup.find_all('div', {'class': 'postpagestats'})
    if not poststats:
        return None
    poststats = poststats[0].text
    return int(poststats.strip().split(' ')[-1]) - 1

def get_themes(soup):
    '''
    Gets thread themes from breadcrumbs
    (e.g. Бухгалтерия -> Общая бухгалтерия -> Бухучет и Налогообложение)

    Parameters
    ------------
    * soup (beautifulSoup object): thread page

    Returns
    ------------
    * (string[]): arrays of thread themes
    '''
    ret = []
    themes = soup.find_all('li', {'class', 'navbit'})
    for theme in themes[1:]:
        ret.append(theme.text)
    return ret

def get_post_text(soup):
    '''
    Gets post text from post html object (class: postbitim)

    Parameters
    ------------
    * soup (beautifulSoup object): post html object

    Returns
    ------------
    * (string): post text
    '''
    container = soup.find_all('blockquote')
    if not container:
        return None
    return container[0].text.strip()

def get_post_hrefs(soup):
    '''
    Gets post hyperlinks (text and href) from post html object (class: postbitim)

    Parameters
    ------------
    * soup (beautifulSoup object): post html object

    Returns
    ------------
    * (string[], string[]): tuple of (array of texts) and (array of hrefs)
    '''
    container = soup.find_all('blockquote')
    if not container:
        return None

    post_href_texts = []
    post_href_refs = []
    post_hrefs = [(a.string, a.get('href')) for a in container[0].find_all('a')]
    for href in post_hrefs:
        text = href[0]
        if not text:
            continue
        ref = href[1]
        post_href_texts.append(text)
        post_href_refs.append(ref)
    return post_href_texts, post_href_refs

def exists(data, idx):
    '''
    Checks if provided topic id exists in data array

    Parameters
    ------------
    * data (QuestionKlerk[]): array of questions
    * idx (string): index of question to search

    Returns
    ------------
    * (boolean): True if found, False otherwise
    '''
    res = False
    for d in data:
        if d.idx == idx:
            res = True
            break
    return res

def update_views_count(data, idx, views_count):
    '''
    Updates views_count of object in data array

    Parameters
    ------------
    * data (QuestionKlerk[]): array of questions
    * idx (string): index of question to update
    * views_count (int): new views_count

    Returns
    ------------
    * (boolean): Index of updated element if updated, False otherwise
    '''
    #print(idx, views_count)
    for i, d in enumerate(data):
        if d.idx == idx:
            data[i].views_count = views_count
            return i
    return False

def add_thread_data(data, q_data):
    '''
    Function for updating specific Question (with the same id as q_data has)
    (for multi-page threads)

    Parameters
    ------------
    * data (QuestionKlerk[]): array of questions
    * q_data (QuestionKlerk): question data that contains updated values

    Returns
    ------------
    None
    '''
    for i, d in enumerate(data):
        if q_data.idx == d.idx:
            data[i].question_href_ref = data[i].question_href_ref + q_data.question_href_ref
            data[i].question_href_txt = data[i].question_href_txt + q_data.question_href_txt
            data[i].answers_href_ref = data[i].answers_href_ref + q_data.answers_href_ref
            data[i].answers_href_txt = data[i].answers_href_txt + q_data.answers_href_txt
            data[i].answers = data[i].answers + q_data.answers

def dump_data(name, data, batch_size):
    '''
    Cuts data into batches and dumps them into json files

    Parameters
    ------------
    * name (string): filename prefix [<name>-<batch_number>] (may include path)
    * data (QuestionKlerk[]): array of questions
    * batch_size (int): batch size

    Returns
    ------------
        None
    '''
    length = len(data)
    for i in range(int(length / batch_size)):
        batch = data[i*batch_size:(i+1)*batch_size]
        if not dump_batch(name, batch, i):
            break

def dump_batch(name, batch, batch_number):
    '''
    Dumps data batch into json file

    Parameters
    ------------
    * name (string): filename prefix [<name>-<batch_number>] (may include path)
    * batch (QuestionKlerk[]): array of questions (batch)
    * batch_number (int): batch number

    Returns
    ------------
        (boolean): True if dumped, False otherwise
    '''
    batch_dict = [q.to_dict() for q in batch]
    if len(batch_dict) == 0:
        return False
    with open(name + '-' + str(batch_number), 'w', encoding='utf-8') as fp_out:
        json.dump(batch_dict, fp_out)
    return True

def main():
    ''' Main function '''
    print(sys.argv[0])
    print('\nScript for Klerk forum data parsing')

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the folder with Klerk forum data")
    parser.add_argument("-m", "--max", help="Maximum number of threads to get")
    parser.add_argument("-d", "--dump", help="Path to the folder for dumps")
    parser.add_argument("-b", "--batch", help="Number of questions to dump in one file")
    args = parser.parse_args()

    data_path = args.input
    max_cnt = args.max
    dump_folder = args.dump
    batch_size = args.batch

    print('\nData Path:', data_path)
    if max_cnt:
        max_cnt = int(max_cnt)
        print('Max Count:', max_cnt)
    if not dump_folder:
        os.system('mkdir dump')
        dump_folder = 'dump'
    print('Dump Folder:', dump_folder)
    if not batch_size:
        batch_size = 20
    else:
        batch_size = int(batch_size)
    print('Batch Size:', batch_size)

    idxs = []
    data = []
    views = []
    cnt = 0
    # batch_cnt = 0
    # batch_number = 0
    stop_flag = False
    # TODO: optimize crawling
    for root, dirs, _ in os.walk(data_path):
        for d in dirs:
            #is_theme_folder = re.search(r'^\d+$', d)
            for rt, _, ff in os.walk(path.join(root, d)):
                for f in ff:
                    # print(path.join(rt, f))
                    with open(path.join(rt, f), 'r', encoding='utf8') as f_in:
                        print(time_str(), path.join(rt, f))
                        if not f_in:
                            continue

                        # check if file is thread file
                        # it is thread file if it has numeric only name
                        # and its name is more than 2 symbols
                        is_thread = re.search(r'[0-9]+', f)
                        if is_thread and len(f.split('.')[0]) > 2:
                            is_thread = True
                        else:
                            is_thread = False

                        soup = BeautifulSoup(f_in, 'html.parser')
                        if is_thread:
                            title_container = soup.find_all('span', {'class': 'threadtitle'})
                            if not title_container:
                                continue
                            idx = title_container[0].find_all('a')[0].get('href').split('=')[-1]
                            title = get_topic_title(soup)
                            date = get_date(soup)
                            answers_count = get_answers_count(soup)
                            themes = get_themes(soup)

                            posts = soup.find_all('li', {'class': 'postbitim'})
                            if not posts:
                                continue
                            question_full = get_post_text(posts[0])
                            post_href_texts, post_href_refs = get_post_hrefs(posts[0])
                            question_href_ref = post_href_refs
                            question_href_txt = post_href_texts

                            answers = []
                            answers_href_ref = []
                            answers_href_txt = []
                            for post in posts[1:]:
                                answers.append(get_post_text(post))
                                post_href_texts, post_href_refs = get_post_hrefs(post)
                                for ref in post_href_refs:
                                    answers_href_ref.append(ref)
                                for txt in post_href_texts:
                                    answers_href_txt.append(txt)

                            q = Q()
                            q.idx = idx
                            q.date = date
                            q.answers_count = answers_count
                            q.themes_list = themes
                            q.question_title = title
                            q.question_full = question_full
                            q.question_href_ref = question_href_ref
                            q.question_href_txt = question_href_txt
                            q.answers_href_ref = answers_href_ref
                            q.answers_href_txt = answers_href_txt
                            q.answers = answers

                            if idx in idxs:
                                add_thread_data(data, q)
                                print('update')
                            else:
                                data.append(q)
                                idxs.append(idx)
                                cnt = cnt + 1
                                print('add')
                                if cnt % batch_size == 0:
                                    print("******:::", cnt)
                            # batch_cnt = batch_cnt + 1
                            # if batch_cnt == batch_size:
                            #     dump_batch(path.join(dump_folder, 'data' + str(max_cnt)), data, batch_number)
                            #     data.clear()
                            #     batch_number = batch_number + 1
                                if max_cnt and cnt >= max_cnt:
                                    stop_flag = True
                                    break
                        else:
                            topics = soup.find_all('li', {'class': 'threadbit'})
                            for topic in topics:
                                idx = topic.get('id').split('_')[1]
                                thread_stats = topic.find_all('ul', {'class': 'threadstats'})[0].text.split()
                                # if thread_stats length is less than 4 then there is no views_count
                                if len(thread_stats) < 4:
                                    continue
                                views_count = ''.join(s if s not in string.punctuation else '' for s in thread_stats[3])
                                views_count = int(views_count) if views_count else -1
                                updated = update_views_count(data, idx, views_count)
                                if not updated:
                                    views.append((idx, views_count))
                                # date_label = topic.find_all('span', {'class': 'label'})[0].text.strip()
                                # date = date_label.split()[1]
                                # answers_count = ''.join(s if s not in string.punctuation else '' for s in thread_stats[1])
                                # answers_count = int(answers_count) if answers_count else -1
                if stop_flag:
                    break
            if stop_flag:
                break
        if stop_flag:
            break
    for view in views:
        update_views_count(data, view[0], view[1])

    dump_data(path.join(dump_folder, 'data' + str(max_cnt)), data, batch_size)

if __name__ == '__main__':
    main()
