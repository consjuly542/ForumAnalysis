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

# Home page route
@app.route('/')
def index():
    return render_template('home.html')

# Import StatisticsWeb blueprint
from app.module.StatisticsWeb import statistics_page
app.register_blueprint(statistics_page, url_prefix='/statistics')

# Import ArticlesWeb blueprint
from app.module.ArticlesWeb import articles_page
app.register_blueprint(articles_page, url_prefix='/articles')

app.run(debug=True, host='0.0.0.0', port=8097)