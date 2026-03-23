"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def temp_frames_dir(tmp_path):
    """Create a temporary frames directory for testing."""
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()
    return frames_dir


@pytest.fixture
def temp_collision_log(tmp_path):
    """Create a temporary collision log file path."""
    return tmp_path / "collisions_log.json"


@pytest.fixture
def sample_game_config():
    """Provide sample game configuration."""
    return {
        "fps": 60,
        "caption": "Test Game",
        "display_surface_width": 400,
        "display_surface_height": 600,
    }
