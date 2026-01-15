# Virtual Desktop Controller

**Multimodal Eye-Gaze and Gesture Control for Motor-Impaired Accessibility - DIPEX 2026**

## Overview

Virtual Desktop Controller is a comprehensive accessibility solution that combines eye-gaze tracking and hand gesture recognition to provide an intuitive, hands-free interface for users with motor impairments. This project leverages MediaPipe for real-time hand and eye tracking, integrated with a PyQt5 UI featuring accessibility-first design.

## Key Features

- **Eye-Gaze Tracking**: Real-time iris detection with 9-point calibration and Kalman filtering for smooth cursor movement
- **Gesture Recognition**: Hand detection and gesture training with confidence scoring
- **Hybrid Control**: Seamless integration of eye-gaze and gesture inputs for flexible control
- **Accessibility UI**: High-contrast theme (15:1 ratio) with dwell-click indicators
- **Performance Optimization**: Adaptive complexity based on hardware capabilities (high-end, mid-range, low-end)
- **Accessibility Standards**: WCAG compliance with tremore filtering and smooth motion

## Project Structure

This is a collaborative, role-based project with 6 specialized teams:

```
virtual-desktop-controller/
├── src/
│   ├── core/              # Shared utilities (camera, config, logging)
│   ├── gesture/           # Gesture recognition module (Role 1)
│   ├── eyetracking/       # Eye-gaze tracking module (Role 2)
│   ├── ui/                # UI & accessibility module (Role 3)
│   ├── performance/       # Performance optimization module (Role 4)
│   ├── utils/             # Shared utility functions
│   └── main.py           # Entry point
├── tests/
│   ├── unit/             # Unit tests (Role 5)
│   ├── integration/       # Integration tests
│   ├── fixtures/         # Test fixtures & mock data
│   └── conftest.py      # Pytest configuration
├── docs/                  # Documentation (Role 6)
├── config/               # Configuration files
├── scripts/              # Automation scripts
├── .github/workflows/    # CI/CD pipelines
├── requirements.txt      # Core dependencies
├── requirements-dev.txt  # Development dependencies
├── SETUP.md             # Environment setup guide
├── DEVELOPMENT.md       # Development workflow
├── ARCHITECTURE.md      # System design documentation
└── README.md           # This file
```

## Team Roles

