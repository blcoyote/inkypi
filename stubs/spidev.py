"""
spidev stub module for Windows development.
"""


class SpiDev:
    """Mock SPI device"""
    
    def __init__(self):
        self.mode = 0
        self.max_speed_hz = 500000
        self.bits_per_word = 8
        print("[STUB] SpiDev created")
    
    def open(self, bus, device):
        """Open SPI device"""
        print(f"[STUB] SpiDev.open({bus}, {device})")
    
    def close(self):
        """Close SPI device"""
        print("[STUB] SpiDev.close()")
    
    def xfer(self, data):
        """Transfer data"""
        print(f"[STUB] SpiDev.xfer({len(data)} bytes)")
        return [0] * len(data)
    
    def xfer2(self, data):
        """Transfer data (variant)"""
        print(f"[STUB] SpiDev.xfer2({len(data)} bytes)")
        return [0] * len(data)
    
    def writebytes(self, data):
        """Write bytes"""
        print(f"[STUB] SpiDev.writebytes({len(data)} bytes)")
    
    def readbytes(self, n):
        """Read bytes"""
        print(f"[STUB] SpiDev.readbytes({n})")
        return [0] * n
