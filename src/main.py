#!/usr/bin/env python3
"""
Virtual Desktop Controller - Main Entry Point

Multimodal eye-gaze and gesture control for motor-impaired accessibility.
DIPEX 2026 Project
"""

import sys
import logging
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from core.logger import setup_logger
from core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for Virtual Desktop Controller.
    """
    try:
        # Initialize logger
        logger = setup_logger(__name__)
        logger.info("Starting Virtual Desktop Controller...")
        
        # Load configuration
        config = ConfigManager()
        logger.info(f"Configuration loaded. Hardware tier: {config.hardware_tier}")
        
        # Import and initialize modules
        from gesture.gesture_recognizer import GestureRecognizer
        from eyetracking.gaze_estimator import GazeEstimator
        from ui.main_window import MainWindow
        
        # Initialize UI
        logger.info("Initializing UI...")
        app = MainWindow()
        app.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
