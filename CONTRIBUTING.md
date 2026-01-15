# Contributing to Virtual Desktop Controller

First off, thank you for considering contributing to Virtual Desktop Controller! It's people like you that make this project such a great tool for accessibility.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue
* **Describe the exact steps which reproduce the problem** in as many details as possible
* **Provide specific examples to demonstrate the steps** - include links, file references, or copy/paste snippets
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible** - show how the bug manifests
* **Include your environment** - OS, Python version, hardware tier (high-end, mid-range, low-end)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

* **Use a clear and descriptive title** for the issue
* **Provide a step-by-step description** of the suggested enhancement
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected behavior**
* **Explain why this enhancement would be useful** to most users

## Pull Request Process

1. **Read** [DEVELOPMENT.md](./DEVELOPMENT.md) and [SETUP.md](./SETUP.md)
2. **Follow** the development workflow outlined in DEVELOPMENT.md
3. **Ensure** all tests pass locally before pushing
4. **Format** your code with Black and lint with Flake8
5. **Write** clear commit messages following the convention
6. **Create** a PR with a clear description
7. **Link** related issues in your PR description
8. **Request review** from the relevant role leads
9. **Address review feedback** promptly
10. **Squash commits** if requested before merging

## Styleguides

### Git Commit Messages

* Use the imperative mood ("add feature" not "added feature")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Use role-specific prefixes: `GESTURE:`, `EYETRACK:`, `UI:`, `PERF:`, `TEST:`, `DOCS:`

**Example:**
```
GESTURE: Implement hand detection with MediaPipe

- Integrated MediaPipe Hands API
- Added confidence threshold filtering
- Achieves 96% detection accuracy
- Implements latency optimization

Closes #42
See also #21, #39
```

### Python Styleguide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these additions:

* Use **type hints** for all function parameters and return values
* Write **docstrings** for all public functions, classes, and modules
* Keep **line length** to 100 characters maximum
* Use **meaningful variable names** - avoid single letters except for loops
* Add **comments** for complex logic, not obvious code

**Example:**
```python
from typing import List, Tuple
import numpy as np

def calculate_hand_confidence(
    landmarks: List[float],
    hand_id: int
) -> Tuple[float, bool]:
    """Calculate confidence score for detected hand.
    
    Args:
        landmarks: Hand landmark coordinates from MediaPipe
        hand_id: Unique identifier for the hand
        
    Returns:
        Tuple of (confidence_score, is_valid) where:
        - confidence_score: Float between 0 and 1
        - is_valid: Boolean indicating if hand meets threshold
    """
    # Calculate average distance from hand center
    center = np.mean(landmarks, axis=0)
    distances = np.linalg.norm(landmarks - center, axis=1)
    confidence = 1.0 - (np.std(distances) / np.mean(distances))
    
    return float(confidence), confidence > 0.7
```

### Documentation Styleguide

* Use **Markdown** for all documentation
* Reference code with triple backticks and language specification
* Include examples when explaining features
* Keep technical depth appropriate for target audience
* Link to related documentation sections

## Testing

* **Write tests** for all new features
* **Maintain 80%+ code coverage** for your module
* **Test edge cases** and error conditions
* **Use descriptive test names** that explain what is being tested
* **Run tests locally** before pushing

**Example Test:**
```python
import pytest
from gesture.gesture_recognizer import GestureRecognizer

class TestGestureRecognizer:
    """Test cases for GestureRecognizer class."""
    
    @pytest.fixture
    def recognizer(self):
        """Create a GestureRecognizer instance for testing."""
        return GestureRecognizer(confidence_threshold=0.8)
    
    def test_recognizes_closed_fist(self, recognizer):
        """Test recognition of closed fist gesture."""
        landmarks = create_mock_fist_landmarks()
        gesture = recognizer.recognize(landmarks)
        assert gesture == "closed_fist"
    
    def test_filters_low_confidence(self, recognizer):
        """Test that low-confidence detections are filtered."""
        landmarks = create_mock_landmarks(confidence=0.7)
        gesture = recognizer.recognize(landmarks)
        assert gesture is None
```

## Naming Conventions

### Files
- Use `snake_case` for Python files: `hand_detection.py`
- Use `snake_case` for test files: `test_hand_detection.py`
- Use `UPPER_CASE` for documentation: `README.md`, `SETUP.md`

### Classes
- Use `PascalCase`: `HandDetector`, `GazeEstimator`
- Use descriptive names

### Functions & Variables
- Use `snake_case`: `detect_hands()`, `confidence_threshold`
- Use descriptive names indicating purpose

### Constants
- Use `UPPER_CASE`: `CONFIDENCE_THRESHOLD = 0.8`
- Define at module level

## Issues and Discussion

* **Questions**: Use GitHub Discussions
* **Bug Reports**: Use GitHub Issues with "bug" label
* **Feature Requests**: Use GitHub Issues with "enhancement" label
* **General Discussion**: Use GitHub Discussions

## Recognition

Contributors will be:
* Listed in [README.md](./README.md)
* Mentioned in release notes
* Credited in commit messages

## Questions?

* Read [DEVELOPMENT.md](./DEVELOPMENT.md) for workflow details
* Check [README.md](./README.md) for project overview
* Open a Discussion for questions
* Email the project maintainers

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help organize and categorize issues and pull requests.

#### Type of Issue and Issue State
* `bug` - Confirmed bugs or reports that are very likely to be bugs
* `enhancement` - Feature requests
* `documentation` - Improvements or additions to documentation
* `duplicate` - Issues which are duplicates of other issues
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - The core team has decided not to fix these issues for now

## License

By contributing to Virtual Desktop Controller, you agree that your contributions will be licensed under the [MIT License](./LICENSE).

Thank you for contributing! 🎉
