"""Main game engine implementation."""

import pygame
import logging
from typing import Optional
from .config import Config
from .state import GameState, GameStats


class GameEngine:
    """Main game engine managing the game loop and all systems."""
    
    def __init__(self, config: Config):
        """Initialize the game engine.
        
        Args:
            config: Game configuration
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.state = GameState.INITIALIZING
        self.stats = GameStats()
        self.running = False
        
        # Initialize Pygame
        pygame.init()
        self.logger.info("Pygame initialized")
        
        # Create display
        flags = pygame.DOUBLEBUF | pygame.OPENGL
        if config.fullscreen:
            flags |= pygame.FULLSCREEN
        
        pygame.display.set_mode(
            (config.screen_width, config.screen_height),
            flags
        )
        pygame.display.set_caption("Flight Simulator")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.logger.info(f"Display created: {config.screen_width}x{config.screen_height}")
        
        self.state = GameState.MENU
    
    def handle_events(self) -> bool:
        """Handle pygame events.
        
        Returns:
            False if quit event received, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self, delta_time: float):
        """Update game state.
        
        Args:
            delta_time: Time elapsed since last frame (seconds)
        """
        if self.state == GameState.PLAYING:
            self.stats.elapsed_time += delta_time
    
    def render(self):
        """Render the current frame."""
        # Clear screen with black
        self.config  # Avoid unused variable warning
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        self.running = True
        self.state = GameState.PLAYING
        self.logger.info("Game loop started")
        
        try:
            while self.running:
                # Calculate delta time
                delta_time = self.clock.tick(self.config.fps) / 1000.0
                
                # Handle events
                if not self.handle_events():
                    self.running = False
                    break
                
                # Update game logic
                self.update(delta_time)
                
                # Render frame
                self.render()
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the game engine."""
        self.state = GameState.SHUTDOWN
        self.logger.info("Shutting down game engine")
        pygame.quit()
