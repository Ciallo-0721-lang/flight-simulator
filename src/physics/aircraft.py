"""Aircraft model and properties."""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AircraftProperties:
    """Physical properties of an aircraft."""
    
    # Basic properties
    name: str
    mass: float  # kg
    wing_area: float  # m²
    wing_span: float  # m
    mean_chord: float  # m
    
    # Aerodynamic coefficients
    cl_max: float  # Maximum lift coefficient
    cd0: float  # Zero-lift drag coefficient
    k: float  # Induced drag coefficient
    stall_angle: float  # Stall angle (degrees)
    
    # Engine properties
    max_thrust: float  # N
    specific_fuel_consumption: float  # kg/(N·s)
    max_fuel_capacity: float  # kg
    
    # Inertia matrix (approximation)
    ixx: float  # kg·m²
    iyy: float  # kg·m²
    izz: float  # kg·m²
    ixz: float = 0.0  # kg·m² (cross-product term)
    
    @classmethod
    def cessna_172(cls) -> 'AircraftProperties':
        """Create a Cessna 172 aircraft configuration.
        
        Returns:
            AircraftProperties for Cessna 172
        """
        return cls(
            name="Cessna 172",
            mass=1157,
            wing_area=16.17,
            wing_span=11.0,
            mean_chord=1.47,
            cl_max=1.4,
            cd0=0.027,
            k=0.0525,
            stall_angle=16.0,
            max_thrust=41600,  # N
            specific_fuel_consumption=0.085e-6,
            max_fuel_capacity=122,  # kg
            ixx=963.0,
            iyy=1087.0,
            izz=1946.0,
        )


class Aircraft:
    """Aircraft model combining properties and state."""
    
    def __init__(self, properties: AircraftProperties):
        """Initialize aircraft.
        
        Args:
            properties: Aircraft properties
        """
        self.properties = properties
        
        # Position (m) - [x, y, z] in world frame
        self.position = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        
        # Velocity (m/s) - [u, v, w] in body frame
        self.velocity_body = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        
        # Euler angles (rad) - [roll, pitch, yaw]
        self.euler_angles = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        
        # Angular velocity (rad/s) - [p, q, r] in body frame
        self.angular_velocity = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        
        # Control inputs
        self.throttle = 0.0  # 0-1
        self.aileron = 0.0   # -1 to 1 (roll control)
        self.elevator = 0.0  # -1 to 1 (pitch control)
        self.rudder = 0.0    # -1 to 1 (yaw control)
        
        # Fuel state
        self.fuel_weight = properties.max_fuel_capacity
    
    def get_airspeed(self) -> float:
        """Get true airspeed.
        
        Returns:
            True airspeed in m/s
        """
        return np.linalg.norm(self.velocity_body)
    
    def get_altitude(self) -> float:
        """Get altitude above sea level.
        
        Returns:
            Altitude in meters
        """
        return -self.position[2]  # Z is negative up
    
    def get_angle_of_attack(self) -> float:
        """Get angle of attack.
        
        Returns:
            Angle of attack in radians
        """
        u = self.velocity_body[0]
        w = self.velocity_body[2]
        
        if u == 0.0:
            return 0.0
        
        return np.arctan2(w, u)
    
    def update_fuel(self, delta_time: float, thrust: float):
        """Update fuel consumption.
        
        Args:
            delta_time: Time step (seconds)
            thrust: Current engine thrust (N)
        """
        fuel_burn_rate = thrust * self.properties.specific_fuel_consumption
        fuel_consumed = fuel_burn_rate * delta_time
        self.fuel_weight = max(0.0, self.fuel_weight - fuel_consumed)
    
    def get_total_mass(self) -> float:
        """Get total aircraft mass including fuel.
        
        Returns:
            Total mass in kg
        """
        return self.properties.mass + self.fuel_weight
