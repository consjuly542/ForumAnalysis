# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)
app.debug = False

# Configurations
# app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fun')
def fun():
    return render_template('fun.html')

from app.module.StatisticsWeb import statistics_page
app.register_blueprint(statistics_page, url_prefix='/statistics')

# cd app
# set PYTHONPATH=..
# "C:\ProgramData\Anaconda3\python.exe" __init__.py
app.run(host="0.0.0.0", port="3030")
