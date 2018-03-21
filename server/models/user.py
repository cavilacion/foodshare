
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base

from models.offer import Offer
# from models.classes import Reservation

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(64), nullable=False, unique=True)
	
	# user has many offerings, many reservations, many ratings, and many "rateds"
	offerings = relationship("Offer", backref="host")
	reservations = relationship("Reservation", backref="user")
	ratings = relationship("Rating", backref="user", foreign_keys="Rating.user_id")
	rateds = relationship("Rating", backref="host", foreign_keys="Rating.host_id")

	def to_dict(self):
	    return dict(
			id = self.id,
			username = self.username
		)