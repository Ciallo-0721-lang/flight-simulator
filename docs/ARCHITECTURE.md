# Flight Simulator Architecture

## Overview

This document describes the high-level architecture of the Flight Simulator game.

## System Components

### 1. Core Engine (`src/core/`)

The core game engine manages the main game loop, state machine, and overall application lifecycle.

**Key Classes:**
- `GameEngine`: Main application loop
- `GameState`: Enumeration of game states
- `Config`: Configuration management

**Responsibilities:**
- Initialize and manage the game loop
- Handle game state transitions
- Coordinate all subsystems

### 2. Physics Engine (`src/physics/`)

Implements realistic flight dynamics using 6-DOF rigid body motion and aerodynamic calculations.

**Key Classes:**
- `FlightDynamics`: 6-DOF rigid body dynamics solver
- `AerodynamicsModel`: Aerodynamic force and moment calculations
- `Aircraft`: Aircraft model with state and properties

**Key Equations:**

**Linear Motion:**
```
F = ma
a = F/m
v = v + a*dt
p = p + v*dt
```

**Angular Motion:**
```
τ = Iα
α = I^-1 * τ
ω = ω + α*dt
```

**Lift Calculation:**
```
L = 0.5 * ρ * V² * S * CL
```

**Drag Calculation:**
```
D = 0.5 * ρ * V² * S * CD
CD = CD0 + k*CL²
```

### 3. Graphics System (`src/graphics/`)

Handles all rendering, including 3D graphics, terrain, and user interface.

**Key Classes:**
- `Renderer`: Low-level rendering commands
- `HUD`: Heads-up display and flight instruments

**Rendering Pipeline:**
1. Clear screen
2. Render terrain/environment
3. Render aircraft
4. Render HUD/UI
5. Swap buffers

### 4. Input System (`src/input/`)

Manages user input from keyboard, mouse, and joystick devices.

**Key Classes:**
- `InputManager`: Unified input handling

**Input Mapping:**
- Keyboard: WASD for pitch/roll, QE for yaw, Space/Ctrl for throttle
- Joystick: Analog stick for pitch/roll, triggers for throttle

### 5. Utility Functions (`src/utils/`)

Common mathematical functions and utilities.

**Functions:**
- `quaternion_to_euler()`: Convert quaternion to Euler angles
- `euler_to_quaternion()`: Convert Euler angles to quaternion
- `clamp()`: Clamp value to range
- `lerp()`: Linear interpolation

## Data Flow

```
Input Manager
    ↓
Game Engine (Main Loop)
    ↓
┌───────────────────┐
│   Update Phase    │
├───────────────────┤
│ • Physics Engine  │
│ • Aerodynamics    │
│ • Aircraft State  │
└───────────────────┘
    ↓
┌───────────────────┐
│   Render Phase    │
├───────────────────┤
│ • Graphics Engine │
│ • HUD/Instruments │
│ • UI Elements     │
└───────────────────┘
    ↓
Display Output
```

## Physics Simulation

### State Variables

The aircraft state consists of:

**Position:** `[x, y, z]` in world frame (meters)
**Velocity:** `[u, v, w]` in body frame (m/s)
**Euler Angles:** `[roll, pitch, yaw]` in radians
**Angular Velocity:** `[p, q, r]` in body frame (rad/s)

### Coordinate Frames

**World Frame (NED - North, East, Down):**
- X-axis points North
- Y-axis points East
- Z-axis points Down

**Body Frame:**
- X-axis points forward (nose)
- Y-axis points right (wing)
- Z-axis points down

### Integration Method

The physics engine uses a simple Euler integration scheme for first-order accuracy.
For better stability, consider RK4 (Runge-Kutta 4th order) in the future.

```python
a = F/m
v = v + a*dt
p = p + v*dt
```

## Configuration

Configuration files are in YAML format:

- `config/settings.yaml`: Game settings (display, physics, audio)
- `config/aircraft.yaml`: Aircraft specifications

## Extension Points

### Adding New Aircraft

1. Add entry to `config/aircraft.yaml`
2. Load in aircraft factory function
3. Update HUD if needed for aircraft-specific instruments

### Adding New Game Systems

1. Create new module in `src/systems/`
2. Initialize in `GameEngine.__init__()`
3. Call update in main loop
4. Integrate with physics engine as needed

### Adding Environmental Effects

1. Implement in `AerodynamicsModel`
2. Add weather system in `src/systems/weather.py`
3. Update air density calculations

## Performance Considerations

- Physics updates run at higher frequency (120 Hz) than rendering (60 Hz)
- Aerodynamic calculations use simplified models for speed
- Consider spatial partitioning for terrain collision in future
- Profile hot paths regularly

## Testing Strategy

- Unit tests for physics calculations
- Integration tests for system interactions
- Validation against real flight data (if available)
- Performance benchmarks

## Future Enhancements

1. **Advanced Aerodynamics:** Turbulence, wind, weather effects
2. **Failure Systems:** Engine failures, hydraulic failures, etc.
3. **Advanced Graphics:** 3D terrain, lighting, particles
4. **Multiplayer:** Network synchronization, shared world
5. **VR Support:** Head tracking, controller support
6. **AI Pilots:** Autopilot, ATC, traffic
