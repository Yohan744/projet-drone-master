from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager


messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
ws.send(messageManager.create_message(0, "setName", "joystick"))

GPIO.setmode(GPIO.BOARD)
x_pin = pin_manager.get_pin("joystick_x")
y_pin = pin_manager.get_pin("joystick_y")
button_pin = pin_manager.get_pin("joystick_button")

GPIO.setup(x_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(y_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def x_callback(channel):
    state = GPIO.input(channel)
    ws.send(messageManager.create_message(1, "joystick", f"X {'on' if state else 'off'}"))


def y_callback(channel):
    state = GPIO.input(channel)
    ws.send(messageManager.create_message(1, "joystick", f"Y {'on' if state else 'off'}"))


def button_callback(channel):
    state = GPIO.input(channel)
    ws.send(messageManager.create_message(1, "joystick_button", "pressed" if state else "released"))


GPIO.add_event_detect(x_pin, GPIO.BOTH, callback=x_callback, bouncetime=100)
GPIO.add_event_detect(y_pin, GPIO.BOTH, callback=y_callback, bouncetime=100)
GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=button_callback, bouncetime=100)


try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    ws.close()
