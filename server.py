from websocket_server import WebsocketServer
import threading
import time
import RPi.GPIO as GPIO


micro_button_PIN = 40


def message_received(client, server, message):
    print("Message reçu :", message)
    server.send_message(client, message)  # Echo du message


def new_client(client, server):
    print("")
    print(f"{client['address']} connecté")
    print("")


def client_left(client, server):
    print(f"{client['address']} déconnecté")


server = WebsocketServer(port=1234, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.set_fn_client_left(client_left)

try:
    threading.Thread(target=server.run_forever).start()
    print("Server started on port 1234")

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated and GPIO cleaned up")