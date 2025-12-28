"""
Image Rendering and Composition

This module handles image creation, layout, and styling.
"""

from PIL import Image, ImageDraw, ImageFont


class Renderer:
    """Handles image composition and rendering for display"""

    def __init__(self, width, height, logger=None):
        """
        Initialize the renderer

        Args:
            width: Image width in pixels
            height: Image height in pixels
            logger: Optional logger instance
        """
        self.width = width
        self.height = height
        self.logger = logger
        self._log_info(f"Renderer initialized: {width}x{height}")

    def create_blank_image(self, color=255):
        """
        Create a blank image

        Args:
            color: Fill color (default: 255 for white)

        Returns:
            PIL Image object
        """
        self._log_info(f"Creating blank image with color {color}")
        return Image.new("P", (self.width, self.height), color)

    def draw_text(self, image, text, position=(10, 10), font_size=20, color=0):
        """
        Draw text on an image

        Args:
            image: PIL Image object
            text: Text string to draw
            position: (x, y) tuple for text position
            font_size: Font size in points
            color: Text color (0=white, 1=black)

        Returns:
            Modified PIL Image object
        """
        self._log_info(f"Drawing text: '{text}' at {position}")

        draw = ImageDraw.Draw(image)

        # Try to use a TrueType font, fall back to default
        try:
            # Common font paths
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "C:\\Windows\\Fonts\\arial.ttf",
            ]

            font = None
            for path in font_paths:
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except Exception:
                    continue

            if font is None:
                font = ImageFont.load_default()

        except Exception as e:
            self._log_error(f"Font loading error: {e}, using default")
            font = ImageFont.load_default()

        draw.text(position, text, color, font=font)
        return image

    def draw_rectangle(self, image, bbox, fill=None, outline=None, width=1):
        """
        Draw a rectangle on an image

        Args:
            image: PIL Image object
            bbox: Bounding box as (x1, y1, x2, y2)
            fill: Fill color
            outline: Outline color
            width: Outline width

        Returns:
            Modified PIL Image object
        """
        self._log_info(f"Drawing rectangle at {bbox}")
        draw = ImageDraw.Draw(image)
        draw.rectangle(bbox, fill=fill, outline=outline, width=width)
        return image

    def draw_line(self, image, coords, fill=0, width=1):
        """
        Draw a line on an image

        Args:
            image: PIL Image object
            coords: Line coordinates as (x1, y1, x2, y2)
            fill: Line color
            width: Line width

        Returns:
            Modified PIL Image object
        """
        self._log_info(f"Drawing line from ({coords[0]},{coords[1]}) to ({coords[2]},{coords[3]})")
        draw = ImageDraw.Draw(image)
        draw.line(coords, fill=fill, width=width)
        return image

    def paste_image(self, base_image, paste_image, position=(0, 0)):
        """
        Paste one image onto another

        Args:
            base_image: Base PIL Image object
            paste_image: Image to paste
            position: (x, y) position to paste at

        Returns:
            Modified base image
        """
        self._log_info(f"Pasting image at {position}")
        base_image.paste(paste_image, position)
        return base_image

    def _log_info(self, message):
        """Log info message"""
        if self.logger:
            self.logger.info(message)

    def _log_error(self, message):
        """Log error message"""
        if self.logger:
            self.logger.error(message)
