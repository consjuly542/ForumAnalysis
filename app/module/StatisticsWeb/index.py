import os.path
import sys

sys.path.append('C:\\Users\\NRS-GromovSI\\Documents\\ForumAnalysis\\source')
from ArticleStatistics import ArticleStatistics

import pickle
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import os.path
import datetime
from definitions import ROOT_DIR

def time_str(date):
    return ('%s' % date.replace(microsecond=0))

statistics_page = Blueprint('statistics_page', __name__,
                        template_folder='templates')

@statistics_page.route('/')
def get_view():
    data = None
    with open(os.path.join(ROOT_DIR, 'data/res/current_article_list'), 'rb') as f_in:
        data = pickle.load(f_in)
    data = data[:20]
    # for idx, item in enumerate(data):
    #     data[idx]['official_article'].date = '.'.join(reversed(item['official_article'].date.split('.')))
    #     data[idx]['official_article'].law = ''.join([i[0].upper() for i in item['official_article'].law.split()])
    try:
        return render_template('Statistics/index.html', data=data)
    except TemplateNotFound:
        abort(404)

# @statistics_page.route('/run', methods=['POST'])
# def run():
#     module = LinkSearcherModule(
#         'LinkSearcher',
#         'C:\\Users\\NRS-GromovSI\\Documents\\ForumAnalysisWeb\\data\\pro',
#         'C:\\Users\\NRS-GromovSI\\Documents\\ForumAnalysisWeb\\data\\res\\LinkSearcher')
#     module.run('test.txt', 'test-links.txt')
#     data = None
#     with open(path.join(module.dir_target, 'test-links.txt'), 'r') as f_in:
#         data = json.load(f_in)
#     return render_template('LinkSearcher/LinkSearcher_result.html', data=data)
    # data = sorted(data, key=lambda i: i['sum_answers_cnt'], reverse=True)[:20]
