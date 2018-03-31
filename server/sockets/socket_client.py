import socket
import sys
import threading
import pickle
import time
from queue import Queue


class SocketClient:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.thread = None
        self.is_connected = False
        self.send_queue = Queue()
        self.response_queue = Queue()

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            self.socket = None

    def connect(self):
        for i in range(10):
            try:
                print("trying to connect to", self.host, str(self.port))
                self.socket.connect((self.host, self.port))
                self.is_connected = True
                self.thread = threading.Thread(target = self.wait_for_send)
                self.thread.daemon = True
                self.thread.start()
                break
            except socket.error:
                # self.socket.close()
                print("Could not open connection..")
            time.sleep(1)

    def wait_for_send(self):
        while self.is_connected:
            message = self.send_queue.get()
            print("sending message")
            self.socket.sendall(message)

            data = self.socket.recv(2048)
            self.response_queue.put(pickle.loads(data))

            self.send_queue.task_done()
    
    def send_message(self, message):
        response = None
        if self.is_connected:
            print("putting message in queue")
            self.send_queue.put(message)
            try:
                response = self.response_queue.get(block=True, timeout=1)
            except:
                print("no response from server..")
        return response
    

    def close_connection(self):
        self.is_connected = False
        self.send_queue.join()
        self.socket.close()

        # data = self.socket.recv(2048)
        
        # self.socket.close()
        # print('Received', repr(data))