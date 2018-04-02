import os
import sys
import datetime
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from classes import Base, User, Offer, Reservation, Rating

# create engine that stores data in the database file
engine = create_engine('sqlite:///foodshare.db')

# create all tables in the engine, executing SQL queries CREATE_TABLE
Base.metadata.create_all(engine)

	
	
