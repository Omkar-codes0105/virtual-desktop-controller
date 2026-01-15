# Architecture

## Overview
The Virtual Desktop Controller is a multimodal interface that combines eye-gaze tracking and gesture recognition to provide accessible control for motor-impaired users.

## System Architecture

### Core Components

#### 1. Eye Tracking Module (`src/eyetracking/`)
- **Purpose**: Captures and processes eye-gaze data
- **Key Classes**:
  - `EyeTracker`: Main tracking engine
  - `GazePoint`: Represents a 2D gaze point on screen
  - `CalibrationManager`: Manages tracker calibration

#### 2. Gesture Recognition Module (`src/gesture/`)
- **Purpose**: Recognizes and interprets hand gestures
- **Key Classes**:
  - `GestureRecognizer`: Main recognition engine
  - `Gesture`: Represents a recognized gesture
  - `GestureProfile`: Stores gesture definitions

#### 3. Core Services Module (`src/core/`)
- **Camera Handler**: Manages webcam input
- **Config Manager**: Handles configuration files
- **Logger**: Provides logging functionality

#### 4. UI Module (`src/ui/`)
- **Purpose**: Renders user interface and feedback
- **Components**:
  - Main display interface
  - Gaze visualization
  - Gesture feedback
  - Settings panel

#### 5. Performance Monitor (`src/performance/`)
- Tracks FPS and latency
- Memory profiling
- System resource monitoring

### Data Flow

1. **Input Capture**: Camera stream from webcam
2. **Eye Tracking**: Process frames for gaze position
3. **Gesture Recognition**: Detect hand gestures
4. **Action Mapping**: Map gaze + gestures to desktop actions
5. **Output**: Execute system commands or emulate input

## Module Dependencies

```
main.py
  ├── eyetracking/tracker.py
  ├── gesture/recognizer.py
  ├── core/camera.py
  ├── core/configmanager.py
  ├── core/logger.py
  ├── ui/interface.py
  └── performance/monitor.py
```

## Configuration Structure

- `config/hardware_config.json`: Hardware specifications
- `config/gesture_profiles.json`: Gesture definitions
- `config/ui_themes.json`: UI theme settings

## Testing Strategy

- Unit tests in `tests/`
- Integration tests for module interaction
- Continuous Integration via GitHub Actions

## Development Workflow

See DEVELOPMENT.md for detailed development guidelines.
