"""Heads-Up Display (HUD) rendering."""

import pygame
import numpy as np
from .renderer import Renderer
from physics.aircraft import Aircraft


class HUD:
    """Flight instruments and heads-up display."""
    
    def __init__(self, renderer: Renderer, width: int, height: int):
        """Initialize HUD.
        
        Args:
            renderer: Renderer instance
            width: Screen width
            height: Screen height
        """
        self.renderer = renderer
        self.width = width
        self.height = height
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
    
    def render(self, aircraft: Aircraft, stats: dict = None):
        """Render HUD elements.
        
        Args:
            aircraft: Aircraft object with current state
            stats: Optional game statistics dictionary
        """
        if stats is None:
            stats = {}
        
        # Get aircraft state
        airspeed = aircraft.get_airspeed()
        altitude = aircraft.get_altitude()
        aoa = np.degrees(aircraft.get_angle_of_attack())
        
        # Attitude (pitch/roll)
        pitch = np.degrees(aircraft.euler_angles[1])
        roll = np.degrees(aircraft.euler_angles[0])
        
        # Render instruments in top-left
        x_offset = 20
        y_offset = 20
        line_height = 30
        
        # Airspeed
        airspeed_text = f"Airspeed: {airspeed:.1f} m/s"
        self.renderer.draw_text(airspeed_text, self.font_small, (0, 255, 0),
                               (x_offset, y_offset))
        
        # Altitude
        altitude_text = f"Altitude: {altitude:.1f} m"
        self.renderer.draw_text(altitude_text, self.font_small, (0, 255, 0),
                               (x_offset, y_offset + line_height))
        
        # Pitch and Roll
        attitude_text = f"Pitch: {pitch:.1f}° Roll: {roll:.1f}°"
        self.renderer.draw_text(attitude_text, self.font_small, (0, 255, 0),
                               (x_offset, y_offset + 2 * line_height))
        
        # Angle of Attack
        aoa_text = f"AoA: {aoa:.1f}°"
        self.renderer.draw_text(aoa_text, self.font_small, (0, 255, 0),
                               (x_offset, y_offset + 3 * line_height))
        
        # Fuel
        fuel_text = f"Fuel: {aircraft.fuel_weight:.1f} kg"
        self.renderer.draw_text(fuel_text, self.font_small, (0, 255, 0),
                               (x_offset, y_offset + 4 * line_height))
        
        # Draw artificial horizon (simplified)
        self.draw_horizon(pitch, roll)
    
    def draw_horizon(self, pitch: float, roll: float):
        """Draw artificial horizon.
        
        Args:
            pitch: Pitch angle in degrees
            roll: Roll angle in degrees
        """
        center_x = self.width * 0.75
        center_y = self.height * 0.3
        radius = 80
        
        # Draw circle
        self.renderer.draw_circle((int(center_x), int(center_y)), radius, (0, 255, 0), 2)
        
        # Draw horizon line (simplified)
        angle_rad = np.radians(roll)
        horizon_offset = pitch * 0.5  # Simplified pitch representation
        
        x1 = center_x + radius * np.cos(angle_rad)
        y1 = center_y + horizon_offset + radius * np.sin(angle_rad)
        x2 = center_x - radius * np.cos(angle_rad)
        y2 = center_y + horizon_offset - radius * np.sin(angle_rad)
        
        self.renderer.draw_line((int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
