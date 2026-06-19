"""Game state management."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GameState(Enum):
    """Enumeration of game states."""
    
    INITIALIZING = "initializing"
    MENU = "menu"
    LOADING = "loading"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SHUTDOWN = "shutdown"


@dataclass
class GameStats:
    """Game statistics tracking."""
    
    elapsed_time: float = 0.0
    distance_traveled: float = 0.0
    altitude_max: float = 0.0
    speed_max: float = 0.0
    crashes: int = 0
    landings: int = 0
    
    def reset(self):
        """Reset all statistics."""
        self.elapsed_time = 0.0
        self.distance_traveled = 0.0
        self.altitude_max = 0.0
        self.speed_max = 0.0
        self.crashes = 0
        self.landings = 0
