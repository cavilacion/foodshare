# FoodShare Server Database
## Requirements
The server requires python version 2.7 with python-pip installed
To install the sql_alchemy library necessary for the server do
```
$ pip3 install sqlalchemy
```
To install the pika library necessary for RabbitMQ for client and server do
```
$ pip3 install pika
``` 
## Execution
Create a local database for the server by executing create_database
```
$ python create_database.py
```
Test the functionality by adding some users, an offer, two reservations, and two ratings
```
$ python test.py
```
Start consuming a queue that handles registration of users 
```
$ python register.py
```
Now, when in the client directory, you can try to add a username to the database by executing the same command
```
$ python register.py
```







