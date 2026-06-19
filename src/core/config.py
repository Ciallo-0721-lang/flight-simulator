"""Game configuration management."""

import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Game configuration."""
    
    # Display settings
    screen_width: int = 1280
    screen_height: int = 720
    fps: int = 60
    fullscreen: bool = False
    
    # Physics settings
    physics_fps: int = 120
    gravity: float = 9.81
    
    # Graphics settings
    vsync: bool = True
    antialiasing: bool = True
    
    # Audio settings
    master_volume: float = 1.0
    music_volume: float = 0.7
    sfx_volume: float = 0.8
    
    @classmethod
    def from_file(cls, filepath: str) -> 'Config':
        """Load configuration from YAML file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            Config instance
        """
        path = Path(filepath)
        if not path.exists():
            return cls()  # Return defaults if file doesn't exist
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or {}
        
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of config
        """
        return {
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'fps': self.fps,
            'fullscreen': self.fullscreen,
            'physics_fps': self.physics_fps,
            'gravity': self.gravity,
            'vsync': self.vsync,
            'antialiasing': self.antialiasing,
            'master_volume': self.master_volume,
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
        }
