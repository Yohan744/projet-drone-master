from websocket import create_connection
import time
import board
import adafruit_dht
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

isActivate = False

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "temperature"))

dht_left = adafruit_dht.DHT11(board.D17)
dht_right = adafruit_dht.DHT11(board.D27)

while True:
    try:

        if isActivate is True:
            h_left = dht_left.humidity
            h_right = dht_right.humidity
            temp = dht_right.temperature

            if h_left is not None and h_right is not None and isinstance(h_left, int) and isinstance(h_right, int):
                moy = (h_left + h_right) / 2
                if ws.connected:
                    ws.send(messageManager.create_message(3, "humidity", moy))
                else:
                    print("Humidity is not activated")
            else:
                break

        if isActivate is False:
            mess = ws.recv()
            if mess:
                message = messageManager.get_message(mess)
                if message["action"] == "launchHumidity":
                    isActivate = True
                    print("Humidity activation")

        time.sleep(2.0)

    except RuntimeError as error:
        pass
    except Exception as e:
        pass
    except KeyboardInterrupt:
        ws.close()
