#!/usr/bin/env python3
import time, os, json, logging, sys
from angel import AngelList
from models import *

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import scoped_session, sessionmaker



#-----
#Setup
#-----

URI = 'postgresql://postgres:postgres@146.20.68.107/postgres'

num_missed_startups = 0
num_missed_founders = 0
num_missed_cities = 0
num_missed_city_data = 0

def get_db_session() :
    engine = create_engine(URI, echo=True)
    logging.info("DB engine created")

    Session = sessionmaker(bind=engine)
    s = Session()
    logging.info("DB session created")

    return s


def get_angel_list() :
    """
    Returns AngelList API object
    """
    try :
        ACCESS_TOKEN = '7b2f970c65843c003f29faab3cd089d9a2fe65fb738a1f69'
        CLIENT_ID = 'f4bc189150f55e3a4e04d7dd47d6f60d5d0101b7c16c9719'
        CLIENT_SECRET = '45e8cf40afa601846ea9af9dcf4d101aef2d183514690433'
    except KeyError as e :
        raise Exception("Missing environment variable: " + str(e[0]))

    return AngelList(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN)

def test_angel_list(al) :
    """
    Returns true if connected
    """
    if al.get_self() is not None :
        logging.info("Connected to API")
    else :
        logging.info("Could not connect to API")

    return al.get_self() is not None

def configure_logging() :
    """
    Configures logging for script
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        filename='database_entry.log',
                        filemode='w',
                        stream=sys.stdout)


def filter_hidden(data) :
    return list(filter(lambda d : not d['hidden'], data))

def get_city_data(city_id) :
    """
    Returns all city data
    """

    def clean_data(data) :
        keys = {'name', 'display_name', 'statistics'}
        missing_keys = keys - set(data.keys())

        if missing_keys :
            return

        city_stats = data['statistics']['all']

        city_data = {
                    'name': data['display_name'] if data['display_name'] else data['name'],
                    # 'angel_id': data['id'],
                    'popularity': city_stats['followers'] if city_stats['followers'] else 0,
                    'investor_followers': city_stats['investor_followers'] if city_stats['investor_followers'] else 0,
                    'num_companies': city_stats['startups'] if city_stats['startups'] else 0,
                    'num_people': city_stats['users'] if city_stats['users'] else 0
                    }

        return city_data

    response = None
    retries = 3
    while retries and not response :
        try :
            response = al.get_tags(city_id)
            logging.info("Received response for city data of: " + str(city_id))
        except :
            logging.debug("City data response error from city: " + str(city_id))
            retries -= 1
            time.sleep(2)


    if not response or response['tag_type'] != 'LocationTag' :
        logging.debug("tag_id is not for a location: " + city_id)
        num_missed_city_data += 1
        return

    return clean_data(response)



def get_companies_by_city(city_id, page) :
    """
    Returns full list of company objects
    """

    def clean_data(data) :
        keys = {'name', 'logo_url', 'markets', 'locations', 'follower_count', 'product_desc'}
        missing_keys = keys - set(data.keys())

        if missing_keys :
            return

        company_data = {
                        'name': data['name'],
                        'angel_id': data['id'],
                        'logo_url': data['logo_url'] if data['logo_url']  else '',
                        'popularity': data['follower_count'] if data['follower_count'] else 0,
                        'product_desc': data['product_desc'] if data['product_desc'] else '',
                        'company_url': data['company_url'] if data['company_url'] else '',
                        'market': data['markets'][0]['name'] if data['markets'] else '',
                        'location': data['locations'][0]['name'] if data['locations'] else '',
                        'num_founders': 1
                        }

        return company_data

    response = None
    retries = 3
    while retries and not response :
        try :
            response = al.get_tags_startups(city_id, page)
            logging.info("Recieved response for startups in: " + str(city_id))
        except :
            logging.debug("Company response error from city: " + str(city_id))
            retries -= 1
            time.sleep(2)


    if not response or 'startups' not in response :
        logging.debug("No startups in city with tag_id: " + city_id)
        num_missed_cities += 1
        return

    companies_data = filter_hidden(response['startups'])

    return [clean_data(company) for company in companies_data]


def get_founders_by_company(company_id) :
    """
    Returns full list of founder objects
    """
    def clean_data(data) :
        keys = {'name', 'id', 'bio', 'follower_count', 'image'}
        missing_keys = keys - set(data.keys())

        if missing_keys :
            return

        founder_data = {
                        'name': data['name'],
                        'angel_id': data['id'],
                        'bio': data['bio'] if data['bio'] else '',
                        'popularity': data['follower_count'] if data['follower_count'] else 0,
                        'image_url': data['image'] if data['image'] else '',
                        'rank': 0,
                        'num_startups': 1
                        }

        return founder_data

    response = None
    retries = 3
    while retries and not response :
        try :
            response = al.get_startup_roles(startup_id=company_id, role='founder')
            logging.info("Recieved response for founders of: " + str(company_id))
        except :
            logging.debug("Startup roles response error from company: " + str(company_id))
            retries -= 1
            time.sleep(2)



    if not response or 'startup_roles' not in response :
        logging.debug("No founders found for: " + company_id)
        num_missed_founders += 1
        return

    founders_data = (f['tagged'] for f in response['startup_roles'])

    return filter(lambda f: f, [clean_data(founder) for founder in founders_data])



al = get_angel_list()

session = get_db_session()

if __name__ == "__main__" :
    configure_logging()
    test_angel_list(al)

    city_ids = [1692, 1664, 1617, 1620, 1621, 1621, 1653, 1694]

    all_companies = []
    all_founders = []
    all_cities = []

    for city_id in city_ids :

        city_data = get_city_data(city_id)

        if not session.query(exists().where(City.name == city_data['name'])).scalar() :

            city = City(**city_data)
            city_companies = get_companies_by_city(city_id, 1)
            # for i in range(1, 4) :
            #     city_companies += get_companies_by_city(city_id,i)

            for c in city_companies :

                try :
                    if not session.query(exists().where(Startup.name == c['name'])).scalar() :

                        company_founders = get_founders_by_company(c['angel_id'])
                        c['num_founders'] = len(company_founders)

                        company = Startup(c['name'], c['location'], c['popularity'],
                                          c['market'], c['num_founders'], c['product_desc'],
                                          c['company_url'], c['logo_url'], city = city)

                        for f in company_founders :

                            try :
                                if not session.query(exists().where(Founder.name == f['name'])).scalar() :

                                    founder = Founder(f['name'], f['angel_id'], f['popularity'],
                                                      f['image_url'], f['bio'], f['rank'], f['num_startups'],
                                                      city_name=city.name, city=city)


                                    city.founders.append(founder)
                                    founder.startups.append(company)

                                    session.add(founder)
                                    # logging.info("Added founder: " + str(founder.name))
                            except :
                                logging.debug("Founder insert failed: " + f['name'])

                        city.startups.append(company)


                        session.add(company)
                        # logging.info("Added company: " + str(company.name))

                except :
                    logging.debug("Startup insert failed: " + c['name'])


            session.add(city)
            # logging.info("Added city: " + str(city.name))

    i = 1
    for founder in session.query(Founder).order_by(Founder.popularity.desc()).all() :
        founder.rank = i
        founder.num_startups = len(founder.startups)
        i += 1

    session.commit()






