import spidev
import RPi.GPIO as GPIO
import time
from websocket import create_connection
from messageManager import MessageManager
from pinManager import PinManager

messageManager = MessageManager()
pin_manager = PinManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "joystick"))

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

smell = False

GPIO.setmode(GPIO.BOARD)
button_pin = pin_manager.get_pin("joystick_button")
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_callback(channel):
    global smell
    state = GPIO.input(channel)
    if state and smell == False:
        if ws.connected:
            ws.send(messageManager.create_message(1, "spray", ""))
        smell = True


GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=button_callback, bouncetime=100)


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


X_MIN = 0
X_MAX = 1023
Y_MIN = 0
Y_MAX = 1023
X_CENTER = 833
Y_CENTER = 833

DEADZONE = 0.05
x_zero_sent = True
y_zero_sent = True
last_x_value_sent = None
last_y_value_sent = None


def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def calibrate_and_map(value, min_value, max_value, center_value):
    if value < center_value:
        return round(map_value(value, min_value, center_value, -1, 0), 2)
    else:
        return round(map_value(value, center_value, max_value, 0, 1), 2)


def handle_deadzone(value, axis, zero_sent, invert=False):
    global last_x_value_sent, last_y_value_sent

    if invert:
        value = -value

    if abs(value) < DEADZONE:
        if not zero_sent:
            if ws.connected:
                ws.send(messageManager.create_message(1, f"joystick_{axis}", "0"))
            return True
    else:
        if ws.connected:
            ws.send(messageManager.create_message(1, f"joystick_{axis}", str(value)))
        return False
    return zero_sent


try:
    while True:
        raw_x = read_channel(pin_manager.get_pin("joystick_x"))
        raw_y = read_channel(pin_manager.get_pin("joystick_y"))

        x_value = calibrate_and_map(raw_x, X_MIN, X_MAX, X_CENTER)
        y_value = calibrate_and_map(raw_y, Y_MIN, Y_MAX, Y_CENTER)

        x_zero_sent = handle_deadzone(x_value, "X", x_zero_sent)
        y_zero_sent = handle_deadzone(y_value, "Y", y_zero_sent, invert=True)

        time.sleep(0.2)

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
    ws.close()
