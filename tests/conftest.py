"""Pytest configuration and fixtures for Virtual Desktop Controller tests."""
import logging
import pytest
import numpy as np
from typing import Generator

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture
def sample_frame() -> np.ndarray:
    """Provide a sample video frame for testing.
    
    Returns:
        Sample frame as numpy array (480, 640, 3)
    """
    return np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)


@pytest.fixture
def blank_frame() -> np.ndarray:
    """Provide a blank/white video frame.
    
    Returns:
        Blank frame as numpy array (480, 640, 3)
    """
    return np.ones((480, 640, 3), dtype=np.uint8) * 255


@pytest.fixture
def black_frame() -> np.ndarray:
    """Provide a black video frame.
    
    Returns:
        Black frame as numpy array (480, 640, 3)
    """
    return np.zeros((480, 640, 3), dtype=np.uint8)


@pytest.fixture
def test_config() -> dict:
    """Provide test configuration.
    
    Returns:
        Dictionary with test configuration
    """
    return {
        'window_size': 30,
        'sensitivity': 0.7,
        'debug': True
    }


@pytest.fixture
def logger() -> logging.Logger:
    """Provide logger for tests.
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger('test_logger')


def pytest_configure(config):
    """Configure pytest with custom markers.
    
    Args:
        config: Pytest config object
    """
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers.
    
    Args:
        config: Pytest config object
        items: List of test items
    """
    for item in items:
        # Add unit marker by default
        if not any(marker.name in ['integration', 'performance']
                  for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
