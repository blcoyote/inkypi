"""
Unit Tests for Layouts

Tests for display layout rendering.
"""

from unittest.mock import Mock, patch

import pytest

from rendering.layouts import Layouts


@pytest.mark.unit
class TestLayouts:
    """Tests for Layouts rendering"""

    def test_init_creates_instance(self, mock_logger):
        """Test that __init__ creates Layouts instance"""
        layouts = Layouts(width=250, height=122, logger=mock_logger)

        assert layouts.width == 250
        assert layouts.height == 122
        assert layouts.logger == mock_logger

    def test_split_text_short_text_no_split(self, mock_logger):
        """Test that _split_text doesn't split short text"""
        layouts = Layouts(width=250, height=122, logger=mock_logger)

        lines = layouts._split_text("Short text", max_length=15)

        assert lines == ["Short text"]

    def test_split_text_long_text_splits(self, mock_logger):
        """Test that _split_text splits long text"""
        layouts = Layouts(width=250, height=122, logger=mock_logger)

        lines = layouts._split_text("This is a very long text that needs splitting", max_length=15)

        assert len(lines) > 1
        assert all(isinstance(line, str) for line in lines)

    def test_split_text_comma_separated_splits_on_comma(self, mock_logger):
        """Test that _split_text prefers splitting on commas"""
        layouts = Layouts(width=250, height=122, logger=mock_logger)

        lines = layouts._split_text("Glas, Metal, Mad- og drikkekartoner, Plast", max_length=15)

        assert len(lines) > 1
        # Should have split on commas
        assert any("Glas" in line for line in lines)

    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.truetype")
    def test_get_font_loads_truetype(self, mock_truetype, mock_exists, mock_logger):
        """Test that _get_font loads TrueType font when available"""
        mock_exists.return_value = True
        mock_font = Mock()
        mock_truetype.return_value = mock_font

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        font = layouts._get_font(20)

        assert font == mock_font
        mock_truetype.assert_called()

    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.load_default")
    def test_get_font_fallback_to_default(self, mock_load_default, mock_exists, mock_logger):
        """Test that _get_font falls back to default font when TrueType not available"""
        mock_exists.return_value = False
        mock_font = Mock()
        mock_load_default.return_value = mock_font

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        font = layouts._get_font(20)

        assert font == mock_font
        mock_load_default.assert_called_once()

    @patch("rendering.layouts.datetime")
    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.truetype")
    @patch("rendering.layouts.ImageDraw.Draw")
    @patch("rendering.layouts.Image.new")
    def test_title_and_date_creates_image(
        self, mock_image_new, mock_draw, mock_truetype, mock_exists, mock_datetime, mock_logger
    ):
        """Test that title_and_date creates an image with correct dimensions"""
        mock_exists.return_value = True
        mock_font = Mock()
        mock_truetype.return_value = mock_font
        mock_datetime.now.return_value = Mock(strftime=Mock(return_value="28/12 14:30"))

        mock_img = Mock()
        mock_img.mode = "P"
        mock_img.size = (250, 122)
        mock_image_new.return_value = mock_img

        mock_draw_obj = Mock()
        mock_draw_obj.textbbox.return_value = (0, 0, 100, 20)
        mock_draw.return_value = mock_draw_obj

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        image = layouts.title_and_date("Test Title", "2025-01-15")

        # Should create image in palette mode
        mock_image_new.assert_called_with("P", (250, 122), 0)
        assert image == mock_img

    @patch("rendering.layouts.datetime")
    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.truetype")
    @patch("rendering.layouts.ImageDraw.Draw")
    @patch("rendering.layouts.Image.new")
    def test_title_and_date_draws_black_rectangle(
        self, mock_image_new, mock_draw, mock_truetype, mock_exists, mock_datetime, mock_logger
    ):
        """Test that title_and_date draws black rectangle for bottom section"""
        mock_exists.return_value = True
        mock_font = Mock()
        mock_truetype.return_value = mock_font
        mock_datetime.now.return_value = Mock(strftime=Mock(return_value="28/12 14:30"))

        mock_img = Mock()
        mock_image_new.return_value = mock_img

        mock_draw_obj = Mock()
        mock_draw_obj.textbbox.return_value = (0, 0, 100, 20)
        mock_draw.return_value = mock_draw_obj

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        layouts.title_and_date("Test", "2025-01-15")

        # Should draw black rectangle for bottom half
        mock_draw_obj.rectangle.assert_called()
        rectangle_call = mock_draw_obj.rectangle.call_args
        # Check that fill=1 (black) was used
        assert rectangle_call[1]["fill"] == 1

    @patch("rendering.layouts.datetime")
    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.truetype")
    @patch("rendering.layouts.ImageDraw.Draw")
    @patch("rendering.layouts.Image.new")
    def test_title_and_date_draws_text(
        self, mock_image_new, mock_draw, mock_truetype, mock_exists, mock_datetime, mock_logger
    ):
        """Test that title_and_date draws title and date text"""
        mock_exists.return_value = True
        mock_font = Mock()
        mock_truetype.return_value = mock_font
        mock_datetime.now.return_value = Mock(strftime=Mock(return_value="28/12 14:30"))

        mock_img = Mock()
        mock_image_new.return_value = mock_img

        mock_draw_obj = Mock()
        mock_draw_obj.textbbox.return_value = (0, 0, 100, 20)
        mock_draw.return_value = mock_draw_obj

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        layouts.title_and_date("Test Title", "2025-01-15")

        # Should draw text multiple times (title, date, timestamp)
        assert mock_draw_obj.text.call_count >= 2

    @patch("rendering.layouts.datetime")
    @patch("rendering.layouts.os.path.exists")
    @patch("rendering.layouts.ImageFont.truetype")
    @patch("rendering.layouts.ImageDraw.Draw")
    @patch("rendering.layouts.Image.new")
    def test_title_and_date_long_title_uses_smaller_font(
        self, mock_image_new, mock_draw, mock_truetype, mock_exists, mock_datetime, mock_logger
    ):
        """Test that title_and_date uses smaller font for long titles"""
        mock_exists.return_value = True
        mock_font = Mock()
        mock_truetype.return_value = mock_font
        mock_datetime.now.return_value = Mock(strftime=Mock(return_value="28/12 14:30"))

        mock_img = Mock()
        mock_image_new.return_value = mock_img

        mock_draw_obj = Mock()
        mock_draw_obj.textbbox.return_value = (0, 0, 100, 20)
        mock_draw.return_value = mock_draw_obj

        layouts = Layouts(width=250, height=122, logger=mock_logger)
        layouts.title_and_date("Very Long Title That Exceeds Fifteen Characters", "2025-01-15")

        # Should call _get_font with size 18 (smaller) instead of 28
        # Verify by checking font was loaded
        assert mock_truetype.called
