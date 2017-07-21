from definitions import ROOT_DIR
import sys
import os.path
sys.path.append(os.path.join(ROOT_DIR, 'source/'))

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

articles_page = Blueprint('articles_page', __name__,
                          template_folder='templates')

def get_articles_list():
    data = []
    for root, _, files in os.walk(os.path.join(ROOT_DIR, 'app/static/articles')):
        for f in files:
            name = f.split('.')[0]
            ext = f.split('.')[1]
            data.append({
                'name': name,
                'extension': ext
            })
    return data

@articles_page.route('/')
def get_view():
    data = get_articles_list()
    try:
        return render_template('Articles/index.html',data=data)
    except TemplateNotFound:
        abort(404)
