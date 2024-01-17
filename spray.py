from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "spray"))

alreadySprayed = False


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
sprayPin = pin_manager.get_pin("spray")
GPIO.setup(sprayPin, GPIO.OUT)
GPIO.output(sprayPin, GPIO.HIGH)


def activateSpray():
    GPIO.output(sprayPin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(sprayPin, GPIO.HIGH)
    time.sleep(4)
    GPIO.output(sprayPin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(sprayPin, GPIO.HIGH)


try:
    while True:
        try:
            mess = ws.recv()
            message = messageManager.get_message(mess)
            if message["action"] == "activateSpray" and not alreadySprayed:
                print("Spray activation")
                activateSpray()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Une erreur est survenue :", e)
            break

except KeyboardInterrupt:
    GPIO.output(sprayPin, GPIO.HIGH)
    GPIO.cleanup()
