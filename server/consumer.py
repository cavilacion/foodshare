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
		return True
	except IntegrityError: # unique constraint must not be violated
		print (" > Username "+username+" already taken.")
		return False

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

def message_handle(ch, method, props, body):
	print (body)
	msg = json.loads(body)  # body is in json format
	print (msg)
	action = msg["action"]
	if action == "user":
		result = add_user(msg["username"])
	elif action == "offer":
		result = add_offer(msg)
	else:
		result = "FAILURE"
	ch.basic_publish(exchange='', routing_key=props.reply_to,
		properties=pika.BasicProperties(correlation_id = props.correlation_id),
		body=result)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume (message_handle, queue='foodshare', no_ack=True)

print (" > Waiting for messages...")
channel.start_consuming()

