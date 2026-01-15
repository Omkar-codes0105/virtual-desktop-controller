"""Configuration manager for Virtual Desktop Controller."""
import json
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or 'config'
        self.config: Dict[str, Any] = {}
    
    def load(self, filename: str) -> bool:
        """Load configuration from file.
        
        Args:
            filename: Name of configuration file
            
        Returns:
            True if loading was successful
        """
        try:
            path = Path(self.config_path) / filename
            if path.exists():
                with open(path, 'r') as f:
                    self.config = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
