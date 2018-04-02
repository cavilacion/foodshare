
# FoodShare Server

## Dependencies
The server requires python version 3.6. 

To install the dependencies, create a virtualenv and run:
```
$ pip install -r requirements.txt
```

after this, you can go to the root directory and run:
```
$ python3 server.py
```
This will start the program. It will start up different threads for the different components. 


To populate the database with some initial data, run:
```
$ python3 fixtures.py
```

## Sockets

When other server presets (Client objects) are specified in the server.py file, the server will try to connect to these servers.

If the server is able to connect succesfully, the servers will synchronize their databases.

snippet from server.py:
```
client1 = SocketClient('127.0.0.1', presets[setting]['clients'][0])
client2 = SocketClient('127.0.0.1', presets[setting]['clients'][1])

clients = [client1] # Add clients here to test network sockets
```

Identical servers using different ports (from the presets specified in server.py) can be run using a command line argument:

```
$ python3 server.py 0
$ python3 server.py 1
```

## Tests

To run tests for the REST api, run:
These will only test the REST api. But it does not properly test the message queue backend yet..

```
$ pytest
```








