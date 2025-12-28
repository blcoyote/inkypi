"""
gpiozero stub module for Windows development.
"""


class Device:
    """Base device class"""
    
    def __init__(self):
        self._closed = False
    
    def close(self):
        """Close device"""
        self._closed = True
        print(f"[STUB] {self.__class__.__name__}.close()")


class LED(Device):
    """Mock LED"""
    
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self._value = 0
        print(f"[STUB] LED created on pin {pin}")
    
    def on(self):
        """Turn on"""
        self._value = 1
        print(f"[STUB] LED({self.pin}).on()")
    
    def off(self):
        """Turn off"""
        self._value = 0
        print(f"[STUB] LED({self.pin}).off()")
    
    def toggle(self):
        """Toggle state"""
        self._value = 1 - self._value
        print(f"[STUB] LED({self.pin}).toggle() -> {self._value}")


class Button(Device):
    """Mock button"""
    
    def __init__(self, pin, pull_up=True, bounce_time=None):
        super().__init__()
        self.pin = pin
        self.pull_up = pull_up
        self._pressed = False
        print(f"[STUB] Button created on pin {pin}")
    
    @property
    def is_pressed(self):
        """Check if pressed"""
        return self._pressed
    
    def wait_for_press(self, timeout=None):
        """Wait for press"""
        print(f"[STUB] Button({self.pin}).wait_for_press()")
    
    def wait_for_release(self, timeout=None):
        """Wait for release"""
        print(f"[STUB] Button({self.pin}).wait_for_release()")
