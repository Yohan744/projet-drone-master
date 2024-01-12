#!/bin/bash

cd /
cd home/digital/Desktop/projetDrone/raspberry
source environment/bin/activate
cd src
python3 server.py &
sleep 2
python3 buttons.py &
sleep 1
python3 rotator.py &
sleep 1
python3 spray.py &
sleep 1
python3 temperature.py &
sleep 1
python3 joystick.py
cd /