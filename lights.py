from websocket import create_connection, WebSocketException
import requests
from dotenv import load_dotenv
import os
from messageManager import MessageManager

load_dotenv()
messageManager = MessageManager()

currentLightIndex = 0
lightTab = [
    [0.1911, 0.1754],
    [0.2323, 0.2008],
    [0.2734, 0.2262],
    [0.3146, 0.2516],
    [0.3557, 0.2771],
    [0.3968, 0.3025],
    [0.4380, 0.3279],
    [0.4791, 0.3533],
    [0.5203, 0.3987],
]

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
        "scene": os.getenv('SCENE_ID')
    }
    response = requests.put(url, json=sceneData, headers=headers)


def control_lights(xy, transitiontime):

    data = {
        "on": True,
        "xy": xy,
        "bri": 254,
        "transitiontime": transitiontime
    }

    response = requests.put(url, json=data, headers=headers)


# setupBasicScene()
control_lights([0.5203, 0.3987], 10)

try:
    while True:
        try:
            mess = ws.recv()
            if mess:
                message = messageManager.get_message(mess)

                if message["action"] == "start":
                    control_lights([0.15, 0.15], 50)

                if message["action"] == "update":
                    if currentLightIndex < len(lightTab) and lightTab[currentLightIndex] is not None:
                        control_lights(lightTab[currentLightIndex], 15)
                        currentLightIndex += 1

                if message["action"] == "fake":
                    control_lights([0.5203, 0.3987], 100)

        except KeyboardInterrupt:
            break
        except WebSocketException as e:
            break
        except Exception as e:
            break

finally:
    ws.close()
