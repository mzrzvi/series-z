import os, sys
import json
import tests
import subprocess
import requests
from highcharts import Highchart
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for, redirect, send_file, make_response, abort
from bs4 import BeautifulSoup

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

from sqlalchemy.sql import exists

from models import *

BASE_URL = "series-z/"

URI = 'sqlite:///%s/series-z.db' % BASE_URL

app = Flask(__name__)

app.config.update(PROPAGATE_EXCEPTIONS = True)

app.url_map.strict_slashes = False

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(URI)
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def basic_pages(**kwargs):
    return render_template('index-b.html')

@app.route('/about')
def show_about():
    return render_template("about.html")

@app.route('/<model_name>/')
def show_model_page(model_name):
    if model_name == 'cities' :
        data = db_session.query(City).all()
        return render_template("city_listing.html", cities=data)

    if model_name == 'founders' :
        data = db_session.query(Founder).all()
        return render_template("founder_listing.html", founders=data)

    if model_name == 'startups' :
        data = db_session.query(Startup).all()
        return render_template("startup_listing.html", startups=data)

    return render_template('404.html')


city_images = {"San Francisco" : "http://www.jetblue.com/img/vacations/destination/San-Francisco-960-x-420.jpg", "New York City" : "https://media-cdn.tripadvisor.com/media/photo-s/03/9b/2d/f2/new-york-city.jpg", "Austin" : "http://intelligenttravel.nationalgeographic.com/files/2015/11/dowtown-austin-skyline-590-590x393.jpg", "Boston" : "https://media-cdn.tripadvisor.com/media/photo-s/03/9b/2f/47/boston.jpg", "Boulder" : "https://res-3.cloudinary.com/simpleview/image/upload/c_fill,f_auto,h_360,q_50,w_1024/v1/clients/boulder/AerialwithBoulderHighField_013f6e79-aa0f-42df-8adf-cf81bf59a2f2.jpg", "Los Angeles" : "http://usa.sae.edu/assets/Campuses/Los-Angeles/2015/Los_Angeles_city_view.jpg", "Palo Alto" : "https://cbsboston.files.wordpress.com/2011/07/stanford-university-palo-alto-california.jpg"}

@app.route('/<model_name>/<item_id>')
def show_item_page(model_name, item_id):
    if model_name == 'cities' :
        try :
            item = db_session.query(City).get(item_id)
            return render_template('city.html', city=item, images=city_images)
        except :
            return render_template('404.html')

    if model_name == 'founders' :
        try :
            founder = db_session.query(Founder).get(item_id)
            return render_template('founder.html', founder=founder)
        except :
            return render_template('404.html')

    if model_name == 'startups' :
        try :
            item = db_session.query(Startup).get(item_id)
            return render_template('startup.html', startup=item)
        except :
            return render_template('404.html')

    return render_template('404.html')

@app.route('/search', methods=['POST'])
def search(**kwargs):
    token = request.form['text']
    tokens = token.split(" ")

    if not tokens :
        return render_template('search.html', results=[])


    res = [set(founder_search(t) + startup_search(t) + city_search(t)) for t in tokens]
    orSet = set.union(*res)
    andSet = set.intersection(*res)

    and_dict = {'startups': [], 'founders': [], 'cities': []}
    for element in andSet :
        if type(element) == Startup :
            and_dict['startups'] += [element]
        if type(element) == Founder :
            and_dict['founders'] += [element]
        if type(element) == City :
            and_dict['cities'] += [element]

    or_dict = {'startups': [], 'founders': [], 'cities': []}
    for element in orSet :
        if type(element) == Startup :
            or_dict['startups'] += [element]
        if type(element) == Founder :
            or_dict['founders'] += [element]
        if type(element) == City :
            or_dict['cities'] += [element]

    return render_template('search.html', and_results=and_dict, or_results=or_dict, text=token)


def founder_search (terms):
    queryOutput = db_session.query(Founder).filter(Founder.name.like("%"+ terms +"%") |
                                                   Founder.city_name.like("%"+ terms + "%") |
                                                   Founder.startups.any(Startup.name == terms.capitalize())).all()
    return queryOutput


