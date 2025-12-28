"""
Layout Templates

Pre-defined layout compositions for common display patterns.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os


class Layouts:
    """Pre-defined layout templates for InkyPHAT display"""
    
    def __init__(self, width, height, logger=None):
        """
        Initialize layouts
        
        Args:
            width: Display width in pixels
            height: Display height in pixels
            logger: Optional logger instance
        """
        self.width = width
        self.height = height
        self.logger = logger
    
    def _get_font(self, size):
        """Get font with fallback"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
        
        return ImageFont.load_default()
    
    def _center_text(self, draw, text, font, bbox):
        """Calculate centered text position within bounding box"""
        # Get text bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate center position
        x = bbox[0] + (bbox[2] - bbox[0] - text_width) // 2
        y = bbox[1] + (bbox[3] - bbox[1] - text_height) // 2
        
        return (x, y)
    
    def _split_text(self, text, max_length=15):
        """
        Split text into multiple lines if it exceeds max_length
        
        Args:
            text: Text to split
            max_length: Maximum characters per line
            
        Returns:
            List of text lines
        """
        if len(text) <= max_length:
            return [text]
        
        # Try to split on comma first
        if ',' in text:
            parts = [p.strip() for p in text.split(',')]
            lines = []
            current_line = ""
            
            for part in parts:
                if not current_line:
                    current_line = part
                elif len(current_line + ", " + part) <= max_length * 1.5:
                    current_line += ", " + part
                else:
                    lines.append(current_line)
                    current_line = part
            
            if current_line:
                lines.append(current_line)
            
            # If we got reasonable lines, return them
            if len(lines) <= 3 and all(len(line) <= max_length * 1.8 for line in lines):
                return lines
        
        # Fallback: simple word wrap
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if not current_line:
                current_line = word
            elif len(current_line + " " + word) <= max_length * 1.5:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def title_and_date(self, title, date):
        """
        Create a two-section layout with title on top and date on bottom
        Top section: white background with black text
        Bottom section: black background with white text
        
        Args:
            title: Title text for top section
            date: Date text for bottom section
            
        Returns:
            PIL Image object ready for display
        """
        self._log_info(f"Creating title_and_date layout: '{title}' / '{date}'")
        
        # Create white background (use 'P' mode for palette/InkyPHAT compatibility)
        # InkyPHAT uses: 0=white, 1=black, 2=red
        image = Image.new('P', (self.width, self.height), 0)
        draw = ImageDraw.Draw(image)
        
        # Calculate division line (horizontal center)
        division_y = self.height // 2
        
        # Fill bottom section with black
        draw.rectangle([(0, division_y), (self.width, self.height)], fill=1)
        
        # Top section (Title) - black text on white background
        # Use smaller font and multi-line if title is long
        if len(title) > 15:
            title_font = self._get_font(14)
            title_lines = self._split_text(title, max_length=15)
        else:
            title_font = self._get_font(24)
            title_lines = [title]
        
        # Calculate vertical spacing for title lines
        line_height = 18  # Approximate line height for multi-line text
        total_height = len(title_lines) * line_height
        start_y = (division_y - total_height) // 2
        
        # Draw each line of title
        for i, line in enumerate(title_lines):
            # Calculate centered position for this line
            line_x = (self.width - draw.textbbox((0, 0), line, font=title_font)[2]) // 2
            line_y = start_y + (i * line_height)
            draw.text((line_x, line_y), line, font=title_font, fill=1)
        
        # Bottom section (Date) - white text on black background
        date_font = self._get_font(18)
        date_bbox = (0, division_y, self.width, self.height)
        date_pos = self._center_text(draw, date, date_font, date_bbox)
        draw.text(date_pos, date, font=date_font, fill=0)
        
        # Add tiny "Last updated" text at the bottom of date section
        update_datetime = datetime.now().strftime('%d/%m %H:%M')
        update_text = f"Updated: {update_datetime}"
        update_font = self._get_font(8)  # Very small font
        
        # Position at bottom right of the black section
        update_bbox = draw.textbbox((0, 0), update_text, font=update_font)
        update_width = update_bbox[2] - update_bbox[0]
        update_x = self.width - update_width - 3  # 3px padding from right
        update_y = self.height - 12  # 12px from bottom
        
        draw.text((update_x, update_y), update_text, font=update_font, fill=0)
        
        self._log_info("Layout created successfully")
        return image
    
    def _log_info(self, message):
        """Log info message"""
        if self.logger:
            self.logger.info(message)
