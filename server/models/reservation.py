import datetime
from sqlalchemy import DateTime, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.base import Base

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

	def to_dict(self):
	    return dict(
			id = self.id,
			offer_id = self.offer_id,
			user_id = self.user_id,
			portions = self.portions,
			timestamp = str(self.timestamp)
		)