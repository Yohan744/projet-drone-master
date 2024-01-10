from websocket import create_connection
import time
import board
import adafruit_dht
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "temperature"))

dht_left = adafruit_dht.DHT11(board.D17)
dht_right = adafruit_dht.DHT11(board.D27)
while True:
    try:
        h_left = dht_left.humidity
        h_right = dht_right.humidity
        moy = (h_left + h_right) / 2

        if ws.connected:
            ws.send(messageManager.create_message(3, "humidity", moy))

    except RuntimeError as error:
        pass

    except KeyboardInterrupt:
        ws.close()
    time.sleep(2.0)
