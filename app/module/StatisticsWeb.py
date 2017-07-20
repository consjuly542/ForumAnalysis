from definitions import ROOT_DIR
import sys
import os.path
import json
sys.path.append(os.path.join(ROOT_DIR, 'source/'))

from source.StatisticsModule import StatisticsModule

from source.ArticleStatistics import ArticleStatistics

import re
import _pickle as pickle
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

statistics_page = Blueprint('statistics_page', __name__,
                            template_folder='templates')

stats_module = StatisticsModule()

def get_data():
    data = None
    with open(os.path.join(ROOT_DIR, 'data/statistics/current_article_list'), 'rb') as f_in:
        data = pickle.load(f_in)
    return data

def load_codex_list():
    codex_list = None
    with open(os.path.join(ROOT_DIR, 'data/res/codex_list'), 'rb') as f_in:
        codex_list = pickle.load(f_in)
    return codex_list

@statistics_page.route('/', methods=['GET', 'POST'])
def get_view():
    # data:
    # -> rank: (string)
    # -> filters: [{'filter_type': (string), 'filter_data': (string)}]
    if request.method == 'POST':
        req_data = request.get_json(force=True)
        r_rank = req_data['rank']
        r_filters = req_data['filters']
        stats_module.ranking_articles(rank_type=(r_rank if r_rank else 'by_cnt_questions'))
        # Cancel prev. filters
        stats_module.cancel_filter('law')
        stats_module.cancel_filter('date')

        if r_filters:
            for filt in r_filters:
                stats_module.add_filter(filter_type=filt['filter_type'], filter_data=filt['filter_data'])
        data = get_data()
        return render_template('Statistics/articles_data.html',data=data)
    else:
        stats_module.ranking_articles()
        stats_module.cancel_filter('law')
        stats_module.cancel_filter('date')
        codex_list = load_codex_list()
        data = get_data()
        try:
            return render_template('Statistics/index.html', 
                                    data=render_template('Statistics/articles_data.html',data=data), 
                                    codex_list=codex_list, 
                                    rank='by_cnt_questions')
        except TemplateNotFound:
            abort(404)


@statistics_page.route('/rank/', defaults={'rank_by': 'by_cnt_questions', 'filters': []})
@statistics_page.route('/rank/<rank_by>', methods=['GET'])
def rank(rank_by):
    stats_module.ranking_articles(rank_type=rank_by)
    data = get_data()
    codex_list = load_codex_list()
    try:
        return render_template('Statistics/index.html', data=data, codex_list=codex_list, rank=rank_by)
    except TemplateNotFound:
        abort(404)
