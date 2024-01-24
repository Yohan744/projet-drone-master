from websocket import create_connection, WebSocketException
import time
import board
import adafruit_dht
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

isActivate = False
lightCount = 0
basicHumidity = None
basicStartMoy = 0
numberOfBasicHumidity = 0
isTempDone = False

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "temperature"))

dht_left = adafruit_dht.DHT11(board.D17)
dht_right = adafruit_dht.DHT11(board.D27)


def calculateBaseHumidity(repeat=10, interval=2):
    humidity = 0
    count = 0

    while count < repeat:
        try:
            h_left = dht_left.humidity
            h_right = dht_right.humidity

            if h_left is not None and h_right is not None:
                moy = (h_left + h_right) / 2
                humidity += moy
                count += 1

            time.sleep(interval)

        except RuntimeError as e:
            time.sleep(interval)

    print("Basic humidity: ", humidity / repeat)
    return humidity / repeat


basicHumidity = calculateBaseHumidity(5, 2)


while True:
    try:

        if isActivate is True and dht_left.humidity is not None and dht_right.humidity is not None:
            h_left = dht_left.humidity
            h_right = dht_right.humidity

            if h_left is not None and h_right is not None and isinstance(h_left, int) and isinstance(h_right,int) and isTempDone is False:

                moy = (h_left + h_right) / 2
                print(moy)

                if basicHumidity is not None:
                    if ws.connected and lightCount < 10 and moy > basicHumidity + 5:
                        ws.send(messageManager.create_message(3, "humidity", moy))
                        lightCount += 1
                    else:
                        if ws.connected and lightCount >= 10:
                            print("Humidity stopped")
                            isTempDone = True

            else:
                if isTempDone is True:
                    pass
                else:
                    break

        if isActivate is False and lightCount == 0:
            mess = ws.recv()
            if mess:
                message = messageManager.get_message(mess)
                if message["action"] == "launchHumidity":
                    isActivate = True
                    print("Humidity activation")

        time.sleep(1.5)

    except RuntimeError as e:
        pass
    except Exception as e:
        pass
    except WebSocketException as e:
        pass
    except KeyboardInterrupt:
        ws.close()