def startup_search (terms):
    queryOutput = db_session.query(Startup).filter(Startup.name.like("%"+ terms + "%") | 
                                                   Startup.location.like("%"+ terms + "%") |
                                                   Startup.founders.any(Founder.name == terms.capitalize())).all()
    return queryOutput


def city_search (terms):
    queryOutput = db_session.query(City).filter(City.name.like("%" + terms + "%") |
                                                City.founders.any(Founder.name == terms.capitalize()) |
                                                City.startups.any(Startup.name == terms.capitalize())).all()
    return queryOutput


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/run_tests')
def run_tests ():
    token = '----------------------------------------------------------------------' 
    command = "python %s/tests.py" % BASE_URL
    r = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
    res = r[r.find(token):]
    return render_template('test.html', test_results=res)

options = {
    'chart': {
        'borderWidth': 1,
        'marginRight': 50 
    },

    'title': {
        'text': 'Cat Weight Min vs. Max'
    },

    'yAxis' : {
        'title' : {
            'enabled': True,
            'text': 'Max Weights (lbs)'
        }
    },

    'xAxis' : {
        'title' : {
            'enabled': True,
            'text': 'Min Weights (lbs)'
        }
    },
    'tooltip': {
        'headerFormat': '<b>Weights</b><br/>',
        'pointFormat': 'Min: {point.x} lbs<br/>Max: {point.y} lbs'
    }

} 

@app.route('/cats')
def cat_page():
    # return render_template('cat_page.html')

    url = 'http://catsgalore.me/api/breeds/'
    r = requests.get(url)
    breeds = r.json()['breeds']
    data = [br['weight'] for br in breeds]
    weights = [map(float, tuple(b[1:b.find(')')].split(' to '))) for b in data]
    chart = Highchart()
    chart.add_data_set(weights, 'scatter', 'Cat Weights')
    chart.set_dict_options(options)

    w = BeautifulSoup(open(BASE_URL + "templates/cat_page.html"))
    c = BeautifulSoup(str(chart.htmlcontent))

    scripts = c.find_all(lambda tag: (tag.has_attr('src') and tag.name == 'script') or tag.name == 'link') 
    chart_script = c.find_all(lambda tag: not tag.has_attr('type') and tag.name == 'script')[0]
    loading = c.div

    head = w.head

    div = w.find_all('div', class_='table-wrapper')[0]
        
    div.insert(0, loading)
    div.insert(1, chart_script)

    for s in scripts : 
        head.append(s)

    html = w.prettify("utf-8")
    with open(BASE_URL + "templates/cats.html", "wb") as f:
        f.write(html)


    return render_template("cats.html")



################ Danyal start ################

@app.route('/api/startups', methods=['GET'])
def api_startups():

    startups = db_session.query(Startup).all()
    data = []

    for startup in startups:
        data.append(row_dict(startup))

    data = json.dumps(data)

    return data

@app.route('/api/startup/<int:id>', methods=['GET'])
def api_startup(id):
    startup = db_session.query(Startup).get(id)

    if startup:
        startup = row_dict(startup)
        data = json.dumps(startup, ensure_ascii=False)
    else:
        data = ''

    return data

@app.route('/api/founders', methods=['GET'])
def api_founders():

    founders = db_session.query(Founder).all()
    data = []
    for founder in founders:
        data.append(row_dict(founder))

    data = json.dumps(data)

    return data


@app.route('/api/founder/<int:id>', methods=['GET'])
def api_founder(id):
    founder = db_session.query(Founder).get(id)

    if founder:
        founder = row_dict(founder)
        data = json.dumps(founder, ensure_ascii=False)
    else:
        data = ''

    return data

@app.route('/api/cities', methods=['GET'])
def api_cities():
    cities = db_session.query(City).all()
    data = []
    for city in cities:
        data.append(row_dict(city))

    data = json.dumps(data)

    return data


@app.route('/api/city/<int:id>', methods=['GET'])
def api_city(id):
    city = db_session.query(City).get(id)

    if city:
        city = row_dict(city)
        data = json.dumps(city, ensure_ascii=False)
    else:
        data = ''


    return data

def row_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


################ Danyal end   ################

def get_server():
    return app

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()