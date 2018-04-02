import datetime

from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Float
from models.base import Base

from models.user import User

class Rating(Base):
	__tablename__ = 'rating'

	id = Column(Integer, primary_key=True)

	# foreign key of the user that rates
	user_id = Column(Integer, ForeignKey(User.id))
	
	# foreign key of the host being rated
	host_id = Column(Integer, ForeignKey(User.id))
	
	# rating information
	stars = Column(Integer, nullable=False)
	comment = Column(String(1024), nullable=False)
	
	def to_dict(self):
	    return dict(
			id = self.id,
			user_id = self.user_id,
			host_id = self.host_id,
			stars = self.stars,
			comment = self.comment
		)