"""Core module for Virtual Desktop Controller."""

from .camera import Camera
from .config_manager import ConfigManager
from .logger import setup_logger

__all__ = [
    'Camera',
    'ConfigManager',
    'setup_logger'
]
