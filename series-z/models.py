#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from init_db import Base


#---------
#Relations
#---------

startup_to_founder = Table("startup_to_founder", Base.metadata,
    Column("startup_id", Integer, ForeignKey("startups.id"), primary_key=True),
    Column("founder_id", Integer, ForeignKey("founders.id"), primary_key=True)
)

#------
#Founder
#------

class Founder(Base):
    """
    Founder is a class representing an investor or a company founder
    """

    __tablename__ = 'founders'

    #Founder attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    angel_id = Column(Integer, nullable=False)
    popularity = Column(Integer)
    image_url = Column(String)
    bio = Column(String)
    rank = Column(Integer)
    num_startups = Column(Integer)
    city_name = Column(String)
    #Founder foreign keys
    city_id = Column(Integer, ForeignKey('cities.id'))

    #Founder relationships
    city = relationship("City", back_populates="founders")
    startups = relationship("Startup", secondary=startup_to_founder, back_populates="founders")

    def __init__(self, name, angel_id, popularity, image_url, bio, rank, num_startups, city_name, city):
        """
        Standard constructor for Founder
        """
        self.name = name
        self.angel_id = angel_id
        self.popularity = popularity
        self.image_url = image_url
        self.bio = bio
        self.rank = rank
        self.num_startups = num_startups
        self.city_name = city_name
        self.city = city
#-------
#Startup
#-------

class Startup(Base):
    """
    Startup is a class representing a startup
    """

    __tablename__ = 'startups'

    #Startup attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False)
    market = Column(String, nullable=False)
    num_founders = Column(Integer, nullable=False)
    product_desc = Column(String)
    company_url = Column(String)
    logo_url = Column(String)

    #Startup foreign keys
    city_id = Column(Integer, ForeignKey('cities.id'))

    #Startup relationships
    city = relationship("City", back_populates="startups")
    founders = relationship("Founder", secondary=startup_to_founder, back_populates="startups")

    def __init__(self, name, location, popularity, market, num_founders, product_desc, company_url, logo_url, city):
        """
        Standard constructor for Startup
        """
        self.name = name
        self.location = location
        self.popularity = popularity
        self.market = market
        self.num_founders = num_founders
        self.product_desc = product_desc
        self.company_url = company_url
        self.logo_url = logo_url
        self.city = city

#--------
#City
#--------

class City(Base):
    """
    City is a class representing a geographical region that hosts People and Companies
    """

    __tablename__ = 'cities'

    #City attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    investor_followers = Column(Integer, nullable=False)
    popularity = Column(Integer, nullable=False)
    num_companies = Column(Integer, nullable=False)
    num_people = Column(Integer, nullable=False)

    #City relationships
    startups = relationship("Startup", back_populates="city")
    founders = relationship("Founder", back_populates="city")

    def __init__(self, name, investor_followers, popularity, num_companies, num_people):
        """
        Standard constructor for City
        """
        self.name = name
        self.investor_followers = investor_followers
        self.popularity = popularity
        self.num_companies = num_companies
        self.num_people = num_people

