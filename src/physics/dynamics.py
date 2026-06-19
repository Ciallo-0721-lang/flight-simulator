"""Flight dynamics implementation using 6-DOF rigid body model."""

import numpy as np
from typing import Tuple
from .aircraft import Aircraft
from .aerodynamics import AerodynamicsModel


class FlightDynamics:
    """6-DOF rigid body flight dynamics."""
    
    GRAVITY = 9.81  # m/s²
    
    def __init__(self, aircraft: Aircraft):
        """Initialize flight dynamics.
        
        Args:
            aircraft: Aircraft model
        """
        self.aircraft = aircraft
        self.aerodynamics = AerodynamicsModel()
    
    def get_rotation_matrix(self, euler_angles: np.ndarray) -> np.ndarray:
        """Get rotation matrix from body to world frame.
        
        Args:
            euler_angles: [roll, pitch, yaw] in radians
            
        Returns:
            3x3 rotation matrix
        """
        roll, pitch, yaw = euler_angles
        
        # Rotation matrices for each axis
        R_roll = np.array([
            [1, 0, 0],
            [0, np.cos(roll), np.sin(roll)],
            [0, -np.sin(roll), np.cos(roll)]
        ])
        
        R_pitch = np.array([
            [np.cos(pitch), 0, -np.sin(pitch)],
            [0, 1, 0],
            [np.sin(pitch), 0, np.cos(pitch)]
        ])
        
        R_yaw = np.array([
            [np.cos(yaw), np.sin(yaw), 0],
            [-np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])
        
        # Combined rotation
        return R_yaw @ R_pitch @ R_roll
    
    def get_euler_angle_rates(self, euler_angles: np.ndarray, 
                              angular_velocity: np.ndarray) -> np.ndarray:
        """Convert angular velocity to Euler angle rates.
        
        Args:
            euler_angles: [roll, pitch, yaw] in radians
            angular_velocity: [p, q, r] in rad/s
            
        Returns:
            Euler angle rates [roll_rate, pitch_rate, yaw_rate]
        """
        roll, pitch, yaw = euler_angles
        p, q, r = angular_velocity
        
        # Transformation matrix
        tan_pitch = np.tan(pitch)
        sec_pitch = 1.0 / np.cos(pitch)
        
        roll_rate = p + q * np.sin(roll) * tan_pitch + r * np.cos(roll) * tan_pitch
        pitch_rate = q * np.cos(roll) - r * np.sin(roll)
        yaw_rate = q * np.sin(roll) * sec_pitch + r * np.cos(roll) * sec_pitch
        
        return np.array([roll_rate, pitch_rate, yaw_rate], dtype=np.float64)
    
    def update(self, delta_time: float, thrust: float):
        """Update aircraft state for one time step.
        
        Args:
            delta_time: Time step in seconds
            thrust: Engine thrust in Newtons
        """
        aircraft = self.aircraft
        props = aircraft.properties
        
        # Get aerodynamic forces
        aero_forces, aero_moments = self.aerodynamics.calculate_aerodynamic_forces(aircraft)
        
        # Thrust force (along body X-axis)
        thrust_force = np.array([thrust, 0.0, 0.0], dtype=np.float64)
        
        # Gravity force in body frame
        R = self.get_rotation_matrix(aircraft.euler_angles)
        gravity_world = np.array([0.0, 0.0, aircraft.get_total_mass() * self.GRAVITY], 
                                 dtype=np.float64)
        gravity_body = R.T @ gravity_world
        
        # Total forces
        total_forces = aero_forces + thrust_force + gravity_body
        
        # Linear acceleration (body frame)
        mass = aircraft.get_total_mass()
        accel_body = total_forces / mass
        
        # Angular acceleration (simplified - no gyroscopic effects yet)
        # τ = I·α
        inertia_matrix = np.diag([props.ixx, props.iyy, props.izz])
        angular_accel = np.linalg.solve(inertia_matrix, aero_moments)
        
        # Update velocity (body frame)
        aircraft.velocity_body += accel_body * delta_time
        
        # Update angular velocity
        aircraft.angular_velocity += angular_accel * delta_time
        
        # Update position (world frame)
        velocity_world = R @ aircraft.velocity_body
        aircraft.position += velocity_world * delta_time
        
        # Update Euler angles
        euler_rates = self.get_euler_angle_rates(aircraft.euler_angles, 
                                                  aircraft.angular_velocity)
        aircraft.euler_angles += euler_rates * delta_time
        
        # Update fuel
        aircraft.update_fuel(delta_time, thrust)
