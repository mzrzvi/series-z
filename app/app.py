import os, sys
import json
import tests
import time, random
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for, redirect, send_file, make_response, abort

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

from sqlalchemy.sql import exists

from models import *

URI = 'postgresql://postgres:postgres@146.20.68.107/postgres'

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
    run_time = round(random.random(),3)
    time.sleep(run_time + 0.5)
    return render_template('test.html', run_time=run_time)


################ Danyal start ################

@app.route('/api/startups', methods=['GET'])
def api_startups():

    startups = db_session.query(City).all()
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

def get_server() :
    return app

if __name__ == '__main__':
    runserver()
