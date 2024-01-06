from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
ws.send(messageManager.create_message(0, "setName", "microphone"))


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_manager.get_pin("microphone"), GPIO.IN, pull_up_down=GPIO.PUD_UP)


def callback(channel):
    state = GPIO.input(channel)
    ws.send(messageManager.create_message(4, "microphone", f"{'off' if state else 'on'}"))


GPIO.add_event_detect(pin_manager.get_pin("microphone"), GPIO.BOTH, callback=callback, bouncetime=1)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    ws.close()
