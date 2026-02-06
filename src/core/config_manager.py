import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        self.config_data: Dict[str, Any] = {}
        self.initialized = True
        self.load_configs()

    def load_configs(self):
        """Load all configuration files from the config directory."""
        if not self.config_dir.exists():
            logger.warning(f"Config directory not found: {self.config_dir}")
            return

        for config_file in self.config_dir.glob("*.json"):
            try:
                with open(config_file, 'r') as f:
                    self.config_data[config_file.stem] = json.load(f)
                logger.info(f"Loaded config: {config_file.name}")
            except Exception as e:
                logger.error(f"Failed to load config {config_file.name}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'hardware_config.resolution')."""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    @property
    def hardware_tier(self) -> str:
        """Get the configured hardware tier."""
        return self.get("hardware_config.tier", "mid")
