# Flight Simulator

A high-fidelity flight simulation game built with Python and Pygame.

## Overview

This project aims to create a realistic flight simulation game that features:

- **Realistic Physics**: Accurate 6-DOF rigid body dynamics
- **Aerodynamic Modeling**: Lift, drag, and stall calculations
- **Engine Systems**: Thrust, fuel consumption, and temperature management
- **Environmental Systems**: Terrain, weather, and day/night cycle
- **Intuitive Controls**: Keyboard and joystick support
- **Visual Feedback**: Real-time HUD and instruments

## Project Structure

```
flight-simulator/
├── src/
│   ├── core/              # Core game engine
│   ├── physics/           # Flight dynamics and physics
│   ├── graphics/          # Rendering system
│   ├── input/             # Control input handling
│   ├── systems/           # Game systems (engine, fuel, etc.)
│   ├── utils/             # Utility functions
│   └── main.py            # Application entry point
├── assets/
│   ├── models/            # 3D models (placeholder)
│   ├── textures/          # Textures (placeholder)
│   ├── sounds/            # Audio files (placeholder)
│   └── data/              # Aircraft specifications
├── config/
│   ├── settings.yaml      # Game settings
│   └── aircraft.yaml      # Aircraft configurations
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ciallo-0721-lang/flight-simulator.git
cd flight-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```bash
python src/main.py
```

## Controls

### Keyboard Controls
- **W/S**: Pitch up/down
- **A/D**: Roll left/right
- **Q/E**: Yaw left/right
- **Space**: Increase throttle
- **Ctrl**: Decrease throttle
- **R**: Reset aircraft
- **ESC**: Quit game

### Joystick Support
- Analog stick: Pitch and roll
- Triggers: Throttle control
- Buttons: Gear, flaps, etc.

## Development

### Architecture Overview

#### Core Engine (`src/core/`)
- Game loop management
- State management
- Event handling

#### Physics Engine (`src/physics/`)
- Flight dynamics (6-DOF rigid body)
- Aerodynamics calculations
- Collision detection

#### Graphics (`src/graphics/`)
- 3D rendering pipeline
- HUD and UI rendering
- Terrain and environment

#### Input System (`src/input/`)
- Keyboard input handling
- Joystick/gamepad support
- Control mapping

#### Systems (`src/systems/`)
- Engine system (thrust, temperature)
- Fuel management
- Instrumentation

## Physics Model

### Forces Acting on Aircraft

1. **Lift (L)**: L = 0.5 × ρ × V² × S × CL
2. **Drag (D)**: D = 0.5 × ρ × V² × S × CD
3. **Thrust (T)**: From engine system
4. **Weight (W)**: Gravity force

### 6-DOF Dynamics

The aircraft motion is modeled using:
- Linear acceleration: F = ma
- Angular acceleration: τ = Iα

### Aerodynamic Coefficients

- **Lift Coefficient (CL)**: Varies with angle of attack and stall
- **Drag Coefficient (CD)**: Parasitic drag + induced drag
- **Moment Coefficients**: Cm, Cl, Cn for pitch, roll, yaw

## Aircraft Configuration

Aircraft properties are defined in YAML files:

```yaml
aircraft:
  name: Cessna 172
  mass: 1157  # kg
  wing_area: 16.17  # m²
  aerodynamic:
    cl_max: 1.4
    cd0: 0.027
    k: 0.0525
    stall_angle: 16.0  # degrees
```

## Roadmap

- [x] Project setup and structure
- [ ] Basic physics engine
- [ ] Flight dynamics implementation
- [ ] Aerodynamic model
- [ ] Engine system
- [ ] Terrain rendering
- [ ] Weather system
- [ ] Instrumentation and HUD
- [ ] Mission/scenario system
- [ ] Multiplayer support (future)
- [ ] VR support (future)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## References

- **Flight Dynamics**: Beard, R. W., & McLain, T. W. (2012). Small Unmanned Aircraft: Theory and Practice
- **Aerodynamics**: Anderson, J. D. (2010). Fundamentals of Aerodynamics
- **Game Development**: Pygame Documentation

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Flight Dynamics Papers](https://arc.aiaa.org/)

## Author

- **Ciallo-0721-lang** - Initial framework

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
