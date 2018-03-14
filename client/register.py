#!/usr/bin/env python

import pika
import json
import uuid

class User:
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
	
	def register (self):
		self.response = None
		
		# unique correlation id for getting response from queue
		self.corr_id = str(uuid.uuid4()) 
		
		self.channel.basic_publish(exchange='',
								   routing_key='db_adduser',
								   properties=pika.BasicProperties(
										reply_to = self.callback_queue,
										correlation_id = self.corr_id),
								   body=self.username)
		while self.response is None:
			self.connection.process_data_events()
		
		return self.response=="SUCCESS"
	
	def __del__(self):
		self.connection.close()
		print ('Connection closed')

new_user = User ()
username = raw_input("Typ in a username: ")
new_user.change_username(username)
response = new_user.register()
if response:
	print ("Hello "+username+", you have been registered!")
else:
	print ("Username already taken.")
