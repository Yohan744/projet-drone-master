from djitellopy import Tello
import keyboard
import time


class TelloController:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.is_flying = False
        self.has_flipped_back = False

    def start(self):
        battery_level = self.tello.get_battery()
        if battery_level < 20:
            print(f"Battery too low for takeoff: {battery_level}%")
        else:
            self.is_flying = True
            self.tello.send_command_without_return("takeoff")
            time.sleep(4)
            self.tello.send_command_without_return("cw 30")
            time.sleep(3)
            self.tello.send_command_without_return("ccw 60")
            time.sleep(3)
            self.tello.send_command_without_return("cw 30")

    def goBack(self):
        self.tello.send_command_without_return("flip b")
        self.has_flipped_back = True

    def stop(self):
        print("Landing")
        self.tello.send_command_without_return("land")
        self.is_flying = False

    def keep_connection_active(self):
        battery = self.tello.get_battery()
        print("Battery: " + str(battery))

    def emergency(self):
        print("Emergency landing")
        self.tello.send_command_without_return("emergency")
        self.is_flying = False

    def run(self):
        connection_counter = 0
        try:
            while True:
                if keyboard.is_pressed('d') and not self.is_flying:
                    self.start()
                elif keyboard.is_pressed('space'):
                    self.emergency()
                    break

                if keyboard.is_pressed("p") and self.is_flying and not self.has_flipped_back:
                    self.goBack()

                if connection_counter >= 50:
                    self.keep_connection_active()
                    connection_counter = 0
                else:
                    connection_counter += 1

                time.sleep(0.1)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop()


controller = TelloController()
controller.keep_connection_active()
controller.run()
