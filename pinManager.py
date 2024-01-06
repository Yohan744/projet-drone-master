class PinManager:
    def __init__(self):
        self.pins = {
            "microphone": 40,
            "joystick_x": 0,
            "joystick_y": 1,
            "joystick_button": 38,
            "rotator_clk": 29,
            "rotator_dt": 31
        }

    def get_pin(self, name):
        return self.pins.get(name, None)
