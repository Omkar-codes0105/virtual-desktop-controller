#!/usr/bin/env python3
"""Test eye tracking independently."""
import sys
import cv2
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from eyetracking.eye_tracker import EyeTracker


def main():
    print("Testing Eye Tracking...")
    print("Press 'q' to quit")
    print("-" * 40)

    tracker = EyeTracker()
    if tracker.landmarker is None:
        print("ERROR: Eye tracker failed to initialize")
        print("Make sure to run: python scripts/download_models.py")
        return 1

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open camera")
        return 1

    print("Camera opened")
    print("Eye tracker ready")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data = tracker.process_frame(frame)

        if data['landmarks']:
            tracker.draw_landmarks(frame, data['landmarks'])

        if data['gaze_point']:
            gx, gy = data['gaze_point']
            h, w, _ = frame.shape
            px, py = int(gx * w), int(gy * h)
            cv2.circle(frame, (px, py), 10, (0, 0, 255), -1)
            cv2.circle(frame, (px, py), 15, (0, 0, 255), 2)
            text = f"Gaze ({gx:.2f}, {gy:.2f})"
            cv2.putText(frame, text, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print(f"\r{text}", end='')

        cv2.imshow('Eye Tracking Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nTest completed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
