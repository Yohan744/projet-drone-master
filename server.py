from websocket_server import WebsocketServer
from messageManager import MessageManager
import RPi.GPIO as GPIO
import threading
import time


class Server:
    def __init__(self):
        self.server = WebsocketServer(port=8080, host='0.0.0.0')
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.message_received)
        self.server.set_fn_client_left(self.client_left)
        self.messageManager = MessageManager()
        self.clients = {}

    def new_client(self, client, server):
        self.clients[client['id']] = {"address": client['address'], "name": None}

    def message_received(self, client, server, messageReceived):
        message = self.messageManager.get_message(messageReceived)
        action = message["action"]

        if action == "setName":
            name = message["message"]
            self.clients[client['id']]["name"] = name
            print(f"{name} connected")
        else:
            print(f"{action}: {message['message']}")

    def client_left(self, client, server):
        client_name = self.clients[client['id']]['name']
        print(f"{client_name} Disconnected")
        del self.clients[client['id']]


server = Server()

try:
    threading.Thread(target=server.server.run_forever).start()
    print("")
    print("Server started on port 8080")
    print("")

    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated and GPIO cleaned up")
