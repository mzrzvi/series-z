#!/usr/bin/env python3

# -------
# imports
# -------

from unittest import main, TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///seriesz.db')
Session = sessionmaker(bind=engine)
s = Session()

class TestIdb(TestCase):
    # -------------
    # Founder queries
    # -------------

    def test_founder_add_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)


        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        s.add(mark)
        s.commit()

        mark_test = s.query(Founder).filter(Founder.name == "Test Name")[0]
        self.assertEqual(mark, mark_test)

        s.delete(mark)
        s.delete(menlo)
        s.commit()

    def test_founder_query_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        name = 'Tyler Winklevoss'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        tyler = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        s.add(mark)
        s.add(tyler)
        s.commit()

        tyler_test = s.query(Founder).filter(Founder.name == "Tyler Winklevoss")[0]

        self.assertEqual(tyler, tyler_test)

        s.delete(mark)
        s.delete(tyler)
        s.delete(menlo)
        s.commit()

    def test_founder_delete_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        s.add(mark)
        s.commit()
        s.delete(mark)
        s.delete(menlo)
        s.commit()

        count = s.query(Founder).filter(Founder.name == "Test Name").count()

        self.assertEquals(0, count)

    # ---------------
    # Founder __init__
    # ---------------

    def test_founder_init_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        self.assertEqual(name, mark.name)
        self.assertEqual(angel_id, mark.angel_id)
        self.assertEqual(popularity, mark.popularity)
        self.assertEqual(image_url, mark.image_url)
        self.assertEqual(bio, mark.bio)
        self.assertEqual(rank, mark.rank)
        self.assertEqual(num_startups, mark.num_startups)
        self.assertEqual(city_name, mark.city_name)

    def test_founder_init_2(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = ''
        angel_id = 0
        popularity = 0
        image_url = ''
        bio = ''
        rank = 0
        num_startups = 0
        city_name = ''
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        self.assertEqual(name, mark.name)
        self.assertEqual(angel_id, mark.angel_id)
        self.assertEqual(popularity, mark.popularity)
        self.assertEqual(image_url, mark.image_url)
        self.assertEqual(bio, mark.bio)
        self.assertEqual(rank, mark.rank)
        self.assertEqual(num_startups, mark.num_startups)
        self.assertEqual(city_name, mark.city_name)

    def test_founder_init_3(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = None
        angel_id = None
        popularity = None
        image_url = None
        bio = None
        rank = None
        num_startups = None
        city_name = None
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        self.assertEqual(name, mark.name)
        self.assertEqual(angel_id, mark.angel_id)
        self.assertEqual(popularity, mark.popularity)
        self.assertEqual(image_url, mark.image_url)
        self.assertEqual(bio, mark.bio)
        self.assertEqual(rank, mark.rank)
        self.assertEqual(num_startups, mark.num_startups)
        self.assertEqual(city_name, mark.city_name)

    def test_founder_city(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)


        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        s.add(mark)
        s.commit()

        self.assertEquals(menlo, mark.city)

        s.delete(menlo)
        s.delete(mark)
        s.commit()

    def test_founder_startup(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        city = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, city, popularity, market, num_founders, product_desc, company_url, logo_url, city=menlo)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        mark.startups.append(facebook)

        s.add(mark)
        s.commit()

        self.assertEquals(facebook, mark.startups[0])

        s.delete(menlo)
        s.delete(facebook)
        s.delete(mark)
        s.commit()


    # --------------
    # Startup tables
    # --------------

    def test_startup_add_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)


        name = 'Test Startup'
        location = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, location, popularity, market , num_founders, product_desc, company_url , logo_url, city = menlo)

        s.add(facebook)
        s.commit()

        fb_test = s.query(Startup).filter(Startup.name == 'Test Startup')[0]

        self.assertEqual(fb_test.name, facebook.name)
        self.assertEqual(fb_test.location, facebook.location)
        self.assertEqual(fb_test.popularity, facebook.popularity)
        self.assertEqual(fb_test.market, facebook.market)
        self.assertEqual(fb_test.num_founders, facebook.num_founders)
        self.assertEqual(fb_test.product_desc, facebook.product_desc)
        self.assertEqual(fb_test.company_url, facebook.company_url)
        self.assertEqual(fb_test.logo_url, facebook.logo_url)

        s.delete(menlo)
        s.delete(facebook)
        s.commit()

    def test_startup_query_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)


        name = 'Test Startup'
        location = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, location, popularity, market , num_founders, product_desc, company_url , logo_url, city = menlo)

        s.add(facebook)
        s.commit()

        fb_test = s.query(Startup).filter(Startup.name == 'Test Startup')[0]

        self.assertEqual(facebook, fb_test)

        s.delete(menlo)
        s.delete(facebook)
        s.commit()

    def test_startup_delete_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        city = 'Test City'
        popularity = 123
        market = 'Social Netowrk'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, city, popularity, market , num_founders, product_desc, company_url , logo_url, city=menlo)

        s.add(facebook)
        s.commit()

        s.delete(facebook)
        s.delete(menlo)
        s.commit()

        count = s.query(Startup).filter(Startup.name == "Facebook").count()

        self.assertEquals(0, count)

    # ----------------
    # Startup __init__
    # ----------------

    def test_startup_init_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        location = 'Test City'
        popularity = 123
        market = 'Social Netowrk'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, location, popularity, market , num_founders, product_desc, company_url , logo_url, city= menlo)

        self.assertEqual(name, facebook.name)
        self.assertEqual(location, facebook.location)
        self.assertEqual(popularity, facebook.popularity)
        self.assertEqual(market, facebook.market)
        self.assertEqual(num_founders, facebook.num_founders)
        self.assertEqual(product_desc, facebook.product_desc)
        self.assertEqual(company_url, facebook.company_url)
        self.assertEqual(logo_url, facebook.logo_url)

    def test_startup_init_2(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = ''
        location = ''
        popularity = 0
        market = ''
        num_founders = 0
        product_desc = ''
        company_url = ''
        logo_url = ''
        facebook = Startup(name, location, popularity, market , num_founders, product_desc, company_url , logo_url, city=menlo)

        self.assertEqual(name, facebook.name)
        self.assertEqual(location, facebook.location)
        self.assertEqual(popularity, facebook.popularity)
        self.assertEqual(market, facebook.market)
        self.assertEqual(num_founders, facebook.num_founders)
        self.assertEqual(product_desc, facebook.product_desc)
        self.assertEqual(company_url, facebook.company_url)
        self.assertEqual(logo_url, facebook.logo_url)

    def test_startup_init_3(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = None
        location = None
        popularity = None
        market = None
        num_founders = None
        product_desc = None
        company_url = None
        logo_url = None
        facebook = Startup(name, location, popularity, market , num_founders, product_desc, company_url , logo_url, city=menlo)

        self.assertEqual(name, facebook.name)
        self.assertEqual(location, facebook.location)
        self.assertEqual(popularity, facebook.popularity)
        self.assertEqual(market, facebook.market)
        self.assertEqual(num_founders, facebook.num_founders)
        self.assertEqual(product_desc, facebook.product_desc)
        self.assertEqual(company_url, facebook.company_url)
        self.assertEqual(logo_url, facebook.logo_url)

    def test_startup_city(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        city = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, city, popularity, market, num_founders, product_desc, company_url, logo_url, city=menlo)

        s.add(facebook)
        s.commit()

        self.assertEquals(menlo, facebook.city)

        s.delete(menlo)
        s.delete(facebook)
        s.commit()


    def test_startup_founder(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        city = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, city, popularity, market, num_founders, product_desc, company_url, logo_url, city=menlo)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        facebook.founders.append(mark)

        s.add(mark)
        s.commit()

        self.assertEquals(mark, facebook.founders[0])

        s.delete(menlo)
        s.delete(facebook)
        s.delete(mark)
        s.commit()


    # ---------------
    # city tables
    # ---------------

    def test_city_add_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        s.add(menlo)
        s.commit()

        menlo_test = s.query(City).filter(City.name == "Test City")[0]

        self.assertEqual(menlo_test.name, menlo.name)
        self.assertEqual(menlo_test.investor_followers, menlo.investor_followers)
        self.assertEqual(menlo_test.popularity, menlo.popularity)
        self.assertEqual(menlo_test.num_companies, menlo.num_companies)
        self.assertEqual(menlo_test.num_people, menlo.num_people)


        s.delete(menlo)
        s.commit()

    def test_city_query_1(self):


        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'MP'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        mp = City(name, investor_followers, popularity, num_companies, num_people)

        s.add(menlo)
        s.add(mp)
        s.commit

        mp_test = s.query(City).filter(City.name == "MP")[0]

        self.assertEqual(mp, mp_test)

        s.delete(mp)
        s.delete(menlo)
        s.commit()

    def test_city_delete_1(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        s.add(menlo)
        s.commit()
        s.delete(menlo)
        s.commit()

        count = s.query(City).filter(City.name == "Test City").count()

        self.assertEquals(0, count)
    # -----------------
    # Startup __init__
    # -----------------

    def test_city_init_1(self):
        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        self.assertEqual(name, menlo.name)
        self.assertEqual(investor_followers, menlo.investor_followers)
        self.assertEqual(popularity, menlo.popularity)
        self.assertEqual(num_companies, menlo.num_companies)
        self.assertEqual(num_people, menlo.num_people)

    def test_city_init_2(self):
        name = ""
        investor_followers = 0
        popularity = 0
        num_companies = 0
        num_people = 0
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        self.assertEqual(name, menlo.name)
        self.assertEqual(investor_followers, menlo.investor_followers)
        self.assertEqual(popularity, menlo.popularity)
        self.assertEqual(num_companies, menlo.num_companies)
        self.assertEqual(num_people, menlo.num_people)

    def test_city_init_3(self):
        name = None
        investor_followers = None
        popularity = None
        num_companies = None
        num_people = None
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        self.assertEqual(name, menlo.name)
        self.assertEqual(investor_followers, menlo.investor_followers)
        self.assertEqual(popularity, menlo.popularity)
        self.assertEqual(num_companies, menlo.num_companies)
        self.assertEqual(num_people, menlo.num_people)


    def test_city_startup(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Startup'
        city = 'Test City'
        popularity = 123
        market = 'Social Network'
        num_founders = 4
        product_desc = 'A social network.'
        company_url = 'http://www.facebook.com'
        logo_url = 'http://www.facebook.com/logo'
        facebook = Startup(name, city, popularity, market, num_founders, product_desc, company_url, logo_url, city=menlo)

        s.add(facebook)
        s.commit()

        self.assertEquals(menlo.startups[0], facebook)

        s.delete(menlo)
        s.delete(facebook)
        s.commit()


    def test_city_founder(self):

        name = 'Test City'
        investor_followers = 123
        popularity = 123
        num_companies = 123
        num_people = 123
        menlo = City(name, investor_followers, popularity, num_companies, num_people)

        name = 'Test Name'
        angel_id = 123
        popularity = 123
        image_url = 'http://markzuckerburg.com/photo'
        bio = 'A dropout'
        rank = 1
        num_startups = 1
        city_name = 'Test City'
        mark = Founder(name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city=menlo)

        s.add(mark)
        s.commit()

        self.assertEquals(mark, menlo.founders[0])

        s.delete(menlo)
        s.delete(mark)
        s.commit()



# ----
# main
# ----

if __name__ == "__main__":
    main()
