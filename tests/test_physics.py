"""Unit tests for physics engine."""

import unittest
import numpy as np
from src.physics.aircraft import Aircraft, AircraftProperties
from src.physics.aerodynamics import AerodynamicsModel
from src.physics.dynamics import FlightDynamics


class TestAircraft(unittest.TestCase):
    """Test Aircraft class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.props = AircraftProperties.cessna_172()
        self.aircraft = Aircraft(self.props)
    
    def test_aircraft_creation(self):
        """Test aircraft initialization."""
        self.assertEqual(self.aircraft.get_airspeed(), 0.0)
        self.assertEqual(self.aircraft.get_altitude(), 0.0)
        self.assertEqual(self.aircraft.fuel_weight, self.props.max_fuel_capacity)
    
    def test_angle_of_attack(self):
        """Test angle of attack calculation."""
        # Set forward velocity
        self.aircraft.velocity_body[0] = 50.0
        aoa = self.aircraft.get_angle_of_attack()
        self.assertAlmostEqual(aoa, 0.0, places=5)
        
        # Set pitching velocity
        self.aircraft.velocity_body[2] = 10.0
        aoa = self.aircraft.get_angle_of_attack()
        expected_aoa = np.arctan2(10.0, 50.0)
        self.assertAlmostEqual(aoa, expected_aoa, places=5)


class TestAerodynamics(unittest.TestCase):
    """Test Aerodynamics model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aero = AerodynamicsModel()
        self.props = AircraftProperties.cessna_172()
        self.aircraft = Aircraft(self.props)
    
    def test_air_density_sea_level(self):
        """Test air density at sea level."""
        rho = self.aero.calculate_air_density(0.0)
        self.assertAlmostEqual(rho, 1.225, places=3)
    
    def test_dynamic_pressure(self):
        """Test dynamic pressure calculation."""
        q = self.aero.calculate_dynamic_pressure(10.0)
        expected_q = 0.5 * 1.225 * 10.0 ** 2
        self.assertAlmostEqual(q, expected_q, places=3)
    
    def test_lift_coefficient_zero_aoa(self):
        """Test lift coefficient at zero angle of attack."""
        cl = self.aero.calculate_lift_coefficient(0.0, self.aircraft)
        self.assertAlmostEqual(cl, 0.0, places=5)


class TestFlightDynamics(unittest.TestCase):
    """Test Flight Dynamics."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.props = AircraftProperties.cessna_172()
        self.aircraft = Aircraft(self.props)
        self.dynamics = FlightDynamics(self.aircraft)
    
    def test_rotation_matrix(self):
        """Test rotation matrix generation."""
        euler = np.array([0.0, 0.0, 0.0])
        R = self.dynamics.get_rotation_matrix(euler)
        
        # Should be identity matrix at zero angles
        np.testing.assert_array_almost_equal(R, np.eye(3), decimal=5)


if __name__ == '__main__':
    unittest.main()
