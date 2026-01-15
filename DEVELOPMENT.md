# Development Guide

## Workflow Overview

This document outlines the development workflow for the Virtual Desktop Controller project. All team members must follow these guidelines to ensure smooth collaboration.

## Development Workflow

### Step 1: Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

**Branch naming convention:**
- `feature/gesture-training` - New features
- `fix/iris-calibration-accuracy` - Bug fixes
- `docs/user-manual` - Documentation
- `chore/update-dependencies` - Maintenance tasks

### Step 2: Activate Virtual Environment

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Run Tests to Ensure Baseline

```bash
pytest tests/ -v --cov=src
```

### Step 4: Start Coding

1. Edit files in your assigned module:
   - **Role 1**: `src/gesture/`
   - **Role 2**: `src/eyetracking/`
   - **Role 3**: `src/ui/`
   - **Role 4**: `src/performance/`
   - **Role 5**: `tests/`
   - **Role 6**: `docs/`

2. Follow code standards:
   - **PEP 8** style guide
   - Type hints for all functions
   - Docstrings for all classes and public methods
   - Maximum line length: 100 characters

### Step 5: Run Tests Frequently

```bash
# Run tests for your module
pytest tests/unit/test_your_module.py -v

# Run with coverage
pytest tests/ --cov=src/your_module
```

### Step 6: Format and Lint Code

```bash
# Format with Black
black src/your_module/

# Lint with Flake8
flake8 src/your_module/

# Type check with mypy
mypy src/your_module/
```

### Step 7: Commit Changes

```bash
git add src/gesture/handdetection.py
git commit -m "GESTURE: Implement hand detection at 30 FPS

- Integrated MediaPipe Hands
- Added confidence thresholding
- Achieves 96% accuracy baseline

Closes #12"
```

**Commit message format:**
```
TYPE: Short description

Detailed explanation of changes.
- Bullet point 1
- Bullet point 2

Closes #issue_number
```

**Types:**
- `GESTURE`, `EYETRACK`, `UI`, `PERF`, `TEST`, `DOCS`
- `feat`, `fix`, `docs`, `chore`, `refactor`, `style`

### Step 8: Push to GitHub

```bash
git push origin feature/your-feature-name
```

### Step 9: Create Pull Request

1. Go to GitHub repository
2. Click "Compare & pull request"
3. Fill out PR template:
   - **Title**: `GESTURE: Implement hand detection`
   - **Description**: Link to issue, explain changes
   - **Related Issues**: `Closes #12`
   - **Type of Change**: Feature/Bug Fix/Documentation
   - **Checklist**: Tests passing, code formatted, docs updated

### Step 10: Code Review

- **Role Lead Review**: Role-specific lead reviews your code
- **QA Review**: QA lead ensures tests are adequate
- **Project Lead Approval**: Final approval for merge
- **Automated Checks**: CI/CD pipeline must pass
  - Unit tests
  - Code coverage (>80%)
  - Linting checks
  - Type checking

### Step 11: Address Feedback

If reviewers request changes:

```bash
# Make the changes locally
git add .
git commit -m "Address review feedback"
git push origin feature/your-feature-name
```

The PR will update automatically. Re-request review from role leads.

### Step 12: Merge to Develop

Once approved:
1. **Project Lead** merges PR to `develop` branch
2. CI/CD pipeline runs automatically
3. Your branch is deleted

## Weekly Integration Cycle

### Monday 10:00 AM - Kickoff
- Review PRs merged last week
- Discuss this week's priorities
- Identify blockers and risks
- Update GitHub Projects board

### Tuesday-Thursday - Development
- Write code and tests
- Commit and push frequently
- Create PRs by end of day

### Friday 2:00 PM - Integration Testing
- Merge all PRs from the week to `develop`
- Run full integration test suite
- Test interactions between modules:
  - Eye-gaze + gesture coordination
  - UI responsiveness with both inputs
  - Performance under load
- Fix any critical issues

### Friday 4:00 PM - Demo & Release
- Each role demos their weekly progress
- Collect feedback from team
- Update documentation
- Create release notes
- Merge `develop` → `main` (if stable)
- Tag with version number (v0.x.y)

## Code Quality Standards

### Testing Requirements

**Unit Tests** (Per Module):
- Minimum 80% code coverage
- Test happy path, edge cases, error handling
- Use pytest fixtures for common setup
- Mock external dependencies (camera, hardware)

**Integration Tests**:
- Test module interactions
- Example: hand detection + action execution
- Run weekly after merges to `develop`

**Example Test Structure:**
```python
def test_hand_detection_confidence_threshold():
    """Test hand detection filters low-confidence detections."""
    detector = HandDetector(confidence_threshold=0.8)
    low_conf_hand = create_mock_hand(confidence=0.7)
    result = detector.detect(low_conf_hand)
    assert result is None  # Should filter out
```

### Code Style

```python
# Good: Type hints + docstring
def calculate_gaze_point(
    iris_landmarks: List[float],
    camera_matrix: np.ndarray
) -> Tuple[float, float]:
    """Calculate gaze point from iris landmarks.
    
    Args:
        iris_landmarks: Normalized iris point coordinates
        camera_matrix: Camera calibration matrix
        
    Returns:
        Tuple of (x, y) gaze coordinates on screen
    """
    pass
```

## Communication

### Synchronous (Real-time)
- **Monday 10 AM**: Weekly kickoff (all roles)
- **Wednesday 2 PM**: Mid-week sync (resolve blockers)
- **Friday 4 PM**: Demo & release planning

### Asynchronous (Documented)
- **GitHub Issues**: Bugs, feature requests, discussions
- **GitHub Discussions**: Design decisions, general questions
- **PR Comments**: Code review feedback
- **Documentation**: Update docs/ folder with API changes

## Troubleshooting

### Test Failures

```bash
# Run tests with verbose output
pytest tests/unit/test_module.py -vv -s

# Run specific test
pytest tests/unit/test_module.py::test_function_name -v

# Clear pytest cache
pytest --cache-clear
```

### Merge Conflicts

```bash
# Resolve conflicts locally
git merge develop
# Edit conflicting files
git add .
git commit -m "Resolve merge conflicts"
```

### Branch Out of Sync

```bash
git fetch origin
git rebase origin/develop
git push --force-with-lease origin feature/branch-name
```

## CI/CD Pipeline

Automated checks run on every PR:

1. **Unit Tests** (`pytest`)
   - All tests in `tests/` must pass
   - Coverage must be >80%

2. **Code Quality**
   - Black formatting check
   - Flake8 linting
   - MyPy type checking

3. **Build** (on `main` branch)
   - Create Windows .exe installer
   - Create macOS .app bundle
   - Upload to releases

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Workflow](https://git-scm.com/book/en/v2)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## Questions?

Refer to:
1. [README.md](./README.md) - Project overview
2. [SETUP.md](./SETUP.md) - Environment setup
3. [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
4. GitHub Issues - Ask the team
