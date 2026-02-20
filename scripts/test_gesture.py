#!/usr/bin/env python3
"""Test gesture recognition independently."""
import sys
import cv2
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from gesture.gesture_recognizer import GestureRecognizer


def main():
    print("Testing Gesture Recognition...")
    print("Press 'q' to quit")
    print("-" * 40)

    recognizer = GestureRecognizer()
    if recognizer.landmarker is None:
        print("ERROR: Gesture recognizer failed to initialize")
        print("Make sure to run: python scripts/download_models.py")
        return 1

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return 1

    print("Camera opened")
    print("Gesture recognizer ready")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gesture_data = recognizer.process_frame(frame)

        if gesture_data['landmarks']:
            recognizer.draw_landmarks(frame, gesture_data['landmarks'])

        if gesture_data['gesture']:
            text = f"{gesture_data['gesture']} ({gesture_data['confidence']:.2f})"
            cv2.putText(frame, text, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(f"\rDetected: {text}", end='')

        cv2.imshow('Gesture Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nTest completed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
