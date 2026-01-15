"""Logger module for Virtual Desktop Controller."""
import logging
from pathlib import Path

class Logger:
    """Handles application logging."""
    
    def __init__(self, name: str = 'VirtualDesktopController', log_dir: str = 'logs'):
        """Initialize logger.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up logging handlers."""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(
            self.log_dir / 'app.log'
        )
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
