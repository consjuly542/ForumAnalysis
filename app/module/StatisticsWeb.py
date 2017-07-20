from definitions import ROOT_DIR
import sys
import os.path
sys.path.append(os.path.join(ROOT_DIR, 'source/'))

from source.ArticleStatistics import ArticleStatistics

import re
import pickle
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

def data2dict(data):
    for i, d in enumerate(data):
        for j, dt in enumerate(data[i].dates):
            data[i].dates[j] = convert_date(dt)
        data[i].last_date = convert_date(data[i].last_date)
        data[i].first_date = convert_date(data[i].first_date)
        data[i].official_article.date = convert_date(data[i].official_article.date)
        data[i].official_article.edit_date = convert_date(data[i].official_article.edit_date)
        for j, dt in enumerate(data[i].questions):
            data[i].questions[j].date = convert_date(dt.date)
            data[i].questions[j] = dt.__dict__
        data[i].official_article = d.official_article.__dict__
        data[i] = d.__dict__
    return data

def convert_date(dt):
    if not isinstance(dt, str):
        dt = str(dt)
    parts = re.split(r'\.|\_|\-', dt)
    if len(parts) == 1:
        parts = str(dt).split('.')
    if len(parts[0]) == 4:
        return '.'.join(reversed(parts))
    return str(dt)

statistics_page = Blueprint('statistics_page', __name__,
                            template_folder='templates')

@statistics_page.route('/')
def get_view():
    data = None
    with open(os.path.join(ROOT_DIR, 'data/statistics/current_article_list'), 'rb') as f_in:
        data = pickle.load(f_in)
    s_data = data2dict(data)
    # for idx, item in enumerate(data):
    #     data[idx]['official_article'].date = '.'.join(reversed(item['official_article'].date.split('.')))
    #     data[idx]['official_article'].law = ''.join([i[0].upper() for i in item['official_article'].law.split()])
    try:
        return render_template('Statistics/index.html', data=s_data)
    except TemplateNotFound:
        abort(404)

# @statistics_page.route('/run', methods=['POST'])
# def run():
