import os.path as path
import json
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from source.LinkSearcherModule import LinkSearcherModule

link_searcher_page = Blueprint('link_searcher_page', __name__,
                        template_folder='templates')

@link_searcher_page.route('/')
def get_view():
    try:
        return render_template('LinkSearcher/index.html')
    except TemplateNotFound:
        abort(404)

@link_searcher_page.route('/run', methods=['POST'])
def run():
    module = LinkSearcherModule(
        'LinkSearcher',
        'C:\\Users\\NRS-GromovSI\\Documents\\ForumAnalysisWeb\\data\\pro',
        'C:\\Users\\NRS-GromovSI\\Documents\\ForumAnalysisWeb\\data\\res\\LinkSearcher')
    module.run('test.txt', 'test-links.txt')
    data = None
    with open(path.join(module.dir_target, 'test-links.txt'), 'r') as f_in:
        data = json.load(f_in)
    return render_template('LinkSearcher/LinkSearcher_result.html', data=data)