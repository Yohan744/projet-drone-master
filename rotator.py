from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

# Connexions WebSocket
ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "rotator"))

ws_rover = create_connection("ws://172.20.10.4:8080")
if ws_rover.connected:
    ws_rover.send(messageManager.create_message(0, "setName", "rotator"))

# Pins du rotocodeur
CLK = pin_manager.get_pin("rotator_clk")
DT = pin_manager.get_pin("rotator_dt")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clkLastState = GPIO.input(CLK)

counter = 19

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)

        if clkState != clkLastState:
            if clkState == dtState:
                counter += 1
                if counter >= 20:

                    if ws.connected:
                        ws.send(messageManager.create_message(3, "rotator", "turning"))

                    if ws_rover.connected:
                        ws_rover.send(messageManager.create_message(3, "rotator", "turning"))

                    counter = 0
            clkLastState = clkState

        time.sleep(0.005)

except KeyboardInterrupt:
    GPIO.cleanup()
