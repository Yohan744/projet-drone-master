#!/bin/bash

cd /
cd home/digital/Desktop/projetDrone/raspberry
source environment/bin/activate
cd src
python3 server.py &
sleep 3
python3 microphone.py &
sleep 1
python3 rotator.py &
sleep 1
python3 joystick.py
cd /