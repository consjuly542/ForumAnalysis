from definitions import ROOT_DIR
import sys
import os.path
sys.path.append(os.path.join(ROOT_DIR, 'source/'))

from source.ArticleStatistics import ArticleStatistics

import re
import _pickle as pickle
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

statistics_page = Blueprint('statistics_page', __name__,
                            template_folder='templates')

@statistics_page.route('/')
def get_view():
    data = None
    with open(os.path.join(ROOT_DIR, 'data/statistics/current_article_list'), 'rb') as f_in:
        data = pickle.load(f_in)
    try:
        return render_template('Statistics/index.html', data=data)
    except TemplateNotFound:
        abort(404)

# @statistics_page.route('/run', methods=['POST'])
# def run():
