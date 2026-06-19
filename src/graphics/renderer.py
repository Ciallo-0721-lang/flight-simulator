"""Basic 2D/3D renderer using Pygame."""

import pygame
import numpy as np


class Renderer:
    """Game renderer handling all visual output."""
    
    def __init__(self, width: int, height: int):
        """Initialize renderer.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.width = width
        self.height = height
        self.display = pygame.display.get_surface()
    
    def clear(self, color: tuple = (0, 0, 0)):
        """Clear the screen with a color.
        
        Args:
            color: RGB color tuple
        """
        self.display.fill(color)
    
    def draw_text(self, text: str, font: pygame.font.Font, 
                  color: tuple, position: tuple):
        """Draw text on screen.
        
        Args:
            text: Text to render
            font: Pygame font object
            color: RGB color tuple
            position: (x, y) position on screen
        """
        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, position)
    
    def draw_line(self, start: tuple, end: tuple, color: tuple, width: int = 1):
        """Draw a line on screen.
        
        Args:
            start: (x, y) start position
            end: (x, y) end position
            color: RGB color tuple
            width: Line width in pixels
        """
        pygame.draw.line(self.display, color, start, end, width)
    
    def draw_circle(self, position: tuple, radius: int, 
                    color: tuple, width: int = 0):
        """Draw a circle on screen.
        
        Args:
            position: (x, y) center position
            radius: Circle radius in pixels
            color: RGB color tuple
            width: Line width (0 = filled)
        """
        pygame.draw.circle(self.display, color, position, radius, width)
    
    def draw_polygon(self, points: list, color: tuple, width: int = 0):
        """Draw a polygon on screen.
        
        Args:
            points: List of (x, y) vertices
            color: RGB color tuple
            width: Line width (0 = filled)
        """
        pygame.draw.polygon(self.display, color, points, width)
