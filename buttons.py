from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "buttons"))


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_manager.get_pin("microphone"), GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_manager.get_pin("heart"), GPIO.IN, pull_up_down=GPIO.PUD_UP)


def callback_micro(channel):
    state = GPIO.input(channel)
    if ws.connected:
        ws.send(messageManager.create_message(4, "microphone", f"{'off' if state else 'on'}"))


def callback_heart(channel):
    state = GPIO.input(channel)
    if ws.connected:
        ws.send(messageManager.create_message(3, "pumping", "on"))


GPIO.add_event_detect(pin_manager.get_pin("microphone"), GPIO.BOTH, callback=callback_micro, bouncetime=300)
GPIO.add_event_detect(pin_manager.get_pin("heart"), GPIO.FALLING, callback=callback_heart, bouncetime=500)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    ws.close()
