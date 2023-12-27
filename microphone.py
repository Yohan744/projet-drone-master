from websocket import create_connection
import RPi.GPIO as GPIO
import time

ws = create_connection("ws://localhost:1234")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def callback(channel):
    if GPIO.input(channel):
        print("up")
    else:
        print("down")


GPIO.add_event_detect(40, GPIO.BOTH, callback=callback, bouncetime=100)
print("Microphone started")

while True:
    time.sleep(0.1)
    pass
