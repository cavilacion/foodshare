import os
import sys
import datetime
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(64), nullable=False, unique=True)
	
	# user has many offerings, many reservations, many ratings, and many "rateds"
	offerings = relationship("Offer", backref="host")
	reservations = relationship("Reservation", backref="user")
	ratings = relationship("Rating", backref="user", foreign_keys="Rating.user_id")
	rateds = relationship("Rating", backref="host", foreign_keys="Rating.host_id")
	
class Offer(Base):
	__tablename__ = 'offer'
	
	# primary key
	id = Column(Integer, primary_key=True)
	
	# foreign key of persion making the offer, the host
	host_id = Column(Integer, ForeignKey('user.id'))
	
	# info about the offering
	portions = Column(Integer, nullable=False)
	price = Column(Float, nullable=False) # price is per portion
	info = Column(String(1024), nullable=False)
	time_ready = Column(DateTime, nullable=False)
	time_created = Column(DateTime, default=datetime.datetime.utcnow)
	
	# many reservations made for this offering 
	reservations = relationship("Reservation", backref="offer")


class Reservation(Base):
	__tablename__ = 'reservation'
	
	# primary key
	id = Column(Integer, primary_key=True)
	
	# foreign key for person making the reservation
	user_id = Column(Integer, ForeignKey('user.id'))
	
	# foreign key for the offer that is reserved
	offer_id = Column(Integer, ForeignKey('offer.id'))
	
	# info about the reservation
	portions = Column(Integer, nullable=False)
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Rating(Base):
	__tablename__ = 'rating'
	# foreign key of the user that rates
	user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
	
	# foreign key of the host being rated
	host_id = Column(Integer, ForeignKey(User.id), primary_key=True)
	
	# rating information
	stars = Column(Integer, nullable=False)
	comment = Column(String(1024), nullable=False)
	 


# create engine that stores data in the database file
engine = create_engine('sqlite:///foodshare.db')

# create all tables in the engine, executing SQL queries CREATE_TABLE
Base.metadata.create_all(engine)

	
	
