# Environment Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9 or higher
- Git
- pip (Python package manager)

### Automated Setup

**Option 1: macOS / Linux**
```bash
chmod +x scripts/setupenv.sh
./scripts/setupenv.sh
```

**Option 2: Windows**
```batch
scripts\setupenv.bat
```

The script will:
1. Clone the repository (if needed)
2. Create Python virtual environment
3. Install all dependencies
4. Set up Git hooks
5. Verify installation

### Manual Setup

**Step 1: Clone Repository**
```bash
git clone https://github.com/Omkar-codes0105/virtual-desktop-controller.git
cd virtual-desktop-controller
```

**Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
```

**Step 3: Activate Virtual Environment**
- Linux/macOS: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Step 4: Upgrade pip**
```bash
pip install --upgrade pip
```

**Step 5: Install Dependencies**
```bash
pip install -r config/requirements.txt
pip install -r config/requirements-dev.txt  # For development
```

**Step 6: Verify Installation**
```bash
python scripts/verifysetup.py
```

## Daily Workflow

### Activate Environment
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Run Application
```bash
python src/main.py
```

### Run Tests
```bash
pytest tests/ -v
```

## Hardware Requirements

### Minimum (Low-End)
- Processor: Intel Pentium N5000 or equivalent
- RAM: 4GB
- GPU: Intel UHD 500 (integrated)

### Recommended (Mid-Range)
- Processor: Intel i5-1135G7 or equivalent
- RAM: 8GB
- GPU: Intel Iris Xe

### Optimal (High-End)
- Processor: Intel i7-12700H or equivalent
- RAM: 16GB
- GPU: NVIDIA RTX 3060 or better

## Troubleshooting

### Python Not Found
```bash
python --version  # Check Python is installed
python3 --version  # Try Python 3
```

### Permission Denied (Linux/macOS)
```bash
chmod +x scripts/setupenv.sh
```

### Virtual Environment Not Activating
- Check script is in project root
- Ensure you have write permissions
- Try manual activation

### Dependency Installation Fails
```bash
pip install --upgrade pip setuptools wheel
pip install -r config/requirements.txt --no-cache-dir
```

## Environment Variables

Create a `.env` file in project root:
```
DEBUG=True
LOG_LEVEL=INFO
HARDWARE_TIER=midrange  # highend, midrange, lowend
```

## IDE Setup

### PyCharm
1. File → Open → Select project folder
2. Configure interpreter: Settings → Python Interpreter
3. Select `venv/bin/python` (Linux/macOS) or `venv\Scripts\python.exe` (Windows)

### VS Code
1. Install Python extension
2. Cmd+Shift+P → Python: Select Interpreter
3. Choose `.venv/bin/python`
4. Open terminal - it will auto-activate

## Git Configuration

```bash
# Set user identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch
git config --global init.defaultBranch main
```

## Next Steps

1. Read [DEVELOPMENT.md](./DEVELOPMENT.md) for workflow
2. Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
3. Check your assigned role in the README
4. Create a feature branch and start coding!