| Role | Responsibility | Module |
|------|----------------|--------|
| **Role 1** | Gesture Recognition | `src/gesture/` |
| **Role 2** | Eye-Tracking | `src/eyetracking/` |
| **Role 3** | UI & Accessibility | `src/ui/` |
| **Role 4** | Performance Optimization | `src/performance/` |
| **Role 5** | Testing & QA | `tests/` |
| **Role 6** | Documentation | `docs/` |

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- 4GB RAM minimum (8GB recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/Omkar-codes0105/virtual-desktop-controller.git
cd virtual-desktop-controller

# Run automated setup (macOS/Linux)
chmod +x scripts/setupenv.sh
./scripts/setupenv.sh

# Or on Windows
scripts\setupenv.bat
```

For detailed setup instructions, see [SETUP.md](./SETUP.md)

## Development Workflow

1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Develop**: Write code following PEP 8 standards
3. **Test**: Run unit tests `pytest tests/`
4. **Format**: `black src/ tests/`
5. **Lint**: `flake8 src/ tests/` and `mypy src/`
6. **Commit**: `git commit -m "TYPE: Description"`
7. **Push & Create PR**: Create pull request against `develop` branch
8. **Review**: Get approval from relevant role leads
9. **Merge**: Merge to `develop` after CI passes

For comprehensive guidelines, see [DEVELOPMENT.md](./DEVELOPMENT.md)

## Architecture

The project follows a **Hub & Spoke** model:

- **Hub**: Shared core modules (`src/core/`) - single source of truth
  - `camera.py`: Unified camera input (1080p, 30 FPS)
  - `configmanager.py`: Configuration management
  - `logger.py`: Unified logging
  - `constants.py`: Global constants

- **Spokes**: Role-specific modules
  - Each role owns their module and API
  - Integration via well-defined interfaces
  - No direct file editing across roles

[See ARCHITECTURE.md for detailed system design](./ARCHITECTURE.md)

## Dependencies

### Core
- OpenCV 4.8.1+
- MediaPipe 0.10.0+ (Hand & Face Mesh)
- NumPy 1.24.3+
- PyQt5 5.15.9+ (UI)
- PyAutoGUI 0.9.53+ (Action execution)
- PyTorch 2.0.1+ (ML models)
- GRLib 1.0.0+ (Gesture training)

### Development
- pytest 7.4.0+ (Testing)
- black 23.7.0+ (Code formatting)
- flake8 6.0.0+ (Linting)
- mypy 1.4.1+ (Type checking)
- sphinx 7.0.1+ (Documentation)

[Full dependency list](./requirements.txt)

## Hardware Support

The project supports three hardware tiers:

### High-End
- RTX 3060 GPU
- Intel i7-12700H
- Full HD processing at 30 FPS

### Mid-Range
- Intel Iris Xe
- Intel i5-1135G7
- 720p processing with adaptive downgrading

### Low-End
- Intel UHD 500
- Pentium N5000
- Reduced resolution, lower frame rate

## CI/CD Pipeline

Automated testing and quality checks on every commit:

- **Unit Tests**: `pytest` with coverage reporting
- **Code Quality**: Black formatting, Flake8 linting, MyPy type checking
- **Integration Tests**: Full module integration testing
- **Build**: Package creation for Windows (.exe) and macOS (.app)

## Contributing

We welcome contributions! Please:

1. Read [CONTRIBUTING.md](./CONTRIBUTING.md)
2. Follow the [Development Workflow](./DEVELOPMENT.md)
3. Ensure all tests pass locally
4. Submit PR against `develop` branch
5. Wait for role-lead review and CI approval

## Documentation

- [Setup Guide](./SETUP.md) - Environment setup for all team members
- [Development Guide](./DEVELOPMENT.md) - Development workflow and best practices
- [Architecture](./ARCHITECTURE.md) - System design and module interactions
- [API Reference](./docs/APIREFERENCE.md) - API documentation
- [User Manual](./docs/USERMANUAL.md) - Complete usage guide

## Testing

Run all tests:

```bash
pytest tests/ -v --cov=src
```

Run specific test module:

```bash
pytest tests/unit/testhanddetection.py -v
```

## Performance

Real-time performance monitoring:

```bash
python scripts/profileperformance.sh
```

Latency targets:
- Eye-gaze to cursor: <100ms
- Gesture recognition: <200ms
- UI response: <50ms

## Known Limitations

- Requires adequate lighting for accurate eye-gaze tracking
- Hand gestures work best with clear hand visibility
- Accuracy degrades with fast head movements
- Hardware-dependent performance

## Troubleshooting

### Camera Not Detected
```bash
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Module Import Errors
```bash
python scripts/verifysetup.py
```

### Low FPS/Latency Issues
Check hardware tier and adjust in `config/hardwareprofiles/`

## License

MIT License - See [LICENSE](./LICENSE) file for details

## Authors

**DIPEX 2026 Team**
- Role 1: Gesture Recognition Lead
- Role 2: Eye-Tracking Lead
- Role 3: UI Designer
- Role 4: Performance Lead
- Role 5: QA Lead
- Role 6: Documentation Lead

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand and eye detection
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for accessible UI
- [OpenCV](https://opencv.org/) for computer vision capabilities
- DIPEX 2026 competition organizers

## Support

For issues and questions:
- Open a [GitHub Issue](https://github.com/Omkar-codes0105/virtual-desktop-controller/issues)
- Start a [Discussion](https://github.com/Omkar-codes0105/virtual-desktop-controller/discussions)
- Contact via [Email Support](mailto:support@example.com)

## Status

**Project Status**: 🚀 Active Development (DIPEX 2026)

**Last Updated**: January 2026

---

*Making technology accessible to everyone* ♿✨
