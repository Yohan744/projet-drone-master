from websocket import create_connection, WebSocketException
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager
import threading

messageManager = MessageManager()
pin_manager = PinManager()

isActivate = False

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "rotator"))

ws_rover = None
try:
    ws_rover = create_connection("ws://172.20.10.4:8080")
    if ws_rover.connected:
        ws_rover.send(messageManager.create_message(0, "setName", "rotator"))
except WebSocketException as e:
    print(f"WebSocketException: {e}")
except Exception as e:
    print(f"Exception: {e}")

CLK = pin_manager.get_pin("rotator_clk")
DT = pin_manager.get_pin("rotator_dt")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
clkLastState = GPIO.input(CLK)
counter = 59


def websocket_listener():
    global isActivate
    while True:
        try:
            mess = ws.recv()
            if mess:
                message = messageManager.get_message(mess)
                if message["action"] == "rotator":
                    if message["message"] == "activate":
                        isActivate = True
                        print("Activated rotator")
                    elif message["message"] == "stop":
                        isActivate = False
                        if ws_rover is not None and ws_rover.connected:
                            ws_rover.send(messageManager.create_message(3, "rotator", "stop"))
                        print("Stopped rotator")
                    elif message["message"] == "reset":
                        if ws_rover is not None and ws_rover.connected:
                            ws_rover.send(messageManager.create_message(3, "rotator", "reset"))
                        print("Reset rover")
                    elif message["message"] == "force":
                        if ws_rover is not None and ws_rover.connected:
                            ws_rover.send(messageManager.create_message(3, "rotator", "turning"))
                        print("Forced turn")
        except WebSocketException:
            pass
        except Exception as e:
            print(f"Error: {e}")


threading.Thread(target=websocket_listener, daemon=True).start()

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)
        if clkState != clkLastState and isActivate:
            if clkState == dtState:
                counter += 1
                if counter >= 60:
                    if ws_rover is not None and ws_rover.connected:
                        ws_rover.send(messageManager.create_message(3, "rotator", "turning"))
                        print("Message was sent to max")
                    print("Rotator turning")
                    counter = 0
            clkLastState = clkState

        time.sleep(0.0025)

except KeyboardInterrupt:
    GPIO.cleanup()
