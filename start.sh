#!/bin/bash

cd /
cd home/digital/Desktop/projetDrone/raspberry
source environment/bin/activate
cd src
python3 server.py &
sleep 5
python3 microphone.py
cd /