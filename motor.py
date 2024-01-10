#!/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time

def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False

    start = 5
    end = 10
    ratio = (end - start) / 180  # Calcul ratio from angle to percent
    angle_as_percent = angle * ratio
    return start + angle_as_percent

GPIO.setmode(GPIO.BOARD)  # Use Board numerotation mode
GPIO.setwarnings(False)  # Disable warnings

# Use pin 12 for PWM signal
pwm_gpio = 12
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

# Start PWM at 0°
pwm.start(angle_to_percent(0))
time.sleep(1)
pwm.ChangeDutyCycle(angle_to_percent(0))
time.sleep(1)

try:
    while True:
        pwm.ChangeDutyCycle(angle_to_percent(150))
        time.sleep(2)

        pwm.ChangeDutyCycle(angle_to_percent(0))
        time.sleep(2)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
