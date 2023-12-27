from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager

messageManager = MessageManager()

ws = create_connection("ws://localhost:8080")
ws.send(messageManager.create_message(0, "setName", "microphone"))


GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def callback(channel):
    if GPIO.input(channel):
        ws.send(messageManager.create_message(4, "microphone", "off"))
    else:
        ws.send(messageManager.create_message(4, "microphone", "on"))


GPIO.add_event_detect(40, GPIO.BOTH, callback=callback, bouncetime=100)

while True:
    time.sleep(0.1)
    pass
