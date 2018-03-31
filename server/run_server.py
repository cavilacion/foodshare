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
	host_username = offer["host"]
	portions = int(offer["portions"])
	price = float(offer["price"])
	info = offer["info"]
	time_ready = offer["time_ready"]
	time_ready = datetime.strptime(time_ready, '%Y-%m-%d %H:%M:%S.%f')
	time_created = offer["time_created"]
	time_created = datetime.strptime(time_created, '%Y-%m-%d %H:%M:%S.%f')
	# check some constraints ???
  
	session=DBSession()
	user=session.query(User).filter(User.username==host_username).first()
	o = Offer(host_id=user.id, portions=portions, price=price, info=info, time_ready=time_ready,
									time_created=time_created)
	session.add(o)
	try:
		session.commit()
		print (" > "+host_username+" offered a meal with "+str(portions)+" for EUR "
             +str(price)+" per portion. It will be ready at "+str(time_ready)+". \""+info+"\"")
		return True
	except IntegrityError:
		print (" > Failed to add offer made by "+host_username)
		return False

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
		result = False
	if result:
		response="SUCCESS"
	else:
		response="FAILURE"
	ch.basic_publish(exchange='', routing_key=props.reply_to,
		properties=pika.BasicProperties(correlation_id = props.correlation_id),
		body=response)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume (message_handle, queue='foodshare', no_ack=True)

print (" > Waiting for messages...")
channel.start_consuming()

