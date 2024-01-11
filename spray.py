from websocket import create_connection
import RPi.GPIO as GPIO
import time
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "motor"))

alreadyTurned = False


def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False

    start = 5
    end = 10
    ratio = (end - start) / 180
    angle_as_percent = angle * ratio
    return start + angle_as_percent


def activateMotor():
    global alreadyTurned
    alreadyTurned = True
    pwm.ChangeDutyCycle(angle_to_percent(0))
    time.sleep(0.25)
    pwm.ChangeDutyCycle(angle_to_percent(130))
    time.sleep(1.5)
    pwm.ChangeDutyCycle(angle_to_percent(0))
    time.sleep(1.5)
    pwm.ChangeDutyCycle(angle_to_percent(130))
    time.sleep(1.5)
    pwm.ChangeDutyCycle(angle_to_percent(0))


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pwm_gpio = pin_manager.get_pin("motor")
frequency = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequency)

pwm.start(angle_to_percent(0))
time.sleep(1)
pwm.ChangeDutyCycle(angle_to_percent(0))
time.sleep(1)

try:
    while True:
        try:
            mess = ws.recv()
            message = messageManager.get_message(mess)
            if message["action"] == "activateMotor" and not alreadyTurned:
                print("Motor activation")
                activateMotor()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Une erreur est survenue :", e)
            break

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
