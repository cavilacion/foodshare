from datetime import datetime
import time
import pika
import json


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models.user import User
from models.offer import Offer 
from models.reservation import Reservation
from models.rating import Rating
from models.base import Base

from app import ecv

# setup database connection
# engine = create_engine('sqlite:///foodshare.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)



class Consumer:

	def __init__(self, synchronizer, queue_name):
		self.sync = synchronizer
		self.DBSession = ecv.session()

		# setup rabbitmq connection
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		self.channel = self.connection.channel()
		self.queue_name = queue_name
		self.channel.queue_declare(queue=self.queue_name)

	def add_user(self, username):
		# session=DBSession()
		# session.add()
		try:
			self.sync.create_obj(User(username=username))
			# session.commit()
			print (" > Added "+username+" to database")
			return "SUCCESS"
		except IntegrityError: # unique constraint must not be violated
			print (" > Username "+username+" already taken.")
			return "FALSE"

	def delete_user (self, user_id):
		session=self.DBSession()
		user = session.query(User).filter(User.id==user_id).first()
		if not user:
			return "User does not exist"
		self.sync.delete_obj(user)
		print (" > Deleted user ", user.username+"[{}]".format(user.id))
		return "SUCCESS"

	def add_offer(self, offer):
		host_id = offer["host_id"]
		portions = offer["portions"]
		price = offer["price"]
		info = offer["info"]
		time_ready = offer["time_ready"]
		time_ready = datetime.strptime(time_ready, '%Y-%m-%d %H:%M:%S.%f')
	
		session=self.DBSession
		user=session.query(User).filter(User.id==host_id).first()
		if not user:
			return "User does not exist"
		try:
			self.sync.create_obj(Offer(host=user, portions=portions, price=price, info=info, time_ready=time_ready))
			print (" > "+user.username+" offered a meal with "+str(portions)+" for EUR "
				+str(price)+" per portion. It will be ready at "+str(time_ready)+". \""+info+"\"")
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to add offer made by "+user.username)
			return "FAILURE"

	def update_offer(self, offer):
		offer_id = offer["offer_id"]
		session = self.DBSession()
		offer_new=session.query(Offer).filter(Offer.id==offer_id).first()
		if not offer_new:
			return "Offer does not exist"

		portions = offer["portions"]
		if portions is not None:
			offer_new.portions=portions
		price = offer["price"]
		if price is not None:
			offer_new.price=price
		info = offer["info"]
		if info is not None:
			offer_new.info = info
		time_ready = offer["time_created"]
		if time_ready is not None:
			offer_new.time_ready = time_ready

		try:
			self.sync.update_obj(offer_new)
			print (" > "+offer.host.username+" updated his offer "+offer.info)
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to update offer by user "+offer.host.username)
			return "FAILURE"

	def delete_offer(self, offer_id):
		session = self.DBSession()
		offer = session.query(Offer).filter(Offer.id == offer_id).first()
		if not offer:
			return "Offer does not exist"
		self.sync.delete_obj(offer)
		print (" > Deleted offer from "+ offer.host.username+" with id {}.".format(offer.id))
		return "SUCCESS"

	def add_reservation(self, reservation):
		user_id = reservation["user_id"]
		offer_id = reservation["offer_id"]
		portions = reservation["portions"]
		session = self.DBSession
		user=session.query(User).filter(User.id==user_id).first()
		offer=session.query(Offer).filter(Offer.id==offer_id).first()
		if not user:
			return "User does not exist"
		if not offer:
			return "Offer does not exist"
		try:
			self.sync.create_obj(Reservation(user=user, offer=offer, portions=portions))
			print (" > "+user.username+" reserved "+str(portions)+" portions from "
					+offer.host.username+"'s home made "+offer.info)
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to reserve for user "+user.username)
			return "FAILURE"

	def update_reservation(self, reservation):
		reservation_id = reservation["reservation_id"]
		portions = reservation["portions"]
		session=self.DBSession
		reservation_new = session.query(Reservation).filter(Reservation.id==reservation_id).first()
		if portions is not None:
			reservation_new.portions = portions
		try:
			self.sync.update_obj(reservation_new)
			print (" > "+reservation.user.username+" updated his reservation to "+reservation_new.portions+ " portions.")
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to update reservation by user "+reservation.host.username)
			return "FAILURE"

	def delete_reservation(self, reservation_id):
		session = self.DBSession
		reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
		if not reservation:
			return "Reservation does not exist"
		self.sync.delete_obj(reservation)
		print (" > Deleted reservation from "+ reservation.user.username+" with id {}.".format(reservation.id))
		return "SUCCESS"

	def add_rating(self, rating):
		user_id = rating["user_id"]
		host_id = rating["host_id"]
		stars = rating["stars"]
		comment = rating["comment"]
		session=self.DBSession
		user=session.query(User).filter(User.id==user_id).first()
		host=session.query(User).filter(User.id==host_id).first()
		if not user:
			return "User does not exist"
		if not host:
			return "Host does not exist"
		try:
			self.sync.update_obj(Rating(user=user, host=host, stars=stars, comment=comment))
			print (" > "+user.username+" rated "+host.username+" with "+str(stars)+" stars: "+comment)
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to add rating made by "+user.username)
			return "FAILURE"

	def update_rating(self, rating):
		rating_id = rating["rating_id"]
		stars = rating["stars"]
		comment = rating["comment"]
		session = self.DBSession()
		rating_new = session.query(Reservation).filter(Reservation.id == rating_id).first()
		if not rating_new:
			return "Rating does not exist"
		if stars is not None:
			rating_new.stars = stars
		if comment is not None:
			rating_new.comment = comment

		try:
			self.sync.update_obj(rating_new)
			print (" > " + rating.user.username + " updated his rating for " + rating.host.username + " to {} stars.".format(rating_new.stars) )
			return "SUCCESS"
		except IntegrityError:
			print (" > Failed to update rating by user " + rating.user.username)
			return "FAILURE"

	def delete_rating(self, rating_id):
		session = self.DBSession()
		rating = session.query(Rating).filter(Rating.id == rating_id).first()
		if not rating:
			return "Rating does not exist"
		self.sync.delete_obj(rating)
		print (" > Deleted rating from "+rating.user.username+" with id {}.".format(rating.id))
		return "SUCCESS"

	def message_handle(self, ch, method, props, body):
		msg = json.loads(body)  # body is in json format
		action = msg["action"]
		if action == "adduser":
			result = self.add_user(msg["username"])
		elif action == "addoffer":
			result = self.add_offer(msg)
		elif action == "updateoffer":
			result = self.update_offer(msg)
		elif action == "deleteoffer":
			result = self.delete_offer(msg)
		elif action == "addreserve":
			result = self.add_reservation(msg)
		elif action == "updatereserve":
			result = self.update_reservation(msg)
		elif action == "deletereserve":
			result = self.delete_reservation(msg)
		elif action == "addrating":
			result = self.add_rating(msg)
		elif action == "updaterating":
			result = self.update_rating(msg)
		elif action == "deleterating":
			result = self.delete_rating(msg)
		else:
			result = "FAILURE"
		ch.basic_publish(exchange='', routing_key=props.reply_to,
			properties=pika.BasicProperties(correlation_id = props.correlation_id),
			body=result)
    
	def start(self):

		self.channel.basic_qos(prefetch_count=1)
		self.channel.basic_consume (self.message_handle, queue=self.queue_name, no_ack=True)

		print (" > Message queue consumer waiting for messages...")
		self.channel.start_consuming()





