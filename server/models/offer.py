import datetime

from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base

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

	def to_dict(self):
	    return dict(
			id = self.id,
			host_id = self.host_id,
			portions = self.portions,
			price = self.price,
            info = self.info,
            time_ready = str(self.time_ready),
            time_created = str(self.time_created)
		)