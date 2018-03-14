import datetime
import pika
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from classes import Base, User, Offer, Reservation, Rating


# setup database connection
engine = create_engine('sqlite:///foodshare.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# setup rabbitmq connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='db_adduser')


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
	'''
	Here code that does a mutual verification with other servers
	that this username will be taken
	'''

def register_users(ch, method, props, username):
	print (" > New user " + username + " tries to register")
	result = add_user (username)
	if result:
		response="SUCCESS"
	else:
		response="FAILURE"
	print (" > Will return "+response+" to "+username)
	ch.basic_publish(exchange='', routing_key=props.reply_to,
		properties=pika.BasicProperties(correlation_id = props.correlation_id),
		body=response)
					 

channel.basic_qos(prefetch_count=1)
channel.basic_consume (register_users, queue='db_adduser', no_ack=True)

print (" > Waiting for people to register...")
channel.start_consuming()

