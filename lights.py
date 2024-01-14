from websocket import create_connection, WebSocketException
import requests
from dotenv import load_dotenv
import os
from messageManager import MessageManager

load_dotenv()
messageManager = MessageManager()

ws = create_connection("ws://localhost:8080")
if ws.connected:
    ws.send(messageManager.create_message(0, "setName", "lights"))


access_token = os.getenv('ACCESS_TOKEN')
username = os.getenv('USERNAME')
url = f"https://api.meethue.com/bridge/{username}/groups/1/action"

headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
}


def setupBasicScene():

    sceneData = {
        "scene": "9Y0xFmgEvVB76a25"
    }

    response = requests.put(url, json=sceneData, headers=headers)


def control_lights(xy, transitiontime):

    data = {
        "on": True,
        "xy": xy,
        "bri": 100,
        "transitiontime": transitiontime
    }

    response = requests.put(url, json=data, headers=headers)


setupBasicScene()

try:
    while True:
        try:
            mess = ws.recv()
            if mess:
                message = messageManager.get_message(mess)
                if message["action"] == "turnOn":
                    control_lights([0.720000, 0.250000], 50)

        except KeyboardInterrupt:
            break
        except WebSocketException as e:
            break
        except Exception as e:
            break

finally:
    ws.close()
