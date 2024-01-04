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
        self.clients[client['id']] = {"address": client['address'], "handler": client["handler"], "name": None}

    def message_received(self, client, server, messageReceived):
        action = None
        message = self.messageManager.get_message(messageReceived)
        if message["action"]:
            action = message["action"]

        if action == "setName":
            name = message["message"]
            self.clients[client['id']]["name"] = name
            print(f"{name} connected")
        else:
            print(f"{action}: {message['message']}")
            print("")
            self.handleMessage(message)

    def client_left(self, client, server):
        client_name = self.clients[client['id']]['name']
        print(f"{client_name} Disconnected")
        del self.clients[client['id']]

    def handleMessage(self, message):

        if message["step_id"] == 1:
            if message["action"] == "joystick_button":
                print("smell")
            else:
                self.send_message_to("ipad", self.messageManager.create_message(1, message["action"], message["message"]))

        if message["step_id"] == 3:
            self.send_message_to("rover", self.messageManager.create_message(3, "rotator", message["message"]))

        if message["step_id"] == 4:
            self.send_message_to("web", self.messageManager.create_message(4, "microphone", message["message"]))

    def send_message_to(self, client_name, message):
        for client_id, client_info in self.clients.items():
            if client_info["name"] == client_name:
                self.server.send_message(self.clients[client_id], message)
                break
        else:
            pass
            #print(f"Client '{client_name}' not found")


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
