import json
import threading
import socketio
import requests
import asyncio
from project.util.data import add_new
# from project.util.generate_socket import sio
from .observer import Observer
import socketio


sio = socketio.Client()


class ObserverMiddleware(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config = config["connection_config"]
        self.token = self.get_socket_token()
        self.sio = sio
        self.call_one = True

    def run(self):
        asyncio.run(
            self.sio.connect(f'{self.config["host"]}:{self.config["port"]}/?token={self.token}',
                        transports=["websocket"],
                        namespaces=['/all'],
                        socketio_path='socket.io'))

    def stop(self):
        raise SystemExit()

    def get_token_dojot(self):
        url = f'{self.config["host"]}:{self.config["port"]}/auth'
        payload = {"username": self.config["user"], "passwd": self.config["password"]}
        headers = {"Content-Type": "application/json"}
        return requests.post(url, headers=headers, json=payload).json()["jwt"]

    def get_socket_token(self):
        url = f'{self.config["host"]}:{self.config["port"]}/stream/socketio'
        token = self.get_token_dojot()
        headers = {"Authorization": f"Bearer {token}"}
        return requests.request("GET", url, headers=headers).json()['token']

    @sio.on('all')
    def on_message(data):
        
        print(f'\n{data}\n')

    @sio.event
    async def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(err):
        print(err)
        print("\nThe connection failed!\n")
        sio.disconnect()

    @sio.event
    def disconnect():
        print("I'm disconnected!")
