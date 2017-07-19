import os.path as path
import json
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import os.path
from definitions import ROOT_DIR

statistics_page = Blueprint('statistics_page', __name__,
                        template_folder='templates')

@statistics_page.route('/')
def get_view():
    data = None
    with open(os.path.join(ROOT_DIR, 'data/res/laws.json')) as f_in:
        data = json.load(f_in)
    data = data[:20]
    for idx, item in enumerate(data):
        data[idx]['date'] = '.'.join(reversed(item['date'].split('.')))
        data[idx]['law'] = ''.join([i[0].upper() for i in item['law'].split()])
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