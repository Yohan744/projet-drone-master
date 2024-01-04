from djitellopy import Tello
import time


class TelloController:
    def __init__(self):
        self.tello = Tello()
        print(f"Batterie: {self.tello.get_battery()}%")

    def connect(self):
        self.tello.connect()

    def takeoff(self):
        self.tello.takeoff()
        print("Le Tello a décollé")

    def land(self):
        self.tello.land()
        print("Le Tello a atterri")

    def emergency_stop(self):
        self.tello.emergency()
        print("Arrêt d'urgence activé")

    def end(self):
        self.tello.end()
        print("Connexion terminée")


tello = TelloController()
try:
    tello.takeoff()
    time.sleep(5)
    tello.land()
finally:
    tello.end()
