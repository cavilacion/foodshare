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

# setup database connection
engine = create_engine('sqlite:///foodshare.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# setup rabbitmq connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='foodshare')


def add_user(username):
	session=DBSession()
	session.add(User(username=username))
	try:
		session.commit()
		print (" > Added "+username+" to database")
		return "SUCCESS"
	except IntegrityError: # unique constraint must not be violated
		print (" > Username "+username+" already taken.")
		return "FALSE"

def add_offer(offer):
	host_id = offer["host_id"]
	portions = offer["portions"]
	price = offer["price"]
	info = offer["info"]
	time_ready = offer["time_ready"]
	time_ready = datetime.strptime(time_ready, '%Y-%m-%d %H:%M:%S.%f')
  
	session=DBSession()
	user=session.query(User).filter(User.id==host_id).first()
	if not user:
		return "User does not exist"
	o = Offer(host=user, portions=portions, price=price, info=info, time_ready=time_ready)
	session.add(o)
	try:
		session.commit()
		print (" > "+user.username+" offered a meal with "+str(portions)+" for EUR "
             +str(price)+" per portion. It will be ready at "+str(time_ready)+". \""+info+"\"")
		return "SUCCESS"
	except IntegrityError:
		print (" > Failed to add offer made by "+user.username)
		return "FAILURE"

def add_reservation(reservation):
	user_id = reservation["user_id"]
	offer_id = reservation["offer_id"]
	portions = reservation["portions"]
	session = DBSession()
	user=session.query(User).filter(User.id==user_id).first()
	offer=session.query(Offer).filter(Offer.id==offer_id).first()
	if not user:
		return "User does not exist"
	if not offer:
		return "Offer does not exist"
	r = Reservation(user=user, offer=offer, portions=portions)
	session.add(r)
	try:
		session.commit()
		print (" > "+user.username+" reserved "+str(portions)+" portions from "
				+offer.host.username+"'s home made "+offer.info)
		return "SUCCESS"
	except IntegrityError:
		print (" > Failed to reserve for user "+user.username)
		return "FAILURE"

def add_rating(rating):
	user_id = rating["user_id"]
	host_id = rating["host_id"]
	stars = rating["stars"]
	comment = rating["comment"]
	session=DBSession()
	user=session.query(User).filter(User.id==user_id).first()
	host=session.query(User).filter(User.id==host_id).first()
	if not user:
		return "User does not exist"
	if not host:
		return "Host does not exist"
	r = Rating(user=user, host=host, stars=stars, comment=comment)
	session.add(r)
	try:
		session.commit()
		print (" > "+user.username+" rated "+host.username+" with "+str(stars)+" stars: "+comment)
		return "SUCCESS"
	except IntegrityError:
		print (" > Failed to add rating made by "+user.username)
		return "FAILURE"

def message_handle(ch, method, props, body):
	msg = json.loads(body)  # body is in json format
	action = msg["action"]
	if action == "adduser":
		result = add_user(msg["username"])
	elif action == "addoffer":
		result = add_offer(msg)
	elif action == "reserve":
		result = add_reservation(msg)
	elif action == "addrating":
		result = add_rating(msg)
	else:
		result = "FAILURE"
	ch.basic_publish(exchange='', routing_key=props.reply_to,
		properties=pika.BasicProperties(correlation_id = props.correlation_id),
		body=result)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume (message_handle, queue='foodshare', no_ack=True)

print (" > Waiting for messages...")
channel.start_consuming()

