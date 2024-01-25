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
        self.updatedLightsCount = 0
        self.isJoystickActive = False

    def new_client(self, client, server):
        self.clients[client['id']] = {"address": client['address'], "handler": client["handler"], "name": None}

    def message_received(self, client, server, messageReceived):
        action = None
        message = self.messageManager.get_message(messageReceived)
        if message["action"] and message is not None:
            action = message["action"]

        if action == "setName":
            name = message["message"]
            self.clients[client['id']]["name"] = name
            self.send_message_to(name, self.messageManager.create_message(0, "callback", "connected"))
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
            if message["action"] == "spray":
                self.isJoystickActive = True
                self.send_message_to("spray", self.messageManager.create_message(1, "activateSpray", message["message"]))
            else:
                if self.isJoystickActive:
                    self.send_message_to("ipad", self.messageManager.create_message(1, message["action"], message["message"]))

        if message["step_id"] == 3:

            if message["action"] == "rotator":
                self.send_message_to("rotator", self.messageManager.create_message(3, message["action"], message["message"]))

            if message["action"] == "startHumidity":
                self.send_message_to("temperature", self.messageManager.create_message(3, "launchHumidity", ""))
                self.send_message_to("lights", self.messageManager.create_message(3, "start", ""))
            if message["action"] == "humidity":
                if message["message"] is not None and self.updatedLightsCount < 10:
                    self.updatedLightsCount += 1
                    self.send_message_to("lights", self.messageManager.create_message(3, "update", ""))

            if message["action"] == "fakeLights":
                self.send_message_to("lights", self.messageManager.create_message(3, "fake", ""))

            if message["action"] == "startPumping":
                self.send_message_to("buttons", self.messageManager.create_message(3, "startPumping", ""))

            if message["action"] == "fakePumping":
                self.send_message_to("buttons", self.messageManager.create_message(3, "fakePumping", ""))

        if message["step_id"] == 4:
            if message["action"] == "microphone":
                self.send_message_to("web", self.messageManager.create_message(4, "microphone", message["message"]))

            if message["action"] == "remote":
                self.send_message_to("web", self.messageManager.create_message(4, "remote", message["message"]))

            if message["action"] == "cancelLoop":
                self.send_message_to("web", self.messageManager.create_message(4, "cancelLoop", message["message"]))

    def send_message_to(self, client_name, message):
        for client_id, client_info in self.clients.items():
            if client_info["name"] == client_name:
                self.server.send_message(self.clients[client_id], message)
                break
        else:
            pass
            print(f"Client '{client_name}' not found")


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
