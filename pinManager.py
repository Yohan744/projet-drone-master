class PinManager:
    def __init__(self):
        self.pins = {
            "microphone": 40,
        }

    def get_pin(self, sensor_name):
        return self.pins.get(sensor_name)
