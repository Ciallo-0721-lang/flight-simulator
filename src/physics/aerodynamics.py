"""Aerodynamic model for flight simulation."""

import numpy as np
from typing import Tuple
from .aircraft import Aircraft, AircraftProperties


class AerodynamicsModel:
    """Aerodynamic force and moment calculations."""
    
    # Sea level standard atmosphere
    AIR_DENSITY_SEA_LEVEL = 1.225  # kg/m³
    TEMP_SEA_LEVEL = 288.15  # K
    TEMP_LAPSE_RATE = 0.0065  # K/m
    
    def __init__(self):
        """Initialize aerodynamics model."""
        self.air_density = self.AIR_DENSITY_SEA_LEVEL
    
    def calculate_air_density(self, altitude: float) -> float:
        """Calculate air density at given altitude.
        
        Args:
            altitude: Altitude in meters
            
        Returns:
            Air density in kg/m³
        """
        temp = self.TEMP_SEA_LEVEL - self.TEMP_LAPSE_RATE * altitude
        temp = max(temp, 216.65)  # Minimum temperature in stratosphere
        
        temp_ratio = temp / self.TEMP_SEA_LEVEL
        pressure_ratio = temp_ratio ** (-5.255877)
        
        self.air_density = self.AIR_DENSITY_SEA_LEVEL * pressure_ratio
        return self.air_density
    
    def calculate_dynamic_pressure(self, velocity: float) -> float:
        """Calculate dynamic pressure.
        
        Args:
            velocity: True airspeed in m/s
            
        Returns:
            Dynamic pressure in Pa
        """
        return 0.5 * self.air_density * velocity ** 2
    
    def calculate_lift_coefficient(self, aoa: float, aircraft: Aircraft) -> float:
        """Calculate lift coefficient.
        
        Args:
            aoa: Angle of attack in radians
            aircraft: Aircraft object
            
        Returns:
            Lift coefficient (CL)
        """
        props = aircraft.properties
        
        # Convert to degrees for calculation
        aoa_deg = np.degrees(aoa)
        
        # Linear lift curve with stall
        if abs(aoa_deg) > props.stall_angle:
            # Post-stall behavior (simplified)
            cl = props.cl_max * np.sign(aoa_deg) * 0.5
        else:
            # Linear region
            cl_slope = 2 * np.pi * props.wing_area / (props.wing_span ** 2)  # Simplified
            cl = cl_slope * aoa
        
        return np.clip(cl, -props.cl_max * 1.5, props.cl_max * 1.5)
    
    def calculate_drag_coefficient(self, cl: float, aircraft: Aircraft) -> float:
        """Calculate drag coefficient.
        
        Args:
            cl: Lift coefficient
            aircraft: Aircraft object
            
        Returns:
            Drag coefficient (CD)
        """
        props = aircraft.properties
        
        # Parasitic drag + induced drag
        cd_parasitic = props.cd0
        cd_induced = props.k * cl ** 2
        
        return cd_parasitic + cd_induced
    
    def calculate_aerodynamic_forces(self, aircraft: Aircraft) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate aerodynamic forces and moments.
        
        Args:
            aircraft: Aircraft object
            
        Returns:
            Tuple of (forces, moments) in body frame
        """
        props = aircraft.properties
        airspeed = aircraft.get_airspeed()
        altitude = aircraft.get_altitude()
        aoa = aircraft.get_angle_of_attack()
        
        # Update air density
        self.calculate_air_density(altitude)
        
        # Calculate aerodynamic coefficients
        q = self.calculate_dynamic_pressure(airspeed)
        cl = self.calculate_lift_coefficient(aoa, aircraft)
        cd = self.calculate_drag_coefficient(cl, aircraft)
        
        # Force magnitudes
        lift = q * props.wing_area * cl
        drag = q * props.wing_area * cd
        
        # Forces in wind frame [lift, drag, side force]
        # Convert to body frame
        if airspeed > 0.1:
            # Axis conversion
            cos_aoa = np.cos(aoa)
            sin_aoa = np.sin(aoa)
            
            # Body frame forces
            fx = -drag * cos_aoa + lift * sin_aoa
            fz = -drag * sin_aoa - lift * cos_aoa
            fy = 0.0  # Simplified, no side force
        else:
            fx = fy = fz = 0.0
        
        forces = np.array([fx, fy, fz], dtype=np.float64)
        
        # Simplified moments (control surface effects)
        # These would be calculated from control surface deflections
        moments = np.array([0.0, 0.0, 0.0], dtype=np.float64)
        
        return forces, moments
