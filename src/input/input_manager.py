"""Input management and control mapping."""

import pygame
import numpy as np


class InputManager:
    """Manages keyboard, mouse, and joystick input."""
    
    def __init__(self, deadzone: float = 0.1):
        """Initialize input manager.
        
        Args:
            deadzone: Joystick deadzone (0-1)
        """
        self.deadzone = deadzone
        
        # Initialize joystick if available
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        # Control state
        self.throttle = 0.0
        self.aileron = 0.0
        self.elevator = 0.0
        self.rudder = 0.0
    
    def update(self):
        """Update input state from keyboard and joystick."""
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Elevator (pitch)
        if keys[pygame.K_w]:
            self.elevator = max(-1.0, self.elevator - 0.05)
        if keys[pygame.K_s]:
            self.elevator = min(1.0, self.elevator + 0.05)
        
        # Aileron (roll)
        if keys[pygame.K_a]:
            self.aileron = max(-1.0, self.aileron - 0.05)
        if keys[pygame.K_d]:
            self.aileron = min(1.0, self.aileron + 0.05)
        
        # Rudder (yaw)
        if keys[pygame.K_q]:
            self.rudder = max(-1.0, self.rudder - 0.05)
        if keys[pygame.K_e]:
            self.rudder = min(1.0, self.rudder + 0.05)
        
        # Throttle
        if keys[pygame.K_SPACE]:
            self.throttle = min(1.0, self.throttle + 0.01)
        if keys[pygame.K_LCTRL]:
            self.throttle = max(0.0, self.throttle - 0.01)
        
        # Return to center (damping)
        self.elevator *= 0.95
        self.aileron *= 0.95
        self.rudder *= 0.95
        
        # Joystick input
        if self.joystick:
            self.update_joystick()
    
    def update_joystick(self):
        """Update input from joystick."""
        if not self.joystick:
            return
        
        # Get analog stick axes
        # Typically: 0=X (roll), 1=Y (pitch), 2=throttle, 3=rudder
        if self.joystick.get_numaxes() > 0:
            x = self.joystick.get_axis(0)
            y = self.joystick.get_axis(1)
            
            # Apply deadzone
            if abs(x) > self.deadzone:
                self.aileron = x
            else:
                self.aileron = 0.0
            
            if abs(y) > self.deadzone:
                self.elevator = y
            else:
                self.elevator = 0.0
        
        # Throttle from analog trigger
        if self.joystick.get_numaxes() > 4:
            throttle_axis = self.joystick.get_axis(4)
            self.throttle = (throttle_axis + 1.0) / 2.0  # Convert from [-1, 1] to [0, 1]
    
    def get_controls(self) -> dict:
        """Get current control inputs.
        
        Returns:
            Dictionary with control values
        """
        return {
            'throttle': self.throttle,
            'aileron': self.aileron,
            'elevator': self.elevator,
            'rudder': self.rudder,
        }
