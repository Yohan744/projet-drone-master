from websocket import create_connection, WebSocketException
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

global ws, ws_rover

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "buttons"))

ws_rover = None
try:
    ws_rover = create_connection("ws://172.20.10.4:8080")
    if ws_rover.connected:
        ws_rover.send(messageManager.create_message(0, "setName", "buttons"))
except WebSocketException as e:
    pass
except Exception as e:
    pass


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_manager.get_pin("microphone"), GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_manager.get_pin("heart"), GPIO.IN, pull_up_down=GPIO.PUD_UP)
isPumpingActive = False


def callback_micro(channel):
    state = GPIO.input(channel)
    if ws.connected:
        ws.send(messageManager.create_message(4, "microphone", f"{'off' if state else 'on'}"))


def callback_heart(channel):
    state = GPIO.input(channel)
    if ws and ws.connected and isPumpingActive:
        ws.send(messageManager.create_message(3, "pumping", "on"))
    if ws_rover and ws_rover.connected and isPumpingActive:
        ws_rover.send(messageManager.create_message(3, "pumping", "on"))


GPIO.add_event_detect(pin_manager.get_pin("microphone"), GPIO.BOTH, callback=callback_micro, bouncetime=300)
GPIO.add_event_detect(pin_manager.get_pin("heart"), GPIO.FALLING, callback=callback_heart, bouncetime=500)

try:
    while True:

        mess = ws.recv()
        if mess and mess is not None:
            message = messageManager.get_message(mess)
            if message["action"] == "fakePumping":
                if ws_rover and ws_rover.connected:
                    print("fake pumping sent")
                    ws_rover.send(messageManager.create_message(3, "pumping", "on"))
                else:
                    print("no rover connected")
            if message["action"] == "startPumping":
                isPumpingActive = True

        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    ws.close()
