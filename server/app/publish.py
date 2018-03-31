#!/usr/bin/env python

import pika
import json
import uuid
import datetime

from app import ecv
from app.general_responses import *

class Publisher:
	def __init__(self):
		self.username=""

		self.connection = pika.BlockingConnection(
						   pika.ConnectionParameters(host='localhost'))

		self.channel = self.connection.channel()
		result = self.channel.queue_declare(exclusive=True)

		self.callback_queue = result.method.queue

		self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

	def change_username (self, u_name):
		self.username=u_name

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def publish (self):
		self.response = None

		# unique correlation id for getting response from queue
		self.corr_id = str(uuid.uuid4())

		self.channel.basic_publish(exchange='',
								   routing_key='foodshare',
								   properties=pika.BasicProperties(
										reply_to = self.callback_queue,
										correlation_id = self.corr_id),
								   body=self.json_msg)
		while self.response is None:
			self.connection.process_data_events()
		return self.response==b'SUCCESS'

	def register (self):
		# prepare json message
		self.json_msg = '{"action":"user","username":"'+self.username+'"}'
		# post message to queue
		return self.publish()

	def offer (self, host_id, portions, price, info, time_ready):
		# prepare json message
		offer = {u'action': u'offer',
				 u'host_id': host_id,
				 u'portions': portions,
				 u'price': price,
				 u'info': info,
				 u'time_ready': time_ready}
		self.json_msg=json.dumps(offer)

		# post message to queue
		return (offer if self.publish() else False)

	def __del__(self):
		self.connection.close()
		print ('Connection closed')


