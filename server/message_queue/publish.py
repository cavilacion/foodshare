#!/usr/bin/env python

import pika
import json
import uuid
import datetime
import os

from app import ecv
from app.general_responses import *

class Publisher:
	def __init__(self):
		self.connection = pika.BlockingConnection(
						   pika.ConnectionParameters(host='127.0.0.1'))

		self.channel = self.connection.channel()
		result = self.channel.queue_declare(exclusive=True)

		self.callback_queue = result.method.queue

		self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def publish (self):
		self.response = None

		# unique correlation id for getting response from queue
		self.corr_id = str(uuid.uuid4())

		json_msg = json.dumps(self.msg)

		self.channel.basic_publish(exchange='',
								   routing_key=os.environ["QUEUE_NAME"],
								   properties=pika.BasicProperties(
										reply_to = self.callback_queue,
										correlation_id = self.corr_id),
								   body=json_msg)
		while self.response is None:
			self.connection.process_data_events()
		return self.response==b'SUCCESS'

	def adduser (self, username):
		self.msg  = {u'action': u'adduser',
				     u'username': username}
		# post message to queue
		return (self.msg if self.publish() else False)

	def deleteuser(self, user_id):
		self.msg = {u'action': u'deleteuser',
					u'user_id': user_id}
		return (self.msg if self.publish() else False)

	def addoffer (self, host_id, portions, price, info, time_ready):
		self.msg = {u'action': u'addoffer',
				 	u'host_id': host_id,
				 	u'portions': portions,
				 	u'price': price,
				 	u'info': info,
				 	u'time_ready': time_ready}
		# post message to queue
		return (self.msg if self.publish() else False)

	def updateoffer (self, offer_id, portions, price, info, time_ready):
		self.msg = {u'action': u'updateoffer',
				 	u'offer_id': offer_id,
				 	u'portions': portions,
				 	u'price': price,
				 	u'info': info,
				 	u'time_ready': time_ready}
		# post message to queue
		return (self.msg if self.publish() else False)

	def deleteoffer (self, offer_id):
		self.msg = {u'action': u'deleteoffer',
			   		u'offer_id': offer_id}
		return (self.msg if self.publish() else False)

	def addreserve (self, user_id, offer_id, portions):
		self.msg = {u'action': u'addreserve',
			   		u'user_id': user_id,
			   		u'offer_id': offer_id,
			   		u'portions': portions}
		# post message to queue
		return (self.msg if self.publish() else False)

	def updatereserve (self, reservation_id, portions):
		self.msg = {u'action': u'updatereserve',
			   		u'reservation_id': reservation_id,
			   		u'portions': portions}
		return (self.msg if self.publish() else False)

	def deletereserve (self, reservation_id):
		self.msg = {u'action': u'deletereserve',
					u'reservation_id': reservation_id}
		return (self.msg if self.publish() else False)

	def addrating (self, user_id, host_id, stars, comment):
		self.msg = {u'action': u'addrating',
				  	u'user_id': user_id,
				  	u'host_id': host_id,
				  	u'stars': stars,
				  	u'comment': comment}
		# post message to queue
		return (self.msg if self.publish() else False)

	def updaterating (self, user_id, host_id, stars, comment):
		self.msg = {u'action': u'updaterating',
					u'user_id': user_id,
					u'host_id': host_id,
					u'stars': stars,
					u'comment': comment}
		# post message to queue
		return (self.msg if self.publish() else False)

	def deleterating (self, rating_id):
		self.msg = {u'action': u'deleterating',
					u'rating_id': rating_id}
		return (self.msg if self.publish() else False)

	def __del__(self):
		self.connection.close()
		print ('Connection closed')


