#!/usr/bin/env python3
"""Download required MediaPipe model files."""
import requests
from pathlib import Path
import sys

MODELS = {
    'hand_landmarker.task': (
        'https://storage.googleapis.com/mediapipe-models/hand_landmarker/'
        'hand_landmarker/float16/1/hand_landmarker.task'
    ),
    'face_landmarker.task': (
        'https://storage.googleapis.com/mediapipe-models/face_landmarker/'
        'face_landmarker/float16/1/face_landmarker.task'
    ),
}


def download_model(name, url, models_dir):
    """Download a model file."""
    filepath = models_dir / name
    if filepath.exists():
        print(f"  {name} already exists")
        return True
    print(f"  Downloading {name}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  {name} downloaded successfully")
        return True
    except Exception as e:
        print(f"  Failed to download {name}: {e}")
        return False


def main():
    project_root = Path(__file__).parent.parent
    models_dir = project_root / 'models'
    models_dir.mkdir(exist_ok=True)

    print("Downloading MediaPipe model files...")
    print(f"Models directory: {models_dir}")
    print("-" * 50)

    success = True
    for name, url in MODELS.items():
        if not download_model(name, url, models_dir):
            success = False

    print("-" * 50)
    if success:
        print("All models downloaded successfully!")
        print("\nNext steps:")
        print("  python scripts/test_gesture.py")
        print("  python scripts/test_eye_tracking.py")
        print("  python src/main.py")
    else:
        print("Some models failed to download")
        sys.exit(1)


if __name__ == '__main__':
    main()
