"""Unit tests for deepflow_engine constants."""

import pytest
from deepflow_engine.constants import (
    BLUE,
    RED,
    GREEN,
    BLACK,
    WHITE,
    DEFAULT_GAME_WIDTH,
    DEFAULT_GAME_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_FPS,
)


class TestColors:
    """Test color constants."""

    def test_blue_color(self):
        """Test BLUE constant is correct."""
        assert BLUE == (0, 0, 255)

    def test_red_color(self):
        """Test RED constant is correct."""
        assert RED == (255, 0, 0)

    def test_green_color(self):
        """Test GREEN constant is correct."""
        assert GREEN == (0, 255, 0)

    def test_black_color(self):
        """Test BLACK constant is correct."""
        assert BLACK == (0, 0, 0)

    def test_white_color(self):
        """Test WHITE constant is correct."""
        assert WHITE == (255, 255, 255)

    def test_color_tuple_length(self):
        """Test all color constants are RGB tuples."""
        colors = [BLUE, RED, GREEN, BLACK, WHITE]
        for color in colors:
            assert len(color) == 3
            assert all(isinstance(c, int) for c in color)
            assert all(0 <= c <= 255 for c in color)


class TestGameConstants:
    """Test game dimension constants."""

    def test_default_game_width(self):
        """Test DEFAULT_GAME_WIDTH is set."""
        assert DEFAULT_GAME_WIDTH == 360

    def test_default_game_height(self):
        """Test DEFAULT_GAME_HEIGHT is set."""
        assert DEFAULT_GAME_HEIGHT == 640

    def test_default_window_width(self):
        """Test DEFAULT_WINDOW_WIDTH is set."""
        assert DEFAULT_WINDOW_WIDTH == 720

    def test_default_window_height(self):
        """Test DEFAULT_WINDOW_HEIGHT is set."""
        assert DEFAULT_WINDOW_HEIGHT == 1280

    def test_default_fps(self):
        """Test DEFAULT_FPS is set."""
        assert DEFAULT_FPS == 60

    def test_window_is_twice_game_size(self):
        """Test window dimensions are 2x game dimensions."""
        assert DEFAULT_WINDOW_WIDTH == DEFAULT_GAME_WIDTH * 2
        assert DEFAULT_WINDOW_HEIGHT == DEFAULT_GAME_HEIGHT * 2

    def test_game_aspect_ratio(self):
        """Test game maintains 9:16 aspect ratio."""
        # 360:640 = 9:16
        assert DEFAULT_GAME_WIDTH / DEFAULT_GAME_HEIGHT == pytest.approx(0.5625)
