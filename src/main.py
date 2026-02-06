#!/usr/bin/env python3
"""
Virtual Desktop Controller - Main Entry Point

Multimodal eye-gaze and gesture control for motor-impaired accessibility.
DIPEX 2026 Project
"""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Add src directory to path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from core.logger import setup_logger
from core.config_manager import ConfigManager
from ui.main_window import MainWindow

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
        
        # Initialize UI Application
        app = QApplication(sys.argv)
        
        logger.info("Initializing UI...")
        main_window = MainWindow()
        main_window.run() # Shows validity
        
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
