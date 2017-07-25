'''
statistics_page blueprint
'''

from definitions import ROOT_DIR
import sys
import os.path
sys.path.append(os.path.join(ROOT_DIR, 'source/'))

from source.StatisticsModule import StatisticsModule
from source.ArticleStatistics import get_questions

import _pickle as pickle
from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

# Define blueprint
statistics_page = Blueprint('statistics_page', __name__,
                            template_folder='templates')

stats_module = StatisticsModule()

# def get_data():
#     '''
#     Gets data from file with articles

#     Parameters
#     ------------
#         None

#     Returns
#     ------------
#     * data: Array of data objects (ArticleStatistics dicts)
#     '''
#     data = None
#     with open(os.path.join(ROOT_DIR, 'data/statistics/current_article_list'), 'rb') as f_in:
#         data = pickle.load(f_in)
#     return data


def load_codex_list():
    '''
    Loads codex list from file
    to show in select menu

    Parameters
    ------------
        None

    Returns
    ------------
    * codex_list (string[]): Array of codex

    '''
    codex_list = None
    with open(os.path.join(ROOT_DIR, 'data/res/codex_list'), 'rb') as f_in:
        codex_list = pickle.load(f_in)
    return codex_list


def load_art_questions(article_id):
    '''
    Loads question+answers data for
    a specific article

    Parameters
    ------------
    * article_id (string): article_ID (from Article class)

    Returns
    ------------
    * data (string[]): Array of question+answers objects

    '''
    data = get_questions(os.path.join(ROOT_DIR, 'data/statistics/article_questions/' + article_id))
    return data


@statistics_page.route('/', methods=['GET', 'POST'])
def get_view(save_options=False):
    # request data:
    # -> rank: (string)
    # -> ascending: (boolean)
    # -> filters: [{'filter_type': (string), 'filter_data': (string)}]
    if request.method == 'POST':
        req_data = request.get_json(force=True)
        r_rank = req_data['rank']
        r_ascending = req_data['ascending']
        r_filters = req_data['filters']
        # stats_module.ranking_articles(rank_type=(r_rank if r_rank else 'by_cnt_questions'), ascending=r_ascending)
        # # Cancel prev. filters
        # stats_module.cancel_filter('law')
        # stats_module.cancel_filter('date')
        # stats_module.cancel_filter('not_in_guide')

        # if r_filters:
        #     for filt in r_filters:
        #         # print (filt['filter_type'])
        #         stats_module.add_filter(filter_type=filt['filter_type'], filter_data=filt['filter_data'])

        data, cnt_articles = stats_module.apply_rank_and_filters(r_rank, r_ascending, r_filters)
        # data = get_data()
        print ("CNT_ARTICLES", cnt_articles)
        try:
            # returns rendered html template with data
            return render_template('Statistics/articles_data.html', data=data, \
                                    items=dict.items, len=len)

        except TemplateNotFound:
            abort(404)
    else:
        # if not save_options:
        #     stats_module.ranking_articles()
        #     stats_module.cancel_filter('law')
        #     stats_module.cancel_filter('date')
        #     stats_module.cancel_filter('not_in_guide')
        codex_list = load_codex_list()
        # data = get_data()
        data, cnt_articles = stats_module.apply_rank_and_filters()
        print ("CNT_ARTICLES", cnt_articles)
        try:
            # returns rendered html template with data
            return render_template('Statistics/index.html',
                                   data=render_template('Statistics/articles_data.html', data=data,
                                                        items=dict.items, len=len),
                                   codex_list=codex_list,
                                   rank='by_cnt_questions',
                                   ascending=False, 
                                   cnt_articles = cnt_articles)
        except TemplateNotFound:
            abort(404)


@statistics_page.route('/<article_id>/questions')
def art_questions(article_id):
    # Find article info by its article_ID
    # data = get_data()
    # global data
    # art_data = None
    # for item in stats_module.cur_articles_list:
    #     if item['official_article']['article_ID'] == article_id:
    #         art_data = item
    #         break
    art_data = stats_module.article_index[article_id]
    data = load_art_questions(article_id)
    try:
        # returns rendered html template with data
        return render_template('Statistics/article_questions.html', data=data, info=art_data)
    except TemplateNotFound:
        abort(404)