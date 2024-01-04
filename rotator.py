from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
ws.send(messageManager.create_message(0, "setName", "rotator"))

CLK = pin_manager.get_pin("rotator_clk")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(CLK)

try:
    while True:
        clkState = GPIO.input(CLK)

        if clkState != clkLastState:
            counter += 1
            print("Rotator: " + str(counter))
            ws.send(messageManager.create_message(3, "rotator", "turning"))
        clkLastState = clkState

        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
