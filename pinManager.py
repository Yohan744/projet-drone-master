class PinManager:
    def __init__(self):
        self.pins = {
            "joystick_x": 0,
            "joystick_y": 1,
            "rotator_dt": 29,
            "rotator_clk": 31,
            "joystick_button": 33,
            "microphone": 35,
        }

    def get_pin(self, name):
        return self.pins.get(name, None)
