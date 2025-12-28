"""
inky stub module for Windows development.
Provides basic mock for testing without actual InkyPHAT hardware.
"""

from PIL import Image


class InkyPHAT:
    """Mock InkyPHAT display"""
    
    WHITE = 0
    BLACK = 1
    RED = 2
    
    WIDTH = 250
    HEIGHT = 122
    
    def __init__(self, color="black"):
        self.color = color
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.border_color = self.BLACK
        self.h_flip = False
        self.v_flip = False
        print(f"[STUB] InkyPHAT initialized (color={color})")
    
    def set_border(self, color):
        """Set border color"""
        self.border_color = color
        print(f"[STUB] InkyPHAT.set_border({color})")
    
    def set_image(self, image):
        """Set image to display"""
        print(f"[STUB] InkyPHAT.set_image(mode={image.mode}, size={image.size})")
        # Save to file for preview
        try:
            # For palette mode, set InkyPHAT-specific palette before conversion
            if image.mode == 'P':
                # InkyPHAT palette: 0=white, 1=black, 2=red
                # Create palette with 256 entries (R, G, B for each)
                palette = [255, 255, 255,  # 0: white
                          0, 0, 0,         # 1: black
                          255, 0, 0]       # 2: red
                # Fill rest with black
                palette.extend([0, 0, 0] * 253)
                image.putpalette(palette)
                preview_image = image.convert('RGB')
            elif image.mode in ['L', '1']:
                preview_image = image.convert('RGB')
            else:
                preview_image = image
            
            preview_image.save("inky_preview.png")
            print("[STUB] Saved preview to inky_preview.png")
            print(f"[STUB] Preview stats - min: {image.getextrema()[0]}, max: {image.getextrema()[1]}")
        except Exception as e:
            print(f"[STUB] Could not save preview: {e}")
    
    def show(self):
        """Update display"""
        print("[STUB] InkyPHAT.show() - display updated")


def auto():
    """Auto-detect display"""
    print("[STUB] inky.auto() - returning mock InkyPHAT")
    return InkyPHAT()
